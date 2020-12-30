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

import view
import readudt
import tcpserver
import json
import time
import queue


class Controller(object):
    def __init__(self):
        # get configdata from configfile
        # Read JSON file
        with open("conplc.conf") as configfile:
            self.configfile = json.load(configfile)

        # get projectdata from projectfile
        # Read JSON file
        with open("default.cplc") as projectfile:
            self.projectfile = json.load(projectfile)

        # call view (handles the graphics of GUI)
        self.view = view.View(self)

        # call server (handles the tcp connection)
        self.server = tcpserver.Server()

    def run(self):
        # refresh variables on screen server
        self.view.server_update()
        # refresh variables on screen data
        self.view.datatree_update()
        # refresh variables on screen setup
        self.view.setup_update()
        # refresh windowsize and scaling
        self.view.window_update()
        # write eventmessage
        self.view.eventframe_post("Programm started")
        # check if autorun is activated
        if self.projectfile["con_autorun"]:
            self.view.cbx_playpause.invoke()
        # start parallel trigger
        self.view.window.after(0, self.trigger_100ms)
        # start mainloop
        self.view.window.mainloop()

    def stop(self):
        # write eventmessage
        self.view.eventframe_post("Programm stopped")
        # stop mainloop
        self.view.window.destroy()

    def trigger_100ms(self):
        # trigger every 250ms
        self.view.window.after(100, self.trigger_100ms)
        # get actual time and save it to variable
        self.view.timestamp.set(self.timestamp_get())
        # set led state
        self.led_state()
        # check for servermessage
        self.server_message()
        # check new serverdata
        self.server_data()

    def file_new(self):
        # read JSON file
        with open("empty.cplc") as file:
            self.projectfile = json.load(file)
        # refresh variables on screen server
        self.view.server_update()
        # refresh variables on screen data
        self.view.datatree_update()
        # refresh variables on screen setup
        self.view.setup_update()
        # refresh windowsize and scaling
        self.view.window_update()
        # write eventmessage
        self.view.eventframe_post("Project opened (new)")

    def file_open(self, path=None):
        if path is None:
            path = self.view.filepath_open(filetypes=(("cplc Files", "*.cplc"),))
        # read JSON file
        with open(path) as file:
            self.projectfile = json.load(file)
        # refresh variables on screen server
        self.view.server_update()
        # refresh variables on screen data
        self.view.datatree_update()
        # refresh variables on screen setup
        self.view.setup_update()
        # refresh windowsize and scaling
        self.view.window_update()
        # write eventmessage
        self.view.eventframe_post("Projekt opened ({path})".format(path=path))

    def file_save(self):
        # write JSON file
        with open('default.cplc', 'w', encoding='utf-8') as f:
            json.dump(self.projectfile, f, ensure_ascii=False, indent=4)
        # write eventmessage
        self.view.eventframe_post("Projekt saved")

    def file_backup(self):
        path = self.view.filepath_saveas(filetypes=(("cplc Files", "*.cplc"),))
        # write JSON file
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.projectfile, f, ensure_ascii=False, indent=4)
        # write eventmessage
        self.view.eventframe_post("Projekt saved ({path})".format(path=path))

    def data_get(self):
        error = False
        # clear data in datatree
        self.view.datatree_clear()
        # get filepath if main UDT
        filepath = self.view.filepath_open(message=None, filetypes=(("UDT Files", "*.udt"),))
        if filepath == "":
            error = True
        if not error:
            # check if UDT consists of sub-UDTs
            dependencies = readudt.get_udt_dependencies(filepath)
            # get filepath of sub-UDTs
            for dep in dependencies:
                dependencies[dep] = self.view.filepath_open(message="select UDT: {dep}".format(dep=dep),
                                                            filetypes=(("UDT Files", "*.udt"),))
                if dependencies[dep] == "":
                    error = True
            if not error:
                # get data of main UDT and sub-UDTs
                name, description, version, info, data = readudt.get_udt_data(filepath=filepath,
                                                                              dependencies=dependencies)
                self.projectfile["udt_name"] = name
                self.projectfile["udt_description"] = description
                self.projectfile["udt_version"] = version
                self.projectfile["udt_info"] = info
                self.projectfile["udt_data"] = data
                # refresh variables on screen data
                self.view.datatree_update()
                # write eventmessage
                self.view.eventframe_post("Datastructure loaded")
        if error:
            self.projectfile["udt_name"] = ""
            self.projectfile["udt_description"] = ""
            self.projectfile["udt_version"] = ""
            self.projectfile["udt_info"] = ""
            self.projectfile["udt_data"] = []
            # refresh variables on screen data
            self.view.datatree_update()

    def server_start(self):
        ip = "{byte1}.{byte2}.{byte3}.{byte4}".format(byte1=str(int(self.projectfile["con_ip_byte1"])),
                                                      byte2=str(int(self.projectfile["con_ip_byte2"])),
                                                      byte3=str(int(self.projectfile["con_ip_byte3"])),
                                                      byte4=str(int(self.projectfile["con_ip_byte4"])))
        port = int(self.projectfile["con_port"])
        self.server.start(ip=ip, port=port)

    def server_stop(self):
        self.server.stop()

    def server_message(self):
        try:
            event, message = self.server.buffer_message.get(block=False)
            # write eventmessage
            self.view.eventframe_post(message)
            if event == "stop":
                self.view.cbx_playpause.invoke()
        except queue.Empty:  # error if queue is empty
            pass

    def server_data(self):
        try:
            recv = self.server.buffer_recv.get(block=False)
            # write eventmessage
            message = "Server received data: {data}".format(data=recv)
            self.view.eventframe_post(message)
        except queue.Empty:  # error if queue is empty
            pass
        else:
            print("---")

    @staticmethod
    def timestamp_get():
        return time.strftime("%d.%m.%Y %H:%M:%S")

    def led_state(self):
        if not self.server.active:
            self.view.led_state("error")
        elif self.server.active and not self.server.connected:
            self.view.led_state("warn")
        elif self.server.active and self.server.connected:
            self.view.led_state("ok")


if __name__ == '__main__':
    app = Controller()
    app.run()
