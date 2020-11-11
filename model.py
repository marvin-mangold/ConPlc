import readudt
import time


class Model:
    def __init__(self, controller, config):
        self.controller = controller
        self.config = config
        self.time = ""
        self.udt_name = ""
        self.udt_description = ""
        self.udt_version = ""
        self.udt_info = ""
        self.udt_data = []

    def get_time(self):
        self.time = time.strftime("%d.%m.%Y %H:%M:%S")

    def get_udt_data(self):
        name, description, version, info, data = readudt.get_udt_data()
        self.udt_name = name
        self.udt_description = description
        self.udt_version = version
        self.udt_info = info
        self.udt_data = data

