"""
Wicke PLC - connect PLC and PC
Copyright (C) 2020  Marvin Mangold

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
        with open("wplc.conf") as configfile:
            self.configfile = json.load(configfile)
        # get default project from projectfile
        # Read JSON file
        with open("default.wplc") as projectfile:
            self.projectfile = json.load(projectfile)
        # call view (handles the graphics of GUI)
        self.view = view.View(self, self.configfile, self.projectfile)
        # call model (handles the functions of GUI)
        self.model = model.Model()

    def run(self):
        # refresh data
        self.view.datatree_update(self.projectfile)
        # initial trigger for 500ms loop
        self.view.window.after(0, self.trigger_500ms)
        # start window
        self.view.window.mainloop()

    def stop(self):
        # stop window
        self.view.window.destroy()

    def file_new(self):
        # read JSON file
        with open("empty.wplc") as file:
            self.projectfile = json.load(file)
        self.view.datatree_update(self.projectfile)
        self.view.window_title("empty.wplc")

    def file_open(self):
        path = self.view.filepath_open(filetypes=(("wplc Files", "*.wplc"),))
        # read JSON file
        with open(path) as file:
            self.projectfile = json.load(file)
        self.view.datatree_update(self.projectfile)
        self.view.window_title(path.split("/")[-1])

    def file_save(self):
        # write JSON file
        with open('default.wplc', 'w', encoding='utf-8') as f:
            json.dump(self.projectfile, f, ensure_ascii=False, indent=4)

    def file_saveas(self):
        path = self.view.filepath_saveas(filetypes=(("wplc Files", "*.wplc"),))
        # write JSON file
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.projectfile, f, ensure_ascii=False, indent=4)
        self.view.window_title(path.split("/")[-1])

    def trigger_500ms(self):
        # trigger every 500ms
        self.view.window.after(500, self.trigger_500ms)
        # get actual time and save it to variable
        self.view.timestamp.set(model.timestamp_get())
        self.view.led_state("error")

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
                self.view.datatree_update(self.projectfile)


if __name__ == '__main__':
    app = Controller()
    app.run()
