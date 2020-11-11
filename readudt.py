import re
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


def get_filepath(message=None):
    desktoppath = os.path.expanduser(r"~\Desktop")
    if message is not None:
        tk.messagebox.showinfo(title=None, message=message)
    path = tk.filedialog.askopenfilename(initialdir=desktoppath, title="UDT auswählen",
                                         filetypes=(("UDT Files", "*.udt"),))
    return path


def read_udt_file(path):
    udt = []
    with open(path, "r", encoding="utf-8") as udt_file:
        for line in udt_file:
            stripped = line.strip()
            if stripped != "":
                udt.append(stripped)
    return udt


def get_udt_name(line):
    # get Name of udt (must have string "TYPE ")
    # -->TYPE "udt Name"
    result = False
    name = ""
    regex = re.search(r'TYPE "(.*?)"', line)
    if regex is not None:
        result = True
        name = regex.group(1)
    return result, name


def get_udt_description(line):
    # get Description of udt (must have string "TITLE = ")
    # -->TITLE = udt with variables
    result = False
    description = ""
    regex = re.search(r'TITLE = (.*)', line)
    if regex is not None:
        result = True
        description = regex.group(1)
    return result, description


def get_udt_version(line):
    # get Version of udt (must have string "VERSION : ")
    # -->VERSION : 0.1
    result = False
    version = ""
    regex = re.search(r'VERSION : (.*)', line)
    if regex is not None:
        result = True
        version = regex.group(1)
    return result, version


def get_udt_info(line):
    # get Info of udt (string has to start with "//")
    # -->//Information about this udt
    result = False
    info = ""
    regex = re.search(r'^/{2}(.*)', line)
    if regex is not None:
        result = True
        info = regex.group(1)
    return result, info


def get_udt_headerend(line):
    # get last part of the header
    # -->STRUCT
    result = False
    regex = re.search(r'STRUCT', line)
    if regex is not None:
        result = True
    return result


def get_udt_datatype(line):
    # get VAR declaration datatype (must have ":")
    # -->name : Bool;   // comment
    result = False
    datatype = ""
    regex = re.search(r'(.*) : ([^;\/\[ ]*)', line)
    if regex is not None:
        result = True
        datatype = regex.group(2)
    return result, datatype


def clean_udt_varname(varname):
    # erase additional info in Varname (internal settings in {} brackets)
    # -->name {InstructionName := 'DTL'; LibVersion := '1.0'} : DTL;   // comment
    regex = re.search(r'(.*) {', varname)
    if regex is not None:
        varname = regex.group(1)
    return varname


def get_udt_struct(line, depth):
    # get Struct declaration (must have ":" and "Struct" and can have "// comment")
    # -->name : Struct   // comment
    result = False
    element = []
    regex = re.search(r'(.*) : (Struct)(?:   // )?(.*)?', line)
    if regex is not None:
        result = True
        name = clean_udt_varname(regex.group(1))
        datatype = regex.group(2)
        comment = regex.group(3)
        element = [depth, name, datatype, comment]
    return result, element


def get_udt_endstruct(line):
    # get end of Struct declaration (must have string "END_STRUCT;")
    # -->END_STRUCT;
    result = False
    regex = re.search(r'END_STRUCT;', line)
    if regex is not None:
        result = True
    return result 


def get_udt_var(line, depth):
    # get VAR declaration (must have ":" and can have "// comment")
    # -->name : Bool;   // comment
    result = False
    element = []
    regex = re.search(r'(.*) : (.*);(?:   // )?(.*)?', line)
    if regex is not None:
        result = True
        name = clean_udt_varname(regex.group(1))
        datatype = regex.group(2)
        comment = regex.group(3)
        element = [depth, name, datatype, comment]
    return result, element


def get_array_data(line):
    # -->Array[X..Y] of Datatype
    start = 0
    end = 0
    datatype = ""
    regex = re.search(r'(?:Array\[)(.*)(?:\.\.)(.*)(?:\] of )(.*);', line)
    if regex is not None:
        start = int(regex.group(1))
        end = int(regex.group(2)) + 1
        datatype = regex.group(3)
    return start, end, datatype


def element_is_udt(datatype):
    # check if element datatype is special udt type
    # -->"someName"
    result = False
    regex = re.search(r'"(.*)"', datatype)
    if regex is not None:
        result = True
    return result
    

