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

import readudt
import time


class Model(object):
    def __init__(self):
        pass


def udt_data_get(filepath, dependencies):
    name, description, version, info, data = readudt.get_udt_data(
        filepath=filepath,
        dependencies=dependencies)
    return name, description, version, info, data


def udt_dependencies_get(filepath):
    return readudt.get_udt_dependencies(filepath)


def timestamp_get():
    return time.strftime("%d.%m.%Y %H:%M:%S")
