"""
ConPlc - connect PLC and PC
Copyright (C) 2020  Marvin Mangold (mangold.mangold00@googlemail.com)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
# TODO multidimensional array
import re


# define possible Datatypes and its bit-size
standard_types = {"Bool": 0.125,
                  "Byte": 1,
                  "Word": 2,
                  "DWord": 4,
                  "LWord": 8,
                  "SInt": 1,
                  "USInt": 1,
                  "Int": 2,
                  "UInt": 2,
                  "DInt": 4,
                  "UDInt": 4,
                  "LInt": 8,
                  "ULInt": 8,
                  "Real": 4,
                  "LReal": 8,
                  "Char": 1,
                  "WChar": 2}

special_types = {"String": 2,
                 "WString": 4,
                 "Array": 0,
                 "DTL": 0,
                 "Struct": 0,
                 "UDT": 0}


def read_file(path):
    """
    open/read file
    """
    data = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            stripped = line.strip()
            if stripped != "":
                data.append(stripped)
    return data


def save_entry(filedata, foldernames, entry, saveposition="end"):
    """
    concat prefix to name and save entry in data
    """
    # concat prefix to varname
    varname = ""
    newentry = entry.copy()
    for prefix in foldernames:
        varname += prefix
    newentry["name"] = varname + newentry["name"]
    # save element
    if saveposition == "end":
        filedata.append(newentry)
    elif saveposition == "-1":
        filedata.insert(-1, newentry)


def clean_name(name):
    """
    erase additional info in Varname (internal settings in {} brackets)
    sample: [Test {InstructionName := 'DTL'; LibVersion := '1.0'} : DTL;   // comment Test] --> "Test"
    """
    newname = name
    regex = re.search(r'(.*) {', name)
    if regex is not None:
        newname = regex.group(1)
    return newname


def is_udt(datatype=""):
    """
    check if datatype is special udt type
    regex searching for text between quotation marks
    sample: [Test : "some_UDT";   // comment Test] --> "some_UDT"
    """
    result = False
    regex = re.search(r'"(.*)"', datatype)
    if regex is not None:
        result = True
    return result


def is_struct(line=""):
    """
    get start of udt declaration
    regex searching for text "STRUCT"
    sample: [STRUCT] --> "STRUCT"
    """
    result = False
    regex = re.search(r'STRUCT$', line)
    if regex is not None:
        result = True
    return result


def is_endstruct(line=""):
    """
    get end of Struct declaration
    regex searching for text "END_STRUCT;"
    sample: [END_STRUCT;] --> "END_STRUCT;"
    """
    result = False
    regex = re.search(r'END_STRUCT;', line)
    if regex is not None:
        result = True
    return result


def is_endtype(rawdata):
    """
    get udt-file end indicator
    regex searching for text "END_TYPE"
    sample: [END_TYPE] --> "END_TYPE"
    """
    result = False
    regex = re.search(r'END_TYPE', rawdata[0])
    if regex is not None:
        result = True
    return result


def to_bitaddress(size):
    """
    bits are saved as 0.125 Bytes
    the byteaddress of 8 bits after 10 Bytes is 10.0 - 10.875
    format this to show the byteaddress as 10.0 - 10.7
    sample: 10.857 --> 10.0 + 0,875
    """
    predecimalplace = int(size)
    decimalplace = int(size % 1 / 0.125)
    bitaddress = "{predecimalplace}.{decimalplace}".format(predecimalplace=predecimalplace, decimalplace=decimalplace)
    return float(bitaddress)


def get_datatype(line=""):
    """
    get datatype from VAR declaration datatype
    regex searching for text between ": " and "whitespace or any other symbol except letters"
    sample:  [Test : Bool;   // comment Test] --> "Bool"
    """
    datatype = ""
    regex = re.search(r'(.*) : (.*?)(;|$|\s{3}|\[)', line)
    if regex is not None:
        datatype = regex.group(2)
    return datatype


def get_arraytype(line=""):
    """
    get datatype from array declaration
    regex searching for text between "of " and ";"
    sample: [Test : Array[0..10] of String;   // comment Test] --> "String"
    """
    datatype = ""
    regex = re.search(r'of (.*);', line)
    if regex is not None:
        datatype = regex.group(1)
    return datatype


def get_header_name(rawdata, headerdata):
    """
    get name from header
    regex searching for text after "TYPE" and between quotation marks
    sample: [TYPE "Main"] --> "Main"
    save data in headerdata
    """
    result = False
    regex = re.search(r'TYPE "(.*?)"', rawdata[0])
    if regex is not None:
        result = True
        name = regex.group(1)
        headerdata["name"] = name
        # delete line from rawdata
        rawdata.pop(0)
    return result


def get_header_description(rawdata, headerdata):
    """
    get description from header
    regex searching for text after "TITLE = "
    sample: [TITLE = Main] --> "Main"
    save data in headerdata
    """
    result = False
    regex = re.search(r'TITLE = (.*)', rawdata[0])
    if regex is not None:
        result = True
        description = regex.group(1)
        headerdata["description"] = description
        # delete line from rawdata
        rawdata.pop(0)
    return result


def get_header_version(rawdata, headerdata):
    """
    get version from header
    regex searching for text after "VERSION : "
    sample: [VERSION : 0.1] --> "0.1"
    save data in headerdata
    """
    result = False
    regex = re.search(r'VERSION : (.*)', rawdata[0])
    if regex is not None:
        result = True
        version = regex.group(1)
        headerdata["version"] = version
        # delete line from rawdata
        rawdata.pop(0)
    return result


def get_header_info(rawdata, headerdata):
    """
    get info from header
    regex searching for text after "//"
    sample: [//some comment] --> "some comment"
    save data in headerdata
    """
    result = False
    regex = re.search(r'^/{2}(.*)', rawdata[0])
    if regex is not None:
        result = True
        info = regex.group(1)
        headerdata["info"] = info
        # delete line from rawdata
        rawdata.pop(0)
    return result


def get_header_end(rawdata):
    """
    get header end indicator from header
    regex searching for text "STRUCT"
    sample: [STRUCT] --> "STRUCT"
    """
    result = False
    regex = re.search(r'STRUCT$', rawdata[0])
    if regex is not None:
        result = True
    return result


def get_struct(rawdata, filedata, foldernames):
    """
    get start of udt declaration
    regex searching for text "STRUCT"
    sample: [STRUCT] --> "STRUCT"
    collect data and save it in filedata
    """
    error = False
    errormessage = ""
    result = False
    regex = re.search(r'STRUCT$', rawdata[0])
    if regex is not None:
        result = True
        # last part of struct (end indicator)
        # collect data
        entry = {
            "name": "",
            "datatype": "STRUCT",
            "byte": 0.0,
            "comment": "",
            "visible": False,
            "access": False,
            "action": None,
            "value": "",
            "size": 0}
        # save entry to list "data"
        save_entry(filedata=filedata, foldernames=[], entry=entry)
        # append name prefix to list
        foldernames.append("")
        # delete line from rawdata
        rawdata.pop(0)
    return result, error, errormessage


def get_endstruct(rawdata, filedata, foldernames):
    """
    get end of Struct declaration
    regex searching for text "END_STRUCT;"
    sample: [END_STRUCT;] --> "END_STRUCT;"
    collect data and save it in filedata
    """
    error = False
    errormessage = ""
    result = False
    regex = re.search(r'END_STRUCT;', rawdata[0])
    if regex is not None:
        result = True
        # delete name prefix from list
        foldernames.pop()
        # last part of struct (end indicator)
        # collect data
        entry = {
            "name": "",
            "datatype": "END_STRUCT",
            "byte": 0.0,
            "comment": "",
            "visible": False,
            "access": False,
            "action": "close",
            "value": "",
            "size": 0}
        # save entry to list "data"
        save_entry(filedata=filedata, foldernames=[], entry=entry)
        # delete line from rawdata
        rawdata.pop(0)
    return result, error, errormessage


def get_data_standard(rawdata, filedata, foldernames):
    """
    get data from VAR declaration of a standard datatype
    regex searching for:
        text between start and before " :"
        text between ": " and ";"
        text between "// " and end
    sample:  [Test : Bool;   // comment Test] --> "Test", "Bool", "comment Test"
    collect data and save it in filedata
    """
    error = False
    errormessage = ""
    result = False
    regex = re.search(r'(.*) : (.*);(?:\s{3}// )?(.*)?', rawdata[0])
    if regex is not None:
        result = True
        name, datatype, comment = clean_name(regex.group(1)), regex.group(2), regex.group(3)
        # get size of data
        size = standard_types[datatype]
        # collect data
        entry = {
            "name": name,
            "datatype": datatype,
            "byte": 0.0,
            "comment": comment,
            "visible": True,
            "access": True,
            "action": None,
            "value": "",
            "size": size}
        # save entry to list "data"
        save_entry(filedata=filedata, foldernames=foldernames, entry=entry)
        # delete line from rawdata
        rawdata.pop(0)
    return result, error, errormessage


def get_data_string(rawdata, filedata, foldernames):
    """
    get data from VAR declaration of a string datatype
    regex searching for:
        text between start and before " :"
        text between ": " and "["
        text between "[ " and "]"
        text between "// " and end
    sample:  [Test : String[10];   // comment Test] --> "Test", "String", "10", "comment Test"
    sample:  [Test : String;   // comment Test] --> "Test", "String", None, "comment Test"
    if datatype = String without [xxx] --> set it to String[254] after regex
    collect data and save it in filedata
    """
    error = False
    errormessage = ""
    result = False
    regex = re.search(r'(.*) : (.*?)(?:\[(.*?)?])?;(?:\s{3}// )?(.*)?', rawdata[0])
    if regex is not None:
        result = True
        name, datatype, length, comment = clean_name(regex.group(1)), regex.group(2), regex.group(3), regex.group(4)
        if length is not None:
            length = int(length)
        else:
            length = 254
        # get size of data
        # first Byte of String = maximal length of String
        # second Byte of String = actual length of String
        size_decalration = special_types["String"]
        size_data = standard_types["Char"] * length  # size of data = count of chars * bit-size of a char
        size = size_decalration + size_data
        # collect data
        entry = {
            "name": name,
            "datatype": "{datatype}[{length}]".format(datatype=datatype, length=length),
            "byte": 0.0,
            "comment": comment,
            "visible": True,
            "access": True,
            "action": None,
            "value": "",
            "size": size}
        # save entry to list "data"
        save_entry(filedata=filedata, foldernames=foldernames, entry=entry)
        # delete line from rawdata
        rawdata.pop(0)
    return result, error, errormessage


def get_data_wstring(rawdata, filedata, foldernames):
    """
    get data from VAR declaration of a wstring datatype
    regex searching for:
        text between start and before " :"
        text between ": " and "["
        text between "[ " and "]"
        text between "// " and end
    sample:  [Test : WString[10];   // comment Test] --> "Test", "WString", "10", "comment Test"
    sample:  [Test : WString;   // comment Test] --> "Test", "WString", None, "comment Test"
    if datatype = WString without [xxx] --> set it to WString[254] after regex
    collect data and save it in filedata
    """
    error = False
    errormessage = ""
    result = False
    regex = re.search(r'(.*) : (.*?)(?:\[(.*?)?])?;(?:\s{3}// )?(.*)?', rawdata[0])
    if regex is not None:
        result = True
        name, datatype, length, comment = clean_name(regex.group(1)), regex.group(2), regex.group(3), regex.group(4)
        if length is not None:
            length = int(length)
        else:
            length = 254
        # get size of data
        # first Word of WString = maximal length of WString
        # second Word of WString = actual length of WString
        size_decalration = special_types["WString"]
        size_data = standard_types["WChar"] * length  # size of data = count of wchars * bit-size of a wchar
        size = size_decalration + size_data
        # collect data
        entry = {
            "name": name,
            "datatype": "{datatype}[{length}]".format(datatype=datatype, length=length),
            "byte": 0.0,
            "comment": comment,
            "visible": True,
            "access": True,
            "action": None,
            "value": "",
            "size": size}
        # save entry to list "data"
        save_entry(filedata=filedata, foldernames=foldernames, entry=entry)
        # delete line from rawdata
        rawdata.pop(0)
    return result, error, errormessage


def get_data_array(rawdata, filedata, foldernames, dependencies):
    """
    get data from VAR declaration of a array datatype
    regex searching for:
        text between start and before " :"
        text between ": " and "["
        text between "[" and "]"
        text between "of " and ";"
        text between "// " and end
    sample: [Test : Array[1..8] of Byte;   // comment Test] --> "Test", "Array", "1..8, 0..10", "Byte", "comment Test"
    split "1..8, 0..10" at "," to get all available dimensions of the array
    sample: "1..8, 0..10" --> [1..8, 0..10]
    regex searching for arraysize in every dimension"
        text before ".."
        text after ".."
    collect data and save it in filedata
    """
    error = False
    errormessage = ""
    result = False
    regex = re.search(r'(.*?) : ((.*)\[(.*)\] of (.*));(?:\s{3}// )?(.*)?', rawdata[0])
    if regex is not None:
        name = clean_name(regex.group(1))  # "Test"
        arraydescription = regex.group(2)  # "Array[1..8, 0..10] of Byte"
        datatype = regex.group(3)  # "Array"
        dimensions = regex.group(4).split(",")  # 1..8, 0..10
        arraydatatype = regex.group(5)  # "Byte"
        comment = regex.group(6)  # "// comment Test"
        # get start and end of arraysize for each dimension
        dimensiondata = []  # [{"start": 1, "end": 8}, {"start": 0, "end": 10}]
        for dimension in dimensions:
            dimensionbounds = dimension.split(".")
            dimensiondata.append({"start": dimensionbounds[0], "end": dimensionbounds[2]})
        print(dimensiondata)
        # ---------------------------------
        # first part of array (declaration line)
        # get size of data
        size = special_types[datatype]
        # collect data
        entry = {
            "name": name,
            "datatype": arraydescription,
            "byte": 0.0,
            "comment": comment,
            "visible": True,
            "access": False,
            "action": "open",
            "value": "",
            "size": size}
        # save entry to list "data"
        save_entry(filedata=filedata, foldernames=foldernames, entry=entry)
        # append name prefix to list
        foldernames.append(name + ".")
        # ---------------------------------
        # middle part of array (data)
        # create list of entrys in range arraysize
        elements = []
        # "[1] : Byte;",
        # "[2] : Byte;",
        # "[3] : Byte;",
        # ... and save it to filedata
        for count in range(0, 0+1):
            name = "[{number}]".format(number=str(count))
            elements.append("{name} : {datatype};".format(name=name, datatype=arraydatatype))
        while True:
            dataend, error, errormessage = get_data(rawdata=elements,
                                                    filedata=filedata,
                                                    foldernames=foldernames,
                                                    dependencies=dependencies)
            if dataend or error:
                break
        # ---------------------------------
        # delete name prefix from list
        foldernames.pop()
        # last part of array (end indicator)
        # get size of data
        size = special_types[datatype]
        # collect data
        entry = {
            "name": "",
            "datatype": "END_ARRAY",
            "byte": 0.0,
            "comment": "",
            "visible": False,
            "access": False,
            "action": "close",
            "value": "",
            "size": size}
        # save entry to list "data"
        save_entry(filedata=filedata, foldernames=[], entry=entry)
        # ---------------------------------
        # delete line from rawdata
        rawdata.pop(0)
    return result, error, errormessage


def get_data_dtl(rawdata, filedata, foldernames):
    """
    get data from VAR declaration of a dtl datatype
    regex searching for:
        text between start and before " :"
        text between ": " and ";"
        text between "// " and end
    sample:  [Test {InstructionName := 'DTL'; LibVersion := '1.0'} : DTL;   // comment Test]
    --> "Test {InstructionName := 'DTL'; LibVersion := '1.0'}", "DTL", "comment Test"
    --> name will be cleaned to "Test"
    collect data and save it in filedata
    data:   "YEAR", "UInt"
            "MONTH", "USInt"
            "DAY", "USInt"
            "WEEKDAY", "USInt"
            "HOUR", "USInt"
            "MINUTE", "USInt"
            "SECOND", "USInt"
            "NANOSECOND", "UDint"
    """
    error = False
    errormessage = ""
    result = False
    regex = re.search(r'(.*) : (.*);(?:\s{3}// )?(.*)?', rawdata[0])
    if regex is not None:
        result = True
        # ---------------------------------
        # first part of dtl (declaration line)
        name, datatype, comment = clean_name(regex.group(1)), regex.group(2), regex.group(3)
        # get size of data
        size = special_types[datatype]
        # collect data
        entry = {
            "name": name,
            "datatype": datatype,
            "byte": 0.0,
            "comment": comment,
            "visible": True,
            "access": False,
            "action": "open",
            "value": "",
            "size": size}
        # save entry to list "data"
        save_entry(filedata=filedata, foldernames=foldernames, entry=entry)
        # append name prefix to list
        foldernames.append(name + ".")
        # ---------------------------------
        # middle part of dtl (data)
        data = [["YEAR", "UInt", "Year"],
                ["MONTH", "USInt", "Month"],
                ["DAY", "USInt", "Day"],
                ["WEEKDAY", "USInt", "Weekday"],
                ["HOUR", "USInt", "Hour"],
                ["MINUTE", "USInt", "Minute"],
                ["SECOND", "USInt", "Second"],
                ["NANOSECOND", "UDInt", "Nanosecond"]]
        for element in data:
            name, datatype, comment = element
            # get size of data
            size = standard_types[datatype]
            # collect data
            entry = {
                "name": name,
                "datatype": datatype,
                "byte": 0.0,
                "comment": comment,
                "visible": True,
                "access": True,
                "action": None,
                "value": "",
                "size": size}
            # save entry to list "data"
            save_entry(filedata=filedata, foldernames=foldernames, entry=entry)
        # ---------------------------------
        # delete name prefix from list
        foldernames.pop()
        # last part of dtl (end indicator)
        # get size of data
        size = special_types["DTL"]
        # collect data
        entry = {
            "name": "",
            "datatype": "END_DTL",
            "byte": 0.0,
            "comment": "",
            "visible": False,
            "access": False,
            "action": "close",
            "value": "",
            "size": size}
        # save entry to list "data"
        save_entry(filedata=filedata, foldernames=[], entry=entry)
        # ---------------------------------
        # delete line from rawdata
        rawdata.pop(0)
    return result, error, errormessage


def get_data_struct(rawdata, filedata, foldernames):
    """
    get data from VAR declaration of a struct datatype
    regex searching for:
        text between start and before " :"
        text between ": " and ";"
        text between "// " and end
    sample:  [Test : Struct   // comment Test] --> "Test", "Struct", "comment Test"
    collect data and save it in filedata
    """
    error = False
    errormessage = ""
    result = False
    regex = re.search(r'(.*) : (Struct)(?:\s{3}// )?(.*)?', rawdata[0])
    if regex is not None:
        result = True
        # first part of struct (declaration line)
        name, datatype, comment = clean_name(regex.group(1)), regex.group(2), regex.group(3)
        # get size of data
        size = special_types[datatype]
        # collect data
        entry = {
            "name": name,
            "datatype": datatype,
            "byte": 0.0,
            "comment": comment,
            "visible": True,
            "access": False,
            "action": "open",
            "value": "",
            "size": size}
        # save entry to list "data"
        save_entry(filedata=filedata, foldernames=foldernames, entry=entry)
        # append name prefix to list
        foldernames.append(name + ".")
        # delete line from rawdata
        rawdata.pop(0)
    return result, error, errormessage


def get_data_subudt(rawdata, filedata, foldernames, dependencies):
    """
    get data from VAR declaration of a sub-udt datatype (UDT in UDT)
    regex searching for text between quotation marks
    sample: [Test : "some_UDT";   // comment Test] --> "Test", "some_UDT", "comment Test"
    collect data and save it in filedata
    data: call the function where this function was called from --> get_structure()
    """
    error = False
    errormessage = ""
    result = False
    regex = re.search(r'(.*) : (.*);(?:\s{3}// )?(.*)?', rawdata[0])
    if regex is not None:
        result = True
        # ---------------------------------
        # first part of sub-udt (declaration line)
        name, datatype, comment = clean_name(regex.group(1)), regex.group(2), regex.group(3)
        # get size of data
        size = special_types["UDT"]
        # collect data
        entry = {
            "name": name,
            "datatype": datatype,
            "byte": 0.0,
            "comment": comment,
            "visible": True,
            "access": False,
            "action": "open",
            "value": "",
            "size": size}
        # save entry to list "data"
        save_entry(filedata=filedata, foldernames=foldernames, entry=entry)
        # append name prefix to list
        foldernames.append(name + ".")
        # ---------------------------------
        # middle part of sub-udt (data)
        path = dependencies[datatype]
        tempheaderdata, filedata, datasize, error, errormessage = get_structure(filedata=filedata,
                                                                                foldernames=foldernames,
                                                                                filepath=path,
                                                                                dependencies=dependencies)
        # ---------------------------------
        # delete name prefix from list
        foldernames.pop()
        # last part of sub-udt (end indicator)
        # get size of data
        size = special_types["UDT"]
        # collect data
        entry = {
            "name": "",
            "datatype": "END_UDT",
            "byte": 0.0,
            "comment": "",
            "visible": False,
            "access": False,
            "action": None,
            "value": "",
            "size": size}
        # save entry to list "data"
        save_entry(filedata=filedata, foldernames=[], entry=entry)
        # ---------------------------------
        # delete line from rawdata
        rawdata.pop(0)
    return result, error, errormessage


def get_header(rawdata, headerdata):
    # check line for header name
    get_header_name(rawdata=rawdata, headerdata=headerdata)
    # check line for header description
    get_header_description(rawdata=rawdata, headerdata=headerdata)
    # check line for header version
    get_header_version(rawdata=rawdata, headerdata=headerdata)
    # check line for header info
    get_header_info(rawdata=rawdata, headerdata=headerdata)
    # check line for header end
    headerend = get_header_end(rawdata=rawdata)
    return headerend, headerdata


def get_data(rawdata, filedata, foldernames, dependencies):
    error = False
    errormessage = ""
    dataend = False
    # get checking variables
    struct = is_struct(line=rawdata[0])
    endstruct = is_endstruct(line=rawdata[0])
    datatype = get_datatype(rawdata[0])
    subudt = is_udt(datatype=datatype)

    # check line for struct
    if struct:
        # get and save data to filedata
        result, error, errormessage = get_struct(rawdata=rawdata,
                                                 filedata=filedata,
                                                 foldernames=foldernames)
    # check line for endstruct
    elif endstruct:
        # get and save data to filedata
        result, error, errormessage = get_endstruct(rawdata=rawdata,
                                                    filedata=filedata,
                                                    foldernames=foldernames)
    # check line for standard datatype
    elif datatype in standard_types:
        # get and save data to filedata
        result, error, errormessage = get_data_standard(rawdata=rawdata,
                                                        filedata=filedata,
                                                        foldernames=foldernames)
    # check line for special datatype struct
    elif (datatype in special_types) and (datatype == "Array"):
        # get and save data to filedata
        result, error, errormessage = get_data_array(rawdata=rawdata,
                                                     filedata=filedata,
                                                     foldernames=foldernames,
                                                     dependencies=dependencies)
    # check line for special datatype string
    elif (datatype in special_types) and (datatype[:6] == "String"):
        # get and save data to filedata
        result, error, errormessage = get_data_string(rawdata=rawdata,
                                                      filedata=filedata,
                                                      foldernames=foldernames)
    # check line for special datatype wstring
    elif (datatype in special_types) and (datatype[:7] == "WString"):
        # get and save data to filedata
        result, error, errormessage = get_data_wstring(rawdata=rawdata,
                                                       filedata=filedata,
                                                       foldernames=foldernames)
    # check line for special datatype dtl
    elif (datatype in special_types) and (datatype == "DTL"):
        # get and save data to filedata
        result, error, errormessage = get_data_dtl(rawdata=rawdata,
                                                   filedata=filedata,
                                                   foldernames=foldernames)
    # check line for special datatype struct
    elif (datatype in special_types) and (datatype == "Struct"):
        # get and save data to filedata
        result, error, errormessage = get_data_struct(rawdata=rawdata,
                                                      filedata=filedata,
                                                      foldernames=foldernames)
    # check line for special datatype sub-udt
    elif subudt:
        # get and save data to filedata
        result, error, errormessage = get_data_subudt(rawdata=rawdata,
                                                      filedata=filedata,
                                                      foldernames=foldernames,
                                                      dependencies=dependencies)
    # check line for end of udt file
    elif is_endtype(rawdata=rawdata):
        # set end flag
        dataend = True
    else:
        error = True
        errormessage = "Dataerror: Line in File can not be interpreted: {line}".format(line=rawdata[0])
        # delete line from rawdata
        rawdata.pop(0)
    # check if rawdata is empty
    if not rawdata:
        # set end flag
        dataend = True
    return dataend, error, errormessage


def get_size(filedata):
    """
    get size of datastructure:
        count size of all entrys
        write byte address of entry
        check for needed offsets
        insert needed offsets
    needed offsets:
        compare datatype and following datatype:
         if datatype is bool and following is not bool:
          -insert 1 bit offset until size is integer (to get full byte size after bool type)
         if following datatype size is not 1 Byte:
          -insert 1 byte offset (to get an even byte size for following ">1 Byte types")
         if special flag in datatype ("END_STRUCT", "END_ARRAY", "END_DTL", "END_UDT"):
          -insert 1 byte offset (to get even byte size after this special type)
    """
    size = 0.0
    # temporary copy filedata
    datalist = filedata[:]
    filedata.clear()
    for index, data in enumerate(datalist):
        # save data
        if data["datatype"] == "Bool":
            data["byte"] = to_bitaddress(size)
        else:
            data["byte"] = size
        filedata.append(data)
        # count size
        size = size + float(data["size"])
        # check if next data exist
        try:
            next_data = datalist[index + 1]
        # end of data
        except IndexError:
            pass
        # next data exists
        else:
            # check if actual datatype != next datatype
            if data["datatype"] != next_data["datatype"]:
                # check if data is integer (full bytes)
                # fill with bool until byte is full
                while size % 1 != 0.0:
                    entry = {
                        "name": "offset",
                        "datatype": "Bool",
                        "byte": to_bitaddress(size),
                        "comment": "offset",
                        "visible": False,
                        "access": False,
                        "action": "offset",
                        "value": "",
                        "size": 0.125}
                    size = size + 0.125
                    save_entry(filedata=filedata, foldernames=[], entry=entry)
                # check if next data size is not 1 Byte
                if next_data["size"] != 1:
                    # check if size is even
                    # fill with Byte to make size even
                    if size % 2 != 0.0:
                        entry = {
                            "name": "offset",
                            "datatype": "Byte",
                            "byte": size,
                            "comment": "offset",
                            "visible": False,
                            "access": False,
                            "action": "offset",
                            "value": "",
                            "size": 1}
                        size = size + 1
                        save_entry(filedata=filedata, foldernames=[], entry=entry)
        # check if datatype is end of an special datatype
        if data["datatype"] in ["END_STRUCT", "END_ARRAY", "END_DTL", "END_UDT"]:
            # check if size is even
            # fill with Byte to make size even
            if size % 2 != 0.0:
                entry = {
                    "name": "offset",
                    "datatype": "Byte",
                    "byte": size,
                    "comment": "offset",
                    "visible": False,
                    "access": False,
                    "action": "offset",
                    "value": "",
                    "size": 1}
                size = size + 1
                save_entry(filedata=filedata, foldernames=[], entry=entry, saveposition="-1")
    return size


def get_structure(filedata=None, foldernames=None, filepath="", dependencies=None):
    """
    open udt file
    read every line of file and process the information to dict "headerdata" and list "filedata"
    """
    # initialise variables
    datasize = 0.0
    headerdata = {"name": "", "description": "", "version": "", "info": ""}
    if filedata is None:
        filedata = []
    if foldernames is None:
        foldernames = []
    if dependencies is None:
        dependencies = {}
    # read udt file
    rawdata = read_file(filepath)
    # read header data of rawdata until headerend is reached
    while True:
        headerend, headerdata = get_header(rawdata=rawdata, headerdata=headerdata)
        if headerend:
            break
    # read data of rawdata until dataend is reached
    while True:
        dataend, error, errormessage = get_data(rawdata=rawdata,
                                                filedata=filedata,
                                                foldernames=foldernames,
                                                dependencies=dependencies)
        if dataend or error:
            break
    # get udt size and fill offsets
    if not error:
        datasize = get_size(filedata=filedata)
    return headerdata, filedata, datasize, error, errormessage


def get_dependencies(path):
    """
    iterate trough udt file and find underlying udts
    """
    dependencies = {}
    udt = read_file(path)
    # get datatype for every line
    # check datatype for udt declaration
    # only check datatype to not get comments with "xxx" as udt declaration
    for line in udt:
        datatype = get_datatype(line)
        if datatype != "":
            # direct udt declaration
            if is_udt(datatype):
                dependencies[datatype] = None
            # udt declaration in array
            elif datatype == "Array":
                # get array datatype
                datatype = get_arraytype(line)
                if datatype != "":
                    if is_udt(datatype):
                        dependencies[datatype] = None
    return dependencies
