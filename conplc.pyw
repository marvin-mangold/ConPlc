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

import json
import view
import model


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

        # call model (handles the functions of GUI)
        self.model = model.Model()

    def run(self):
        # refresh variables on screen plc
        self.view.plc_update()
        # refresh variables on screen data
        self.view.datatree_update()
        # refresh variables on screen setup
        self.view.setup_update()
        # refresh windowsize and scaling
        self.view.window_update()
        # write eventmessage
        self.view.eventframe_post("Programm gestartet")
        # check if autorun is activated
        if self.projectfile["con_autorun"]:
            self.view.connect_state()
        # start mainloop
        self.view.window.mainloop()

    def stop(self):
        # write eventmessage
        self.view.eventframe_post("Programm gestoppt")
        # stop mainloop
        self.view.window.destroy()

    def file_new(self):
        # read JSON file
        with open("empty.cplc") as file:
            self.projectfile = json.load(file)
        # refresh variables on screen plc
        self.view.plc_update()
        # refresh variables on screen data
        self.view.datatree_update()
        # refresh variables on screen setup
        self.view.setup_update()
        # refresh windowsize and scaling
        self.view.window_update()
        # write eventmessage
        self.view.eventframe_post("Projekt geöffnet (neu)")

    def file_open(self, path=None):
        if path is None:
            path = self.view.filepath_open(filetypes=(("cplc Files", "*.cplc"),))
        # read JSON file
        with open(path) as file:
            self.projectfile = json.load(file)
        # refresh variables on screen plc
        self.view.plc_update()
        # refresh variables on screen data
        self.view.datatree_update()
        # refresh variables on screen setup
        self.view.setup_update()
        # refresh windowsize and scaling
        self.view.window_update()
        # write eventmessage
        self.view.eventframe_post("Projekt geöffnet ({path})".format(path=path))

    def file_save(self):
        # write JSON file
        with open('default.cplc', 'w', encoding='utf-8') as f:
            json.dump(self.projectfile, f, ensure_ascii=False, indent=4)
        # write eventmessage
        self.view.eventframe_post("Projekt gespeichert")

    def file_backup(self):
        path = self.view.filepath_saveas(filetypes=(("cplc Files", "*.cplc"),))
        # write JSON file
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.projectfile, f, ensure_ascii=False, indent=4)
        # write eventmessage
        self.view.eventframe_post("Projekt gespeichert ({path})".format(path=path))

    @staticmethod
    def read_time():
        return model.timestamp_get()

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
            dependencies = model.udt_dependencies_get(filepath)
            # get filepath of sub-UDTs
            for dep in dependencies:
                dependencies[dep] = self.view.filepath_open(message="select UDT: {dep}".format(dep=dep),
                                                            filetypes=(("UDT Files", "*.udt"),))
                if dependencies[dep] == "":
                    error = True
            if not error:
                # get data of main UDT and sub-UDTs
                name, description, version, info, data = model.udt_data_get(filepath, dependencies)
                self.projectfile["udt_name"] = name
                self.projectfile["udt_description"] = description
                self.projectfile["udt_version"] = version
                self.projectfile["udt_info"] = info
                self.projectfile["udt_data"] = data
                # refresh variables on screen data
                self.view.datatree_update()
                # write eventmessage
                self.view.eventframe_post("Datenstruktur eingelesen")
        if error:
            self.projectfile["udt_name"] = ""
            self.projectfile["udt_description"] = ""
            self.projectfile["udt_version"] = ""
            self.projectfile["udt_info"] = ""
            self.projectfile["udt_data"] = []
            # refresh variables on screen data
            self.view.datatree_update()

    def connection_run(self):
        # write eventmessage
        self.view.eventframe_post("Verbindung geöffnet")

    def connection_stop(self):
        # write eventmessage
        self.view.eventframe_post("Verbindung geschlossen")


if __name__ == '__main__':
    app = Controller()
    app.run()
