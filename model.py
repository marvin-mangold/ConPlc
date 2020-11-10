import readudt
import time


class Model:
    def __init__(self, controller, config):
        self.controller = controller
        self.config = config
        self.time = ""
        self.data_name = ""
        self.data_description = ""
        self.data_version = ""
        self.data_info = ""
        self.data_data = []

    def get_time(self):
        self.time = time.strftime("%d.%m.%Y %H:%M:%S")
