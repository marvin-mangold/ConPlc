import readudt
import time


class Model:
    def __init__(self):
        pass


def get_udt_data(filepath, dependencies):
    name, description, version, info, data = readudt.get_udt_data(
        filepath=filepath,
        dependencies=dependencies)
    return name, description, version, info, data


def get_udt_dependencies(filepath):
    return readudt.get_udt_dependencies(filepath)


def get_time():
    return time.strftime("%d.%m.%Y %H:%M:%S")
