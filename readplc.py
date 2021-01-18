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
import struct

testdata = [1, 143, 0, 2, 0, 0, 0, 3, 64, 128, 0, 0, 254, 10, 116, 101, 115, 116, 115, 116, 114, 105, 110, 103, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def get_bool(recvbytes, element):
    bit = int(element["byte"].split(".")[1])
    bitmask = 1 << bit
    data = (recvbytes[0] & bitmask) != 0
    element["value"] = data
    if bit == 7:
        recvbytes.pop(0)


def get_byte(recvbytes, element):
    data = str(recvbytes[0])
    element["value"] = data
    recvbytes.pop(0)


def get_word(recvbytes, element):
    pass


def get_dword(recvbytes, element):
    pass


def get_lword(recvbytes, element):
    pass


def get_sint(recvbytes, element):
    pass


def get_usint(recvbytes, element):
    pass


def get_int(recvbytes, element):
    firstbyte = recvbytes[0]
    firstbyte = firstbyte.to_bytes(1, "big")
    secondbyte = recvbytes[1]
    secondbyte = secondbyte.to_bytes(1, "big")
    data = int.from_bytes((firstbyte + secondbyte), "big")
    element["value"] = data
    recvbytes.pop(0)
    recvbytes.pop(0)


def get_uint(recvbytes, element):
    pass


def get_dint(recvbytes, element):
    firstbyte = recvbytes[0]
    firstbyte = firstbyte.to_bytes(1, "big")
    secondbyte = recvbytes[1]
    secondbyte = secondbyte.to_bytes(1, "big")
    thirdbyte = recvbytes[2]
    thirdbyte = thirdbyte.to_bytes(1, "big")
    fourthbyte = recvbytes[3]
    fourthbyte = fourthbyte.to_bytes(1, "big")
    data = int.from_bytes((firstbyte + secondbyte + thirdbyte + fourthbyte), "big")
    element["value"] = data
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)


def get_udint(recvbytes, element):
    pass


def get_lint(recvbytes, element):
    pass


def get_ulint(recvbytes, element):
    pass


def get_char(recvbytes, element):
    pass


def get_wchar(recvbytes, element):
    pass


def get_string(recvbytes, element):
    pass


def get_wstring(recvbytes, element):
    pass


def get_plc_data(receivedbytes, datastructure):
    recvbytes = testdata[:] #receivedbytes[:]
    for element in datastructure:
        datatype = element["datatype"]
        if datatype == "Bool":
            get_bool(recvbytes=recvbytes, element=element)
        elif datatype == "Byte":
            get_byte(recvbytes=recvbytes, element=element)
        elif datatype == "Word":
            pass  # TODO
        elif datatype == "DWord":
            pass  # TODO
        elif datatype == "LWord":
            pass  # TODO
        elif datatype == "SInt":
            pass  # TODO
        elif datatype == "USInt":
            pass  # TODO
        elif datatype == "Int":
            get_int(recvbytes=recvbytes, element=element)
        elif datatype == "UInt":
            pass  # TODO
        elif datatype == "DInt":
            get_dint(recvbytes=recvbytes, element=element)
        elif datatype == "UDInt":
            pass  # TODO
        elif datatype == "LInt":
            pass  # TODO
        elif datatype == "ULInt":
            pass  # TODO
        elif datatype == "Char":
            pass  # TODO
        elif datatype == "WChar":
            pass  # TODO
        elif datatype == "String":
            pass  # TODO
        elif datatype == "WString":
            pass  # TODO
        else:
            pass
    for x in datastructure:
       print(x)
