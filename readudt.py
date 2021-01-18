"""
ConPlc - connect PLC and PC
Copyright (C) 2020  Marvin Mangold (marvin@mangoldx.de)

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

import re


# define possible Datatypes and its bit-size
datatypes = {"Bool": 0.125,
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
             "WChar": 2,
             "String": 2,
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


def entry_save(filedata, foldernames, entry, saveposition="end"):
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


def name_clean(name):
    """
    erase additional info in Varname (internal settings in {} brackets)
    sample: [Test {InstructionName := 'DTL'; LibVersion := '1.0'} : DTL;   // comment Test] --> "Test"
    """
    newname = name
    regex = re.search(r'(.*) {', name)
    if regex is not None:
        newname = regex.group(1)
    return newname


def is_udt(line=""):
    """
    check if datatype is special udt type
    regex searching for text between quotation marks
    sample: [Test : "some_UDT";   // comment Test] --> "some_UDT"
    """
    result = False
    regex = re.search(r'"(.*)"', line)
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


def is_endudt(line=""):
    """
    get udt-file end indicator
    regex searching for text "END_TYPE"
    sample: [END_TYPE] --> "END_TYPE"
    """
    result = False
    regex = re.search(r'END_TYPE', line)
    if regex is not None:
        result = True
    return result


def formatbit_save_to_show(size=0.0):
    """
    input float, return string
    bits are saved as 0.125 Bytes
    bits are shown as 0.1 Bytes
    save form: the byteaddress of 8 bits are saved as 10.0 - 10.875
    show form: the byteaddress of 8 bits are shown as 10.0 - 10.7
    format save form to show form
    sample: 10.875 --> 10.7
    """
    size = "{x:.3f}".format(x=size)
    size = size.split(".")  # ["10", "875"]
    size[1] = str(int(int(size[1]) / 125))  # 875 / 125 = 7
    bitaddress = "{predecimalplace}.{decimalplace}".format(predecimalplace=size[0], decimalplace=size[1])
    return bitaddress  # 10.7


def formatbit_show_to_save(size):
    """
    input string, return float
    bits are saved as 0.125 Bytes
    bits are shown as 0.1 Bytes
    save form: the byteaddress of 8 bits are saved as 10.0 - 10.875
    show form: the byteaddress of 8 bits are shown as 10.0 - 10.7
    format show form to save form
    sample: 10.7 --> 10.875
    """
    size = size.split(".")  # ["10", "7"]
    size[1] = str(int(size[1]) * 125)  # 7 * 125 = 875
    bitaddress = "{predecimalplace}.{decimalplace}".format(predecimalplace=size[0], decimalplace=size[1])
    return float(bitaddress)  # 10.875


def get_address(filedata):
    """
    look at last entry in filedata and calculate actual address:
    add size of last data to address of last data
    keep format at 10.0 - 10.7 even if a bool (0.125 byte) is added
    """
    if len(filedata) == 0:
        address = "0.0"
    else:
        address = formatbit_show_to_save(filedata[-1]["byte"])  # format "10.7" to 10.875
        address = filedata[-1]["size"] + address  # 10.875 + 0.125
        address = formatbit_save_to_show(address)  # format 11.000 to "11.0"
    return address


def get_offset(datatype, filedata):
    """
    look at last entry in filedata and insert offset if needed:
    if (actual type is not bool) and (last one was bool) and (actual address is not integer ("X.7")):
        insert boolean offsets until actual address is X.0 (to get a full byte address after bool type)
    if actual datatype has an even size but actual address is odd:
        insert byte offset to make address even
    """
    if len(filedata) == 0:
        pass
    else:
        # ----------------------------------------------------------
        # get full byte address after bool type
        if datatype != "Bool" and filedata[-1]["datatype"] == "Bool":
            # if actual address is not ".0" then insert 1 bool offset
            while ".0" not in get_address(filedata=filedata):
                entry = {
                    "name": "offset",
                    "datatype": "Bool",
                    "byte": get_address(filedata=filedata),
                    "comment": "offset",
                    "visible": False,
                    "access": False,
                    "action": "offset",
                    "value": "",
                    "size": 0.125}
                entry_save(filedata=filedata, foldernames=[], entry=entry)
        # ----------------------------------------------------------
        # get even byte address for datatypes where size is an even integer
        # get dict of all datatype where a even address is needed
        even_types = dict(filter(lambda x: (x[1] % 2 == 0), datatypes.items()))
        # check if actual data size is not 1 byte
        if datatype in even_types:
            # if actual address is not even then insert 1 byte offset
            if int(float(get_address(filedata=filedata))) % 2 != 0:
                entry = {
                    "name": "offset",
                    "datatype": "Byte",
                    "byte": get_address(filedata=filedata),
                    "comment": "offset",
                    "visible": False,
                    "access": False,
                    "action": "offset",
                    "value": "",
                    "size": 1}
                entry_save(filedata=filedata, foldernames=[], entry=entry)


def get_datatype(line=""):
    """
    get datatype from VAR declaration datatype
    regex searching for text between ": " and "whitespace or any other symbol except letters"
    sample:  [Test : Bool;   // comment Test] --> "Bool"
    """
    datatype = ""
    regex = re.search(r'(.*) : (.*?)(;|$|\s{3}|\[| :=)', line)
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
    regex = re.search(r'(.*) of (.*);', line)
    if regex is not None:
        datatype = regex.group(2)
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
        get_offset(datatype="START_STRUCT", filedata=filedata)
        address = get_address(filedata=filedata)
        entry = {
            "name": "",
            "datatype": "START_STRUCT",
            "byte": address,
            "comment": "",
            "visible": False,
            "access": False,
            "action": None,
            "value": "",
            "size": 0}
        # save entry to list "data"
        entry_save(filedata=filedata, foldernames=[], entry=entry)
        # append name prefix to list
        foldernames.append("")
        # delete line from rawdata
        rawdata.pop(0)
    return result, error, errormessage


def get_endstruct(rawdata, filedata, foldernames):
    """
    get end of struct declaration
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
        get_offset(datatype="END_STRUCT", filedata=filedata)
        address = get_address(filedata=filedata)
        entry = {
            "name": "",
            "datatype": "END_STRUCT",
            "byte": address,
            "comment": "",
            "visible": False,
            "access": False,
            "action": "close",
            "value": "",
            "size": 0}
        # save entry to list "data"
        entry_save(filedata=filedata, foldernames=[], entry=entry)
        # delete line from rawdata
        rawdata.pop(0)
    return result, error, errormessage


def get_endudt(rawdata, filedata, foldernames):
    """
    get end of udt declaration
    regex searching for text "END_STRUCT;"
    sample: [END_STRUCT;] --> "END_STRUCT;"
    collect data and save it in filedata
    """
    error = False
    errormessage = ""
    result = False
    regex = re.search(r'END_TYPE', rawdata[0])
    if regex is not None:
        result = True
        try:
            # delete name prefix from list
            foldernames.pop()
        except IndexError:
            pass
        # last part of struct (end indicator)
        # collect data
        get_offset(datatype="END_UDT", filedata=filedata)
        address = get_address(filedata=filedata)
        entry = {
            "name": "",
            "datatype": "END_UDT",
            "byte": address,
            "comment": "",
            "visible": False,
            "access": False,
            "action": None,
            "value": "",
            "size": 0}
        # save entry to list "data"
        entry_save(filedata=filedata, foldernames=[], entry=entry)
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
    sample:  [Test : Bool := False;   // comment Test] --> "Test", "Bool", "comment Test"
    collect data and save it in filedata
    """
    error = False
    errormessage = ""
    result = False
    regex = re.search(r'(.*) : (.*?)(?: :=.*?)?;(?:\s{3}// )?(.*)', rawdata[0])
    if regex is not None:
        result = True
        name, datatype, comment = name_clean(regex.group(1)), regex.group(2), regex.group(3)
        # get size of data
        size = datatypes[datatype]
        # collect data
        get_offset(datatype=datatype, filedata=filedata)
        address = get_address(filedata=filedata)
        entry = {
            "name": name,
            "datatype": datatype,
            "byte": address,
            "comment": comment,
            "visible": True,
            "access": True,
            "action": None,
            "value": "",
            "size": size}
        # save entry to list "data"
        entry_save(filedata=filedata, foldernames=foldernames, entry=entry)
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
    sample:  [Test : String[10] := 'test';   // comment Test] --> "Test", "String", "10", "comment Test"
    sample:  [Test : String := 'test';   // comment Test] --> "Test", "String", None, "comment Test"
    if datatype = String without [xxx] --> set it to String[254] after regex
    collect data and save it in filedata
    """
    error = False
    errormessage = ""
    result = False
    regex = re.search(r'(.*) : (.*?)(?:\[(.*?)?])?(?: :=.*?)?;(?:\s{3}// )?(.*)?', rawdata[0])
    if regex is not None:
        result = True
        name, datatype, length, comment = name_clean(regex.group(1)), regex.group(2), regex.group(3), regex.group(4)
        if length is not None:
            length = int(length)
        else:
            length = 254
        # get size of data
        # first Byte of String = maximal length of String
        # second Byte of String = actual length of String
        size_decalration = datatypes["String"]
        size_data = datatypes["Char"] * length  # size of data = count of chars * bit-size of a char
        size = size_decalration + size_data
        # collect data
        get_offset(datatype=datatype, filedata=filedata)
        address = get_address(filedata=filedata)
        entry = {
            "name": name,
            "datatype": "{datatype}[{length}]".format(datatype=datatype, length=length),
            "byte": address,
            "comment": comment,
            "visible": True,
            "access": True,
            "action": None,
            "value": "",
            "size": size}
        # save entry to list "data"
        entry_save(filedata=filedata, foldernames=foldernames, entry=entry)
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
    sample:  [Test : WString[10] := 'test';   // comment Test] --> "Test", "WString", "10", "comment Test"
    sample:  [Test : WString := 'test';   // comment Test] --> "Test", "WString", None, "comment Test"
    if datatype = WString without [xxx] --> set it to WString[254] after regex
    collect data and save it in filedata
    """
    error = False
    errormessage = ""
    result = False
    regex = re.search(r'(.*) : (.*?)(?:\[(.*?)?])?(?: :=.*?)?;(?:\s{3}// )?(.*)?', rawdata[0])
    if regex is not None:
        result = True
        name, datatype, length, comment = name_clean(regex.group(1)), regex.group(2), regex.group(3), regex.group(4)
        if length is not None:
            length = int(length)
        else:
            length = 254
        # get size of data
        # first Word of WString = maximal length of WString
        # second Word of WString = actual length of WString
        size_decalration = datatypes["WString"]
        size_data = datatypes["WChar"] * length  # size of data = count of wchars * bit-size of a wchar
        size = size_decalration + size_data
        # collect data
        get_offset(datatype=datatype, filedata=filedata)
        address = get_address(filedata=filedata)
        entry = {
            "name": name,
            "datatype": "{datatype}[{length}]".format(datatype=datatype, length=length),
            "byte": address,
            "comment": comment,
            "visible": True,
            "access": True,
            "action": None,
            "value": "",
            "size": size}
        # save entry to list "data"
        entry_save(filedata=filedata, foldernames=foldernames, entry=entry)
        # delete line from rawdata
        rawdata.pop(0)
    return result, error, errormessage


def get_dimension(dimensiondata, dimension=None, dimensionnames=None, data=None, addbefore="", addafter=""):
    """
    get list of all elements of an multidimensional array
    Array: "Array[0..5, 0..2, 1..3] of Bool"
    takes dimensiondata: [{'start': 0, 'end': 5}, {'start': 0, 'end': 2}, {'start': 1, 'end': 3}]
    adds a special marker after all elements in the deepest dimension are processed
    can append an additional string before data and after data
    returns als combination as list:
        ...         with additional
        "Marker"        -->       "START_DIMENSION"
        "[0,0,1]"       -->       "addbefore [0,0,1]" addafter
        "[0,0,2]"       -->       "addbefore [0,0,2]" addafter
        "[0,0,3]"       -->       "addbefore [0,0,3]" addafter
        "Marker"          -->     "END_DIMENSION"
        "Marker"        -->       "START_DIMENSION"
        "[0,1,1]"       -->       "addbefore [0,1,1]" addafter
        "[0,1,2]"       -->       "addbefore [0,1,2]" addafter
        "[0,1,3]"       -->       "addbefore [0,1,3]" addafter
        "Marker"          -->     "END_DIMENSION"
        "Marker"        -->       "START_DIMENSION"
        "[0,2,1]"       -->       "addbefore [0,2,1]" addafter
        "[0,2,2]"       -->       "addbefore [0,2,2]" addafter
        "[0,2,3]"       -->       "addbefore [0,2,3]" addafter
        "Marker"          -->     "END_DIMENSION"
        "Marker"        -->       "START_DIMENSION"
        "[1,0,1]"       -->       "addbefore [1,0,1]" addafter
        "[1,0,2]"       -->       "addbefore [1,0,2]" addafter
        "[1,0,3]"       -->       "addbefore [1,0,3]" addafter
        "Marker"          -->     "END_DIMENSION"
        "Marker"        -->       "START_DIMENSION"
        "[1,1,1]"       -->       "addbefore [1,1,1]" addafter
        "[1,1,2]"       -->       "addbefore [1,1,2]" addafter
        "[1,1,3]"       -->       "addbefore [1,1,3]" addafter
        "Marker"          -->     "END_DIMENSION"
        ....
    """
    # initialise variables if this is the first call
    if data is None:
        data = []
    if dimension is None:
        dimension = 0
    if dimensionnames is None:
        dimensionnames = [""]
    # get start and end parameters of array in actual dimension
    start = dimensiondata[dimension]["start"]
    end = dimensiondata[dimension]["end"]
    # if the deepest dimension is processes insert a marker
    if dimension == len(dimensiondata) - 1:
        data.append("START_DIMENSION")
    # check if "save data" or "go one dimension deeper"
    for step in range(start, end + 1):
        # change actual dimensionname in name list
        dimensionnames[-1] = str(step)
        # check if this is the deepest dimension
        # not deepest dimension --> go one dimension deeper
        if dimension < len(dimensiondata)-1:
            nextdimension = dimension + 1
            # save next dimensionname in name list
            dimensionnames.append(str(nextdimension))
            # function calls itself to go one dimension deeper
            get_dimension(dimensiondata=dimensiondata,
                          dimension=nextdimension,
                          dimensionnames=dimensionnames,
                          data=data,
                          addbefore=addbefore,
                          addafter=addafter)
            # delete last dimensionname from name list
            dimensionnames.pop()
        # deepest dimension --> save data in datalist
        else:
            # concat dimension names
            actualname = ",".join(dimensionnames)
            actualname = "[{actualname}]".format(actualname=actualname)
            savename = addbefore + actualname + addafter
            # save to data
            data.append(savename)
    # if the deepest dimension is processes insert a marker
    if dimension == len(dimensiondata)-1:
        data.append("END_DIMENSION")
    return data


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
    regex = re.search(r'(.*?) : ((.*)\[(.*)] of (.*));(?:\s{3}// )?(.*)?', rawdata[0])
    if regex is not None:
        # ---------------------------------
        # insert start marker array
        # collect data
        get_offset(datatype="START_ARRAY", filedata=filedata)
        address = get_address(filedata=filedata)
        entry = {
            "name": "",
            "datatype": "START_ARRAY",
            "byte": address,
            "comment": "",
            "visible": False,
            "access": False,
            "action": None,
            "value": "",
            "size": 0}
        # save entry to list "data"
        entry_save(filedata=filedata, foldernames=[], entry=entry)
        # ---------------------------------
        name = name_clean(regex.group(1))  # "Test"
        arraydescription = regex.group(2)  # "Array[1..8, 0..10] of Byte"
        datatype = regex.group(3)  # "Array"
        dimensions = regex.group(4).split(",")  # 1..8, 0..10
        arraydatatype = regex.group(5)  # "Byte"
        comment = regex.group(6)  # "// comment Test"
        # first part of array (declaration line)
        # get size of data
        size = datatypes[datatype]
        # collect data
        get_offset(datatype=datatype, filedata=filedata)
        address = get_address(filedata=filedata)
        entry = {
            "name": name,
            "datatype": arraydescription,
            "byte": address,
            "comment": comment,
            "visible": True,
            "access": False,
            "action": "open",
            "value": "",
            "size": size}
        # save entry to list "data"
        entry_save(filedata=filedata, foldernames=foldernames, entry=entry)
        # append name prefix to list
        foldernames.append(name + ".")
        # ---------------------------------
        # middle part of array (data)
        # create dict with dimension count and bounds [{"start": 1, "end": 8}, {"start": 0, "end": 10}]
        dimensiondata = []
        for dimension in dimensions:
            dimensionbounds = dimension.split(".")
            dimensiondata.append({"start": int(dimensionbounds[0]), "end": int(dimensionbounds[2])})
        # create list of entrys in range arraysize
        addition = " : {datatype};".format(datatype=arraydatatype)
        elements = get_dimension(dimensiondata=dimensiondata, addafter=addition)
        # get data of all elements
        for element in elements:
            if element == "START_DIMENSION":
                # ---------------------------------
                # insert start marker dimension
                # collect data
                get_offset(datatype="START_DIMENSION", filedata=filedata)
                address = get_address(filedata=filedata)
                entry = {
                    "name": "",
                    "datatype": "START_DIMENSION",
                    "byte": address,
                    "comment": "",
                    "visible": False,
                    "access": False,
                    "action": None,
                    "value": "",
                    "size": 0}
                # save entry to list "data"
                entry_save(filedata=filedata, foldernames=[], entry=entry)
            elif element == "END_DIMENSION":
                # ---------------------------------
                # insert end marker dimension
                # collect data
                get_offset(datatype="END_DIMENSION", filedata=filedata)
                address = get_address(filedata=filedata)
                entry = {
                    "name": "",
                    "datatype": "END_DIMENSION",
                    "byte": address,
                    "comment": "",
                    "visible": False,
                    "access": False,
                    "action": None,
                    "value": "",
                    "size": 0}
                # save entry to list "data"
                entry_save(filedata=filedata, foldernames=[], entry=entry)
            else:
                dataend, error, errormessage = get_data(rawdata=[element],
                                                        filedata=filedata,
                                                        foldernames=foldernames,
                                                        dependencies=dependencies)
        # ---------------------------------
        # delete name prefix from list
        foldernames.pop()
        # ---------------------------------
        # insert end marker array
        # collect data
        get_offset(datatype="END_ARRAY", filedata=filedata)
        address = get_address(filedata=filedata)
        entry = {
            "name": "",
            "datatype": "END_ARRAY",
            "byte": address,
            "comment": "",
            "visible": False,
            "access": False,
            "action": "close",
            "value": "",
            "size": 0}
        # save entry to list "data"
        entry_save(filedata=filedata, foldernames=[], entry=entry)
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
    regex = re.search(r'(.*) : (.*?)(?: :=.*?)?;(?:\s{3}// )?(.*)?', rawdata[0])
    if regex is not None:
        result = True
        # ---------------------------------
        # insert start marker dtl
        # collect data
        get_offset(datatype="START_DTL", filedata=filedata)
        address = get_address(filedata=filedata)
        entry = {
            "name": "",
            "datatype": "START_DTL",
            "byte": address,
            "comment": "",
            "visible": False,
            "access": False,
            "action": None,
            "value": "",
            "size": 0}
        # save entry to list "data"
        entry_save(filedata=filedata, foldernames=[], entry=entry)
        # ---------------------------------
        # first part of dtl (declaration line)
        name, datatype, comment = name_clean(regex.group(1)), regex.group(2), regex.group(3)
        # get size of data
        size = datatypes[datatype]
        # collect data
        get_offset(datatype=datatype, filedata=filedata)
        address = get_address(filedata=filedata)
        entry = {
            "name": name,
            "datatype": datatype,
            "byte": address,
            "comment": comment,
            "visible": True,
            "access": False,
            "action": "open",
            "value": "",
            "size": size}
        # save entry to list "data"
        entry_save(filedata=filedata, foldernames=foldernames, entry=entry)
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
            size = datatypes[datatype]
            # collect data
            get_offset(datatype=datatype, filedata=filedata)
            address = get_address(filedata=filedata)
            entry = {
                "name": name,
                "datatype": datatype,
                "byte": address,
                "comment": comment,
                "visible": True,
                "access": True,
                "action": None,
                "value": "",
                "size": size}
            # save entry to list "data"
            entry_save(filedata=filedata, foldernames=foldernames, entry=entry)
        # ---------------------------------
        # delete name prefix from list
        foldernames.pop()
        # ---------------------------------
        # insert end marker dtl
        # collect data
        get_offset(datatype="END_DTL", filedata=filedata)
        address = get_address(filedata=filedata)
        entry = {
            "name": "",
            "datatype": "END_DTL",
            "byte": address,
            "comment": "",
            "visible": False,
            "access": False,
            "action": "close",
            "value": "",
            "size": 0}
        # save entry to list "data"
        entry_save(filedata=filedata, foldernames=[], entry=entry)
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
        # ---------------------------------
        # insert start marker struct in get_struct() because it has an extra line in raw data
        # ---------------------------------
        # first part of struct (declaration line)
        name, datatype, comment = name_clean(regex.group(1)), regex.group(2), regex.group(3)
        # get size of data
        size = datatypes[datatype]
        # collect data
        get_offset(datatype=datatype, filedata=filedata)
        address = get_address(filedata=filedata)
        entry = {
            "name": name,
            "datatype": datatype,
            "byte": address,
            "comment": comment,
            "visible": True,
            "access": False,
            "action": "open",
            "value": "",
            "size": size}
        # save entry to list "data"
        entry_save(filedata=filedata, foldernames=foldernames, entry=entry)
        # ---------------------------------
        # append name prefix to list
        foldernames.append(name + ".")
        # ---------------------------------
        # insert end marker struct in get_endstruct() because it has an extra line in raw data
        # ---------------------------------
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
        # insert end marker subudt
        # collect data
        get_offset(datatype="START_UDT", filedata=filedata)
        address = get_address(filedata=filedata)
        entry = {
            "name": "",
            "datatype": "START_UDT",
            "byte": address,
            "comment": "",
            "visible": False,
            "access": False,
            "action": None,
            "value": "",
            "size": 0}
        # save entry to list "data"
        entry_save(filedata=filedata, foldernames=[], entry=entry)
        # ---------------------------------
        # first part of sub-udt (declaration line)
        name, datatype, comment = name_clean(regex.group(1)), regex.group(2), regex.group(3)
        # get size of data
        size = datatypes["UDT"]
        # collect data
        get_offset(datatype="UDT", filedata=filedata)
        address = get_address(filedata=filedata)
        entry = {
            "name": name,
            "datatype": datatype,
            "byte": address,
            "comment": comment,
            "visible": True,
            "access": False,
            "action": "open",
            "value": "",
            "size": size}
        # save entry to list "data"
        entry_save(filedata=filedata, foldernames=foldernames, entry=entry)
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
        # insert end marker udt in get_endstruct() because it has an extra line in raw data
        # insert end marker udt in get_endudt() because it has an extra line in raw data
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
    dataend = False
    # get checking variables
    struct = is_struct(line=rawdata[0])
    endstruct = is_endstruct(line=rawdata[0])
    datatype = get_datatype(rawdata[0])
    udt = is_udt(line=datatype)
    endudt = is_endudt(line=rawdata[0])
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
    elif datatype in ["Bool", "Byte", "Word", "DWord", "LWord", "SInt", "USInt", "Int", "UInt",
                      "DInt", "UDInt", "LInt", "ULInt", "Real", "LReal", "Char", "WChar"]:
        # get and save data to filedata
        result, error, errormessage = get_data_standard(rawdata=rawdata,
                                                        filedata=filedata,
                                                        foldernames=foldernames)
    # check line for special datatype struct
    elif datatype == "Array":
        # get and save data to filedata
        result, error, errormessage = get_data_array(rawdata=rawdata,
                                                     filedata=filedata,
                                                     foldernames=foldernames,
                                                     dependencies=dependencies)
    # check line for special datatype string
    elif datatype[:6] == "String":
        # get and save data to filedata
        result, error, errormessage = get_data_string(rawdata=rawdata,
                                                      filedata=filedata,
                                                      foldernames=foldernames)
    # check line for special datatype wstring
    elif datatype[:7] == "WString":
        # get and save data to filedata
        result, error, errormessage = get_data_wstring(rawdata=rawdata,
                                                       filedata=filedata,
                                                       foldernames=foldernames)
    # check line for special datatype dtl
    elif datatype == "DTL":
        # get and save data to filedata
        result, error, errormessage = get_data_dtl(rawdata=rawdata,
                                                   filedata=filedata,
                                                   foldernames=foldernames)
    # check line for special datatype struct
    elif datatype == "Struct":
        # get and save data to filedata
        result, error, errormessage = get_data_struct(rawdata=rawdata,
                                                      filedata=filedata,
                                                      foldernames=foldernames)
    # check line for special datatype sub-udt
    elif udt:
        # get and save data to filedata
        result, error, errormessage = get_data_subudt(rawdata=rawdata,
                                                      filedata=filedata,
                                                      foldernames=foldernames,
                                                      dependencies=dependencies)
    # check line for end of udt file
    elif endudt:
        # get and save data to filedata
        result, error, errormessage = get_endudt(rawdata=rawdata,
                                                 filedata=filedata,
                                                 foldernames=foldernames)
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


def get_structure(filedata=None, foldernames=None, filepath="", dependencies=None):
    """
    open udt file
    read every line of file and process the information to dict "headerdata" and list "filedata"
    """
    # initialise variables
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
    # datasize has to be even
    datasize = filedata[-1]["byte"]
    if int(float(datasize)) % 2 != 0:
        datasize = str(float(datasize) + 1.0)

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
