import json
import view
import model


class Controller:
    def __init__(self):
        # get configdata from configfile
        # Read JSON file
        with open("wplc.conf") as file:
            self.config = json.load(file)
        # get default parameters from file
        # Read JSON file
        with open("default.wplc") as file:
            self.parameter = json.load(file)
        # call view (handles the graphics of GUI)
        self.view = view.View(self, self.config, self.parameter)
        # call model (handles the functions of GUI)
        self.model = model.Model()
        # ---------------------------------------------------------------------
        # connect view and controller (Buttons, Events, Functions)
        # call scale function when windowsize gets changed
        self.view.window.bind(
            "<Configure>", lambda x: self.window_scale())
        # call stop when exit button is pressed
        self.view.btn_exit.bind(
            "<ButtonRelease>", lambda x: self.stop())
        # call import datastructure when button is pressed
        self.view.btn_import_datasructure.bind(
            "<ButtonRelease>", lambda x: self.datastructure_get())

    def run(self):
        # refresh data
        self.data_refresh()
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
            self.parameter = json.load(file)
        self.data_refresh()

    def file_open(self):
        path = self.view.filepath_open(filetypes=(("wplc Files", "*.wplc"),))
        # read JSON file
        with open(path) as file:
            self.parameter = json.load(file)
        self.data_refresh()

    def file_save(self):
        # write JSON file
        with open('default.wplc', 'w', encoding='utf-8') as f:
            json.dump(self.parameter, f, ensure_ascii=False, indent=4)

    def file_saveas(self):
        path = self.view.filepath_saveas(filetypes=(("wplc Files", "*.wplc"),))
        # write JSON file
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.parameter, f, ensure_ascii=False, indent=4)

    def data_refresh(self):
        self.view.parameter = self.parameter
        self.datastructure_refresh()

    def trigger_500ms(self):
        # trigger every 500ms
        self.view.window.after(500, self.trigger_500ms)
        # get actual time and save it to variable
        self.view.timestamp.set(model.time_get())

    def window_scale(self):
        width, height = self.view.window_scale()
        if not self.parameter["opt_fullscreen"]:
            self.parameter["opt_windowwidth"] = width
            self.parameter["opt_windowheight"] = height

    def window_fullscreen(self):
        self.parameter["opt_fullscreen"] = self.view.opt_fullscreen.get()
        self.view.window_size()

    def datastructure_get(self):
        dependencies = {}
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
                # get datastructure of main UDT and sub-UDTs
                name, description, version, info, data = model.udt_data_get(filepath, dependencies)
                self.parameter["udt_name"] = name
                self.parameter["udt_description"] = description
                self.parameter["udt_version"] = version
                self.parameter["udt_info"] = info
                self.parameter["udt_data"] = data
                self.datastructure_refresh()

    def datastructure_refresh(self):
        name = self.parameter["udt_name"]
        description = self.parameter["udt_description"]
        version = self.parameter["udt_version"]
        info = self.parameter["udt_info"]
        data = self.parameter["udt_data"]
        # clear data in datatree
        self.view.datatree_clear()
        # fill data in datatree
        self.view.datatree_fill(name, description, version, info, data)


if __name__ == '__main__':
    app = Controller()
    app.run()
