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


def get_bool(recvbytes, element):
    """
    read datatype from 1 byte
    FALSE or TRUE / 0 or 1
    """
    bit = int(element["byte"].split(".")[1])
    bitmask = 1 << bit
    data = str((recvbytes[0] & bitmask) != 0)
    element["value"] = data
    if bit == 7:
        recvbytes.pop(0)


def get_byte(recvbytes, element):
    """
    read datatype from 1 byte
    16#0 to 16#FF / 0 to 255
    """
    data = struct.unpack('!B', bytes([recvbytes[0]]))[0]
    data = format(data, '#01x')
    data = "16#{data}".format(data=data[2:]).upper()
    element["value"] = data
    recvbytes.pop(0)


def get_word(recvbytes, element):
    """
    read datatype from 2 byte
    16#0 to 16#FFFF / 0 to 65.535
    """
    data = struct.unpack('!H', bytes(recvbytes[0:2]))[0]
    data = format(data, '#04x')
    data = "16#{data}".format(data=data[2:]).upper()
    element["value"] = data
    recvbytes.pop(0)
    recvbytes.pop(0)


def get_dword(recvbytes, element):
    """
    read datatype from 4 byte
    16#0000_0000 to 16#FFFF_FFFF / 0 to 4.294.967.295
    """
    data = struct.unpack('!I', bytes(recvbytes[0:4]))[0]
    data = format(data, '#04x')
    data = "16#{data}".format(data=data[2:]).upper()
    element["value"] = data
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)


def get_lword(recvbytes, element):
    """
    read datatype from 8 byte
    16#0000_0000_0000_0000 to 16#FFFF_FFFF_FFFF_FFFF / 0 to 18.446.744.073.709.551.615
    """
    data = struct.unpack('!Q', bytes(recvbytes[0:8]))[0]
    data = format(data, '#08x')
    data = "16#{data}".format(data=data[2:]).upper()
    element["value"] = data
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)


def get_sint(recvbytes, element):
    """
    read datatype from 1 byte
    -128 to +127
    """
    data = str(struct.unpack('!b', bytes([recvbytes[0]]))[0])
    element["value"] = data
    recvbytes.pop(0)


def get_usint(recvbytes, element):
    """
    read datatype from 1 byte
    0 to 255
    """
    data = str(struct.unpack('!B', bytes([recvbytes[0]]))[0])
    element["value"] = data
    recvbytes.pop(0)


def get_int(recvbytes, element):
    """
    read datatype from 2 byte
    -32.768 to +32.767
    """
    data = str(struct.unpack('!h', bytes(recvbytes[0:2]))[0])
    element["value"] = data
    recvbytes.pop(0)
    recvbytes.pop(0)


def get_uint(recvbytes, element):
    """
    read datatype from 2 byte
    0 to 65.535
    """
    data = str(struct.unpack('!H', bytes(recvbytes[0:2]))[0])
    element["value"] = data
    recvbytes.pop(0)
    recvbytes.pop(0)


def get_dint(recvbytes, element):
    """
    read datatype from 4 byte
    -2.147.483.648 to +2.147.483.647
    """
    data = str(struct.unpack('!i', bytes(recvbytes[0:4]))[0])
    element["value"] = data
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)


def get_udint(recvbytes, element):
    """
    read datatype from 4 byte
    0 bis 4.294.967.295
    """
    data = str(struct.unpack('!I', bytes(recvbytes[0:4]))[0])
    element["value"] = data
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)


def get_lint(recvbytes, element):
    """
    read datatype from 8 byte
    -9.223.372.036.854.775.808 bis +9.223.372.036.854.775.807
    """
    data = str(struct.unpack('!q', bytes(recvbytes[0:8]))[0])
    element["value"] = data
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)


def get_ulint(recvbytes, element):
    """
    read datatype from 8 byte
    0 bis 18.446.744.073.709.551.615
    """
    data = str(struct.unpack('!Q', bytes(recvbytes[0:8]))[0])
    element["value"] = data
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)


def get_real(recvbytes, element):
    """
    read datatype from 4 byte
    -3.402823E+38 to -1.175495E-38
    ±0,0
    +1.175495E-38 to +3.402823E+38
    """
    data = str(struct.unpack('!f', bytes(recvbytes[0:4]))[0])
    element["value"] = data
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)


