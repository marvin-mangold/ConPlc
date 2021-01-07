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

import re, time


# define possible Datatypes and its bit-size
standard_types = {"Bool": 1,
                  "Byte": 8,
                  "Word": 16,
                  "DWord": 32,
                  "LWord": 64,
                  "SInt": 8,
                  "USInt": 8,
                  "Int": 16,
                  "UInt": 16,
                  "DInt": 32,
                  "UDInt": 32,
                  "LInt": 64,
                  "ULInt": 64,
                  "Real": 32,
                  "LReal": 64,
                  "Char": 8,
                  "WChar": 16}

special_types = {"String": 16,
                 "WString": 32,
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


def save_entry(filedata, foldernames, entry):
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
    filedata.append(newentry)


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


def get_datatype(line=""):
    """
    get datatype from VAR declaration datatype
    regex searching for text between ": " and "whitespace or any other symbol except letters"
    sample:  [Test : Bool;   // comment Test] --> "Bool"
    """
    datatype = ""
    regex = re.search(r'(.*) : ([^;/\[ ]*)', line)
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
    regex = re.search(r'STRUCT', rawdata[0])
    if regex is not None:
        result = True
        # delete line from rawdata
        rawdata.pop(0)
    return result


def get_data_endstruct(rawdata, filedata, foldernames):
    """
    get end of Struct declaration
    regex searching for text "END_STRUCT;"
    sample: [END_STRUCT;] --> "END_STRUCT;"
    collect data and save it in filedata
    """
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
            "datatype": "",
            "comment": "",
            "visible": False,
            "access": False,
            "action": "close",
            "value": "",
            "size": 0}
        # save entry to list "data"
        save_entry(filedata=filedata, foldernames=foldernames, entry=entry)
        # delete line from rawdata
        rawdata.pop(0)
    return result


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
            "comment": comment,
            "visible": True,
            "access": True,
            "action": "none",
            "value": "",
            "size": size}
        # save entry to list "data"
        save_entry(filedata=filedata, foldernames=foldernames, entry=entry)
        # delete line from rawdata
        rawdata.pop(0)
    return result


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
            "comment": comment,
            "visible": True,
            "access": True,
            "action": "none",
            "value": "",
            "size": size}
        # save entry to list "data"
        save_entry(filedata=filedata, foldernames=foldernames, entry=entry)
        # delete line from rawdata
        rawdata.pop(0)
    return result


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
            "comment": comment,
            "visible": True,
            "access": True,
            "action": "none",
            "value": "",
            "size": size}
        # save entry to list "data"
        save_entry(filedata=filedata, foldernames=foldernames, entry=entry)
        # delete line from rawdata
        rawdata.pop(0)
    return result


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
                "comment": comment,
                "visible": True,
                "access": True,
                "action": "none",
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
            "datatype": "",
            "comment": "",
            "visible": False,
            "access": False,
            "action": "close",
            "value": "",
            "size": size}
        # save entry to list "data"
        save_entry(filedata=filedata, foldernames=foldernames, entry=entry)
        # ---------------------------------
        # delete line from rawdata
        rawdata.pop(0)
    return result


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
    return result


def get_data_subudt(rawdata, filedata, foldernames, dependencies):
    """
    get data from VAR declaration of a sub-udt datatype (UDT in UDT)
    regex searching for text between quotation marks
    sample: [Test : "some_UDT";   // comment Test] --> "Test", "some_UDT", "comment Test"
    collect data and save it in filedata
    data: call the function where this function was called from --> get_structure()
    """
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
        tempheaderdata, filedata = get_structure(filedata=filedata, foldernames=foldernames,
                                                 filepath=path, dependencies=dependencies)
        # ---------------------------------
        # delete name prefix from list
        foldernames.pop()
        # last part of sub-udt (end indicator)
        # get size of data
        size = special_types["UDT"]
        # collect data
        entry = {
            "name": "",
            "datatype": "",
            "comment": "",
            "visible": False,
            "access": False,
            "action": "close",
            "value": "",
            "size": size}
        # save entry to list "data"
        save_entry(filedata=filedata, foldernames=foldernames, entry=entry)
        # ---------------------------------
        # delete line from rawdata
        rawdata.pop(0)
    return result


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
    dataend = False
    # get checking variables
    endstruct = is_endstruct(line=rawdata[0])
    datatype = get_datatype(rawdata[0])
    subudt = is_udt(datatype=datatype)
    # check line for endstruct
    if endstruct:
        # get and save data to filedata
        get_data_endstruct(rawdata=rawdata, filedata=filedata, foldernames=foldernames)
    # check line for standard datatype
    elif datatype in standard_types:
        # get and save data to filedata
        get_data_standard(rawdata=rawdata, filedata=filedata, foldernames=foldernames)
    # check line for special datatype string
    elif (datatype in special_types) and (datatype[:6] == "String"):
        # get and save data to filedata
        get_data_string(rawdata=rawdata, filedata=filedata, foldernames=foldernames)
    # check line for special datatype wstring
    elif (datatype in special_types) and (datatype[:7] == "WString"):
        # get and save data to filedata
        get_data_wstring(rawdata=rawdata, filedata=filedata, foldernames=foldernames)
    # check line for special datatype dtl
    elif (datatype in special_types) and (datatype == "DTL"):
        # get and save data to filedata
        get_data_dtl(rawdata=rawdata, filedata=filedata, foldernames=foldernames)
    # check line for special datatype struct
    elif (datatype in special_types) and (datatype == "Struct"):
        # get and save data to filedata
        get_data_struct(rawdata=rawdata, filedata=filedata, foldernames=foldernames)
    # check line for special datatype sub-udt
    elif subudt:
        # get and save data to filedata
        get_data_subudt(rawdata=rawdata, filedata=filedata, foldernames=foldernames, dependencies=dependencies)
    # check line for end of udt file
    elif is_endtype(rawdata=rawdata):
        # set end flag
        dataend = True
    else:
        print("Line can not be interpreted: {line}".format(line=rawdata[0]))
        # delete line from rawdata
        rawdata.pop(0)
    return dataend


def get_structure(filedata=None, foldernames=None, filepath="", dependencies=None):
    """
    open udt file
    read every line of file and process the information to dict "headerdata" and list "filedata"
    """
    # initialise variables
    headerdata = {"name": "", "description": "", "version": "", "info": "", "size": "0"}
    if filedata is None:
        filedata = []
    if foldernames is None:
        foldernames = []
    foldernames.append("")
    if dependencies is None:
        dependencies = {}
    # read udt file
    rawdata = read_file(filepath)
    # read header data of rawdata as long as the flag is true
    while True:
        headerend, headerdata = get_header(rawdata=rawdata, headerdata=headerdata)
        if headerend:
            break
    # read data of rawdata as long as data in rawdata
    while True:
        dataend = get_data(rawdata=rawdata, filedata=filedata, foldernames=foldernames, dependencies=dependencies)
        if dataend:
            break
    return headerdata, filedata


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