def save_udt_element(data, depthname, element):
    # put prefix to varname
    varname = ""
    newelement = element[:]
    for prefix in depthname:
        varname += prefix
    newelement[1] = varname + newelement[1]
    # save element
    data.append(newelement)


def get_udt_data(data=None, structdepth=0, structdepthname=None):
    if data is None:
        data = []
    if structdepthname is None:
        structdepthname = []
    name = ""
    description = ""
    version = ""
    info = ""
    readheader = True
    # define possible Datatypes
    standard_types = ["Bool", "Byte", "Word", "DWord", "LWord", "SInt", "USInt",
                      "Int", "UInt", "DInt", "UDInt", "LInt", "ULInt", "Real",
                      "LReal", "Char", "WChar", "String", "WString"]
    special_types = ["DTL", "Array", "Struct"]
    # get path from udt-File
    message = "udt auswählen"
    if len(data) > 0:
        message = "udt {name} auswählen!".format(name=data[-1][2])
    path = get_filepath(message)
    # read Data from udt-File
    udt = read_udt_file(path)
    # analyse Data from udt-File
    for line in udt:
        # read header
        if readheader:
            # get udt name
            result, element = get_udt_name(line)
            if result:
                name = element
            # get udt description
            result, element = get_udt_description(line)
            if result:
                description = element
            # get udt version
            result, element = get_udt_version(line)
            if result:
                version = element
            # get udt info
            result, element = get_udt_info(line)
            if result:
                info = element
            # get udt header end
            result = get_udt_headerend(line)
            if result:
                readheader = False
                structdepthname.append("")
        # read data
        else:
            # get udt endstruct
            result = get_udt_endstruct(line)
            if result:
                structdepth -= 1
                structdepthname.pop()
            # check datatype of udt element
            result, datatype = get_udt_datatype(line)
            if result:
                # standard datatype
                if datatype in standard_types:
                    result, element = get_udt_var(line, structdepth)
                    if result:
                        save_udt_element(data, structdepthname, element)
                # special datatype
                elif datatype in special_types:
                    # get udt struct
                    if datatype == "Struct":
                        result, element = get_udt_struct(line, structdepth)
                        if result:
                            save_udt_element(data, structdepthname, element)
                            structdepth += 1
                            structdepthname.append(element[1]+".")
                    elif datatype == "DTL":
                        result, element = get_udt_var(line, structdepth)
                        if result:
                            save_udt_element(data, structdepthname, element)
                            structdepth += 1
                            structdepthname.append(element[1]+".")
                            save_udt_element(data, structdepthname, [structdepth, "YEAR", "UInt", "Year"])
                            save_udt_element(data, structdepthname, [structdepth, "MONTH", "USInt", "Month"])
                            save_udt_element(data, structdepthname, [structdepth, "DAY", "USInt", "Day"])
                            save_udt_element(data, structdepthname, [structdepth, "WEEKDAY", "USInt", "Weekday"])
                            save_udt_element(data, structdepthname, [structdepth, "HOUR", "USInt", "Hour"])
                            save_udt_element(data, structdepthname, [structdepth, "MINUTE", "USInt", "Minute"])
                            save_udt_element(data, structdepthname, [structdepth, "SECOND", "USInt", "Second"])
                            save_udt_element(data, structdepthname, [structdepth, "NANOSECOND", "UDint", "Nanosecond"])
                            structdepthname.pop()
                            structdepth -= 1
                    elif datatype == "Array":
                        result, element = get_udt_var(line, structdepth)
                        if result:
                            save_udt_element(data, structdepthname, element)
                            structdepth += 1
                            structdepthname.append(element[1])
                            start, end, datatype = get_array_data(line)
                            for entry in range(start, end):
                                save_udt_element(data, structdepthname,
                                                 [structdepth, "[" + str(entry) + "]", datatype, element[3]])
                            structdepthname.pop()
                            structdepth -= 1
                # special datatype udt type
                elif element_is_udt(datatype):
                    result, element = get_udt_var(line, structdepth)
                    if result:
                        save_udt_element(data, structdepthname, element)
                        structdepth += 1
                        structdepthname.append(element[1]+".")
                        _name, _description, _version, _info, data = get_udt_data(
                            data, structdepth, structdepthname)
                        structdepthname.pop()
                        structdepth -= 1
                else:
                    print("Datentyp {datatype} nicht implementiert!".format(datatype=datatype))
    return name, description, version, info, data
