import re
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os


def get_UDT_filepath(message):
    desktoppath = os.path.expanduser("~\Desktop")
    window = tk.Tk()
    window.withdraw()
    tk.messagebox.showinfo(title=None, message= message)
    path = filedialog.askopenfilename(initialdir= desktoppath, title= "UDT auswählen", filetypes= (("UDT Files","*.udt"),))
    return path
    
def read_UDT_file(path):
    UDT = []
    with open(path, 'r', encoding='utf-8') as UDT_file:
        for line in UDT_file:
            stripped = line.strip()
            if stripped != "":
                UDT.append(stripped)
    return UDT

def get_UDT_name(line):
    #get Name of UDT (must have string "TYPE ")
    #-->TYPE "UDT Name"
    result = False
    name = ""
    regex = re.search(r'TYPE "(.*?)"', line)
    if regex is not None:
        result = True
        name = regex.group(1)
    return result, name

def get_UDT_description(line):  
    #get Description of UDT (must have string "TITLE = ")
    #-->TITLE = UDT with variables
    result = False
    description = ""
    regex = re.search(r'TITLE = (.*)', line)
    if regex is not None:
        result = True
        description = regex.group(1)
    return result, description

def get_UDT_version(line):
    #get Version of UDT (must have string "VERSION : ")
    #-->VERSION : 0.1
    result = False
    version = ""
    regex = re.search(r'VERSION : (.*)', line)
    if regex is not None:
        result = True
        version = regex.group(1)
    return result, version

def get_UDT_info(line):
    #get Info of UDT (string has to start with "//")
    #-->//Information about this UDT
    result = False
    info = ""
    regex = re.search(r'^/{2}(.*)', line)
    if regex is not None:
        result = True
        info = regex.group(1)
    return result, info

def get_UDT_headerend(line):
    #get last part of the header
    #-->STRUCT
    result = False
    regex = re.search(r'STRUCT', line)
    if regex is not None:
        result = True
    return result

def get_UDT_datatype(line):
    #get VAR declaration datatype (must have ":")
    #-->name : Bool;   // comment
    result = False
    datatype = ""
    regex = re.search(r'(.*) : ([^;\/\[ ]*)', line)
    if regex is not None:
        result = True
        datatype = regex.group(2)
    return result, datatype

def clean_UDT_varname(varname):
    #erase additional info in Varname (internal settings in {} brackets)
    #-->name {InstructionName := 'DTL'; LibVersion := '1.0'} : DTL;   // comment
    regex = re.search(r'(.*) {', varname)
    if regex is not None:
        varname = regex.group(1)
    return varname

def get_UDT_struct(line, depth):
    #get Struct declaration (must have ":" and "Struct" and can have "// comment")
    #-->name : Struct   // comment
    result = False
    element = []
    regex = re.search(r'(.*) : (Struct)(?:   // )?(.*)?', line)
    if regex is not None:
        result = True
        name = clean_UDT_varname(regex.group(1))
        datatype = regex.group(2)
        comment = regex.group(3)
        element = [depth, name, datatype, comment]
    return result, element

def get_UDT_endstruct(line):
    #get end of Struct declaration (must have string "END_STRUCT;")
    #-->END_STRUCT;
    result = False
    regex = re.search(r'END_STRUCT;', line)
    if regex is not None:
        result = True
    return result 

def get_UDT_var(line, depth):
    #get VAR declaration (must have ":" and can have "// comment")
    #-->name : Bool;   // comment
    result = False
    element = []
    regex = re.search(r'(.*) : (.*);(?:   // )?(.*)?', line)
    if regex is not None:
        result = True
        name = regex.group(1)
        datatype = regex.group(2)
        comment = regex.group(3)
        name = clean_UDT_varname(regex.group(1))
        element = [depth, name, datatype, comment]
    return result, element

def get_Array_data(line):
    #-->Array[X..Y] of Datatype
    result = False
    element = []
    start = 0
    end = 0
    datatype = ""
    regex = re.search(r'(?:Array\[)(.*)(?:\.\.)(.*)(?:\] of )(.*);', line)
    if regex is not None:
        result = True
        start = int(regex.group(1))
        end = int(regex.group(2)) + 1
        datatype = regex.group(3)
    return start, end, datatype

def element_is_UDT(datatype):
    #check if element datatype is special UDT type
    #-->"someName"
    result = False
    regex = re.search(r'"(.*)"', datatype)
    if regex is not None:
        result = True
    return result
    
def save_UDT_element(data, depthname, element):
    #put prefix to varname
    varname = ""
    newelement = element[:]
    for prefix in depthname:
        varname += prefix
    newelement[1] = varname + newelement[1]
    #save element
    data.append(newelement)

