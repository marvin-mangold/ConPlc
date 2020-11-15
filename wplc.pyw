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
        self.view = view.View(self, self.config)
        # call model (handles the functions of GUI)
        self.model = model.Model(self, self.config)
        # ---------------------------------------------------------------------
        # connect view and model and controller (Buttons, Events, Functions)
        # call scale function when windowsize gets changed
        self.view.window.bind(
            "<Configure>", lambda x: self.view.scale())
        self.view.btn_exit.bind(
            "<ButtonRelease>", lambda x: self.stop())
        self.view.btn_import_datasructure.bind(
            "<ButtonRelease>", lambda x: self.import_datastructure())

    def run(self):
        # refresh data
        self.refresh()
        # initial trigger for 500ms loop
        self.view.window.after(0, self.trigger_500ms)
        # start window
        self.view.window.mainloop()

    def stop(self):
        # stop window
        self.view.window.destroy()

    def new_file(self):
        # read JSON file
        with open("empty.wplc") as file:
            self.parameter = json.load(file)
        self.refresh()

    def open_file(self):
        path = self.view.get_open_filepath(filetypes=(("wplc Files", "*.wplc"),))
        # read JSON file
        with open(path) as file:
            self.parameter = json.load(file)
        self.refresh()

    def save_file(self):
        # write JSON file
        with open('default.wplc', 'w', encoding='utf-8') as f:
            json.dump(self.parameter, f, ensure_ascii=False, indent=4)

    def save_as_file(self):
        path = self.view.get_save_as_filepath(filetypes=(("wplc Files", "*.wplc"),))
        path = path + ".wplc"
        # write JSON file
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.parameter, f, ensure_ascii=False, indent=4)

    def refresh(self):
        self.refresh_datastructure()

    def trigger_500ms(self):
        # trigger every 500ms
        self.view.window.after(500, self.trigger_500ms)
        # get actual time and save it to variable
        self.view.timestamp.set(model.get_time())

    def import_datastructure(self):
        dependencies = {}
        error = False
        # clear data in datatree
        self.view.clear_datatree()
        # get filepath if main UDT
        filepath = self.view.get_open_filepath(message=None, filetypes=(("UDT Files", "*.udt"),))
        if filepath == "":
            error = True
        if not error:
            # check if UDT consists of sub-UDTs
            dependencies = model.get_udt_dependencies(filepath)
            # get filepath of sub-UDTs
            for dep in dependencies:
                dependencies[dep] = self.view.get_open_filepath(message="select UDT: {dep}".format(dep=dep),
                                                                filetypes=(("UDT Files", "*.udt"),))
                if dependencies[dep] == "":
                    error = True
            if not error:
                # get datastructure of main UDT and sub-UDTs
                name, description, version, info, data = model.get_udt_data(filepath, dependencies)
                self.parameter["udt_name"] = name
                self.parameter["udt_description"] = description
                self.parameter["udt_version"] = version
                self.parameter["udt_info"] = info
                self.parameter["udt_data"] = data
                self.refresh_datastructure()

    def refresh_datastructure(self):
        name = self.parameter["udt_name"]
        description = self.parameter["udt_description"]
        version = self.parameter["udt_version"]
        info = self.parameter["udt_info"]
        data = self.parameter["udt_data"]
        # clear data in datatree
        self.view.clear_datatree()
        # fill data in datatree
        self.view.fill_datatree(name, description, version, info, data)


if __name__ == '__main__':
    app = Controller()
    app.run()