def get_lreal(recvbytes, element):
    """
    read datatype from 8 byte
    -1.7976931348623157e+308 to -2.2250738585072014e-308
    ±0,0
    +2.2250738585072014e-308 to +1.7976931348623157e+308
    """
    data = str(struct.unpack('!d', bytes(recvbytes[0:8]))[0])
    element["value"] = data
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)


def get_char(recvbytes, element):
    """
    read datatype from 1 byte
    ASCII-Character
    """
    data = str(chr(recvbytes[0]))
    element["value"] = data
    recvbytes.pop(0)


def get_wchar(recvbytes, element):
    """
    read datatype from 2 byte
    Unicode-Character
    """
    data = str(chr(struct.unpack('!h', bytes(recvbytes[0:2]))[0]))
    element["value"] = data
    recvbytes.pop(0)
    recvbytes.pop(0)


def get_string(recvbytes, element):
    """
    read datatype from max 256 byte
    first byte of string = maximal length of string
    second byte of string = actual length of string
    other bytes of string = ASCII-Characters (max 254 chars)
    """
    size = recvbytes[0]
    length = recvbytes[1]
    recvbytes.pop(0)
    recvbytes.pop(0)
    data = ""
    for char in range(length):
        data += str(chr(recvbytes[char]))
    element["value"] = data
    for byte in range(size):
        recvbytes.pop(0)


def get_wstring(recvbytes, element):
    """
    read datatype from max 32.768 byte
    first 2 byte of wstring = maximal length of wstring
    second 2 byte of wstring = actual length of wstring
    other bytes of wstring = Unicode-Characters (max 16382 wchars)
    """
    size = struct.unpack('!H', bytes(recvbytes[0:2]))[0]
    size = size * 2  # 10 wchars = 20 bytes
    length = struct.unpack('!H', bytes(recvbytes[2:4]))[0]
    length = length * 2  # 10 wchars = 20 bytes
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    recvbytes.pop(0)
    data = ""
    for wchar in range(0, length, 2):
        data += str(chr(struct.unpack('!h', bytes(recvbytes[wchar:wchar+2]))[0]))
    element["value"] = data
    for wchar in range(size):
        recvbytes.pop(0)


def get_plc_data(receivedbytes, datastructure):
    """
    for every data in datastructure read its values from receivedbytes
    """
    recvbytes = receivedbytes[:]
    for element in datastructure:
        datatype = element["datatype"]
        if datatype == "Bool":
            get_bool(recvbytes=recvbytes, element=element)
        elif datatype == "Byte":
            get_byte(recvbytes=recvbytes, element=element)
        elif datatype == "Word":
            get_word(recvbytes=recvbytes, element=element)
        elif datatype == "DWord":
            get_dword(recvbytes=recvbytes, element=element)
        elif datatype == "LWord":
            get_lword(recvbytes=recvbytes, element=element)
        elif datatype == "SInt":
            get_sint(recvbytes=recvbytes, element=element)
        elif datatype == "USInt":
            get_usint(recvbytes=recvbytes, element=element)
        elif datatype == "Int":
            get_int(recvbytes=recvbytes, element=element)
        elif datatype == "UInt":
            get_uint(recvbytes=recvbytes, element=element)
        elif datatype == "DInt":
            get_dint(recvbytes=recvbytes, element=element)
        elif datatype == "UDInt":
            get_udint(recvbytes=recvbytes, element=element)
        elif datatype == "LInt":
            get_lint(recvbytes=recvbytes, element=element)
        elif datatype == "ULInt":
            get_ulint(recvbytes=recvbytes, element=element)
        elif datatype == "Real":
            get_real(recvbytes=recvbytes, element=element)
        elif datatype == "LReal":
            get_lreal(recvbytes=recvbytes, element=element)
        elif datatype == "Char":
            get_char(recvbytes=recvbytes, element=element)
        elif datatype == "WChar":
            get_wchar(recvbytes=recvbytes, element=element)
        elif datatype[:6] == "String":
            get_string(recvbytes=recvbytes, element=element)
        elif datatype[:7] == "WString":
            get_wstring(recvbytes=recvbytes, element=element)
        else:
            pass
