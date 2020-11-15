import readudt
import time


class Model:
    def __init__(self):
        pass


def udt_data_get(filepath, dependencies):
    name, description, version, info, data = readudt.get_udt_data(
        filepath=filepath,
        dependencies=dependencies)
    return name, description, version, info, data


def udt_dependencies_get(filepath):
    return readudt.get_udt_dependencies(filepath)


def time_get():
    return time.strftime("%d.%m.%Y %H:%M:%S")