def get_UDT_data(data = [], structdepth = 0, structdepthname = []):
    name = ""
    description = ""
    version = ""
    info = ""
    readheader = True
    #define possible Datatypes
    standard_types = ["Bool","Byte","Word","DWord","LWord","SInt","USInt",
                      "Int","UInt","DInt","UDInt","LInt","ULInt","Real",
                      "LReal","Char","WChar","String","WString"]
    special_types = ["DTL","Array","Struct"]
    #get path from UDT-File
    message = "UDT auswählen"
    if len(data) > 0: message = "UDT {name} auswählen!".format(name= data[-1][2])
    path = get_UDT_filepath(message)
    #read Data from UDT-File
    UDT = read_UDT_file(path)
    #analyse Data from UDT-File
    for line in UDT:
        #read header
        if readheader:
            #get UDT name
            result, element = get_UDT_name(line)
            if result: name = element
            #get UDT description
            result, element = get_UDT_description(line)
            if result: description = element            
            #get UDT version
            result, element = get_UDT_version(line)
            if result: version = element      
            #get UDT info
            result, element = get_UDT_info(line)
            if result: info = element
            #get UDT header end
            result = get_UDT_headerend(line)
            if result:
                readheader = False
                structdepthname.append("")
        #read data
        else:
            #get UDT endstruct
            result = get_UDT_endstruct(line)
            if result:
                structdepth -= 1
                structdepthname.pop()
            #check datatype of UDT element
            result, datatype = get_UDT_datatype(line)
            if result:
                #standard datatype
                if datatype in standard_types:
                    result, element = get_UDT_var(line, structdepth)
                    if result: save_UDT_element(data, structdepthname, element)
                #special datatype
                elif datatype in special_types:
                    #get UDT struct
                    if datatype == "Struct":
                        result, element = get_UDT_struct(line, structdepth)
                        if result:
                            save_UDT_element(data, structdepthname, element)
                            structdepth += 1
                            structdepthname.append(element[1]+".")
                    elif datatype == "DTL":
                        result, element = get_UDT_var(line, structdepth)
                        if result:
                            save_UDT_element(data, structdepthname, element)
                            structdepth += 1
                            structdepthname.append(element[1]+".")
                            save_UDT_element(data, structdepthname, [structdepth, "YEAR", "UInt", "Year"])
                            save_UDT_element(data, structdepthname, [structdepth, "MONTH", "USInt", "Month"])
                            save_UDT_element(data, structdepthname, [structdepth, "DAY", "USInt", "Day"])
                            save_UDT_element(data, structdepthname, [structdepth, "WEEKDAY", "USInt", "Weekday"])
                            save_UDT_element(data, structdepthname, [structdepth, "HOUR", "USInt", "Hour"])
                            save_UDT_element(data, structdepthname, [structdepth, "MINUTE", "USInt", "Minute"])
                            save_UDT_element(data, structdepthname, [structdepth, "SECOND", "USInt", "Second"])
                            save_UDT_element(data, structdepthname, [structdepth, "NANOSECOND", "UDint", "Nanosecond"])
                            structdepthname.pop()
                            structdepth -= 1
                    elif datatype == "Array":
                        result, element = get_UDT_var(line, structdepth)
                        if result:
                            save_UDT_element(data, structdepthname, element)
                            structdepth += 1
                            structdepthname.append(element[1])
                            start, end, datatype = get_Array_data(line)
                            for entry in range(start, end):
                                save_UDT_element(data, structdepthname, [structdepth, "[" + str(entry) + "]", datatype, element[3]])
                            structdepthname.pop()
                            structdepth -= 1
                #special datatype UDT type
                elif element_is_UDT(datatype):
                    result, element = get_UDT_var(line, structdepth)
                    if result:
                        save_UDT_element(data, structdepthname, element)
                        structdepth += 1
                        structdepthname.append(element[1]+".")
                        _name, _description, _version, _info, data = get_UDT_data(data, structdepth, structdepthname)
                        structdepthname.pop()
                        structdepth -= 1
                else:
                    print("Datentyp {datatype} nicht implementiert!".format(datatype= datatype))
    return name, description, version, info, data

            



#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------

Name, Description, Version, Info, Data = get_UDT_data()

#------Ausgabe-----------
print("Name = "+Name)
print("Beschreibung = "+Description)
print("Version = "+Version)
print("Info = "+Info)

for x in Data:
    print("{structdepth}{varname:20} | {vartype:25} | {varcomment}".format(structdepth= x[0]*"-",  varname= x[1], vartype= x[2] , varcomment= x[3]))
#------------------------
