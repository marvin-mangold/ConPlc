"""
ConPlc - connect PLC and PC
Copyright (C) 2021  Marvin Mangold (Marvin.Mangold00@googlemail.com)

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
import readplc
import tcpserver
import csvhandler
import json
import time
import queue

# TODO check if win 7
# TODO PLC Blocks s7 and TIA

class Controller(object):
    def __init__(self):
        """
        open configuration file
        open default project file
        create instance of gui
        create instance of server
        """
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

        # call csv handler
        self.csv = csvhandler.CSV()

    def run(self):
        """
        start mainloop of programm
        """
        # refresh variables on screen server
        self.view.server_update()
        # refresh variables on screen data
        self.view.datatree_update()
        # refresh variables on screen setup
        self.view.setup_update()
        # refresh variables on screen csv
        self.view.csv_update()
        # refresh windowsize and scaling
        self.view.window_update()
        # write eventmessage
        self.view.eventframe_post("Programm started")
        # check if autostart is activated
        if self.projectfile["con_autostart"]:
            self.view.cbx_runstop.invoke()
        # start parallel trigger
        self.view.window.after(0, self.trigger_100ms)
        # start mainloop
        self.view.window.mainloop()

    def stop(self):
        """
        stop mainloop of programm
        """
        # write eventmessage
        self.view.eventframe_post("Programm stopped")
        # stop mainloop
        self.view.window.destroy()

    def trigger_100ms(self):
        """
        trigger self every 100ms
        read timestamp
        change led state
        check for messages from server
        check for received data from server
        """
        # trigger every 100ms
        self.view.window.after(100, self.trigger_100ms)
        # get actual time and save it to variable
        self.view.timestamp.set(self.timestamp_get())
        # set led state
        self.led_state()
        # check for servermessage
        self.server_message()
        # check new serverdata
        self.server_data()
        # check if csv needs to me saved
        self.csv_save()

    def file_new(self):
        """
        open empty project file
        update screens with new data
        """
        # read JSON file
        with open("empty.cplc") as file:
            self.projectfile = json.load(file)
        # refresh variables on screen server
        self.view.server_update()
        # refresh variables on screen data
        self.view.datatree_update()
        # refresh variables on screen setup
        self.view.setup_update()
        # refresh variables on screen csv
        self.view.csv_update()
        # refresh windowsize and scaling
        self.view.window_update()
        # write eventmessage
        self.view.eventframe_post("Project opened (new)")

    def file_open(self, path=None):
        """
        choose project file
        open project file
        update screens with new data
        """
        if path is None:
            path = self.view.filepath_open(filetypes=(("cplc Files", "*.cplc"),))
        if path != "":
            # read JSON file
            with open(path) as file:
                self.projectfile = json.load(file)
            # refresh variables on screen server
            self.view.server_update()
            # refresh variables on screen data
            self.view.datatree_update()
            # refresh variables on screen setup
            self.view.setup_update()
            # refresh variables on screen csv
            self.view.csv_update()
            # refresh windowsize and scaling
            self.view.window_update()
            # write eventmessage
            self.view.eventframe_post("Project opened ({path})".format(path=path))

    def file_save(self):
        """
        save project file to default
        """
        # write JSON file
        with open('default.cplc', 'w', encoding='utf-8') as f:
            json.dump(self.projectfile, f, ensure_ascii=False, indent=4)
        # write eventmessage
        self.view.eventframe_post("Project saved")

    def file_backup(self):
        """
        choose saving filepath of actual project file
        save project file on filepath
        """
        path = self.view.filepath_saveas(filetypes=(("cplc Files", "*.cplc"),))
        if path != "":
            # write JSON file
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.projectfile, f, ensure_ascii=False, indent=4)
            # write eventmessage
            self.view.eventframe_post("Project saved ({path})".format(path=path))

    def data_get(self):
        """
        choose filepath of udt file
        check udt file for underlying udt declarations and choose their filepath
        read contents of udt file
        update screens with new data
        """
        error = False
        errormessage = ""
        # stop server if server is running
        if self.view.runstop.get():
            self.view.cbx_runstop.invoke()
        # clear data in datatree
        self.view.datatree_clear()
        # get the filepath of udt and its sub udts
        # create empty dict for dependencies
        dependencies = {"Source": None}  # {"sub_udt_name":"sub_udt_filepath", ...}
        # loop until all entries in dictionary "dependencies" are filled with filepath
        # in every loop search for sub udts in udt
        # if sub udt found, add it to dependencies so the loop will run again
        while (not error) and list(filter(lambda x: dependencies[x] is None, dependencies)):
            # if udt with filepath = None found in dependencies, get its filepath
            dep = list(filter(lambda x: dependencies[x] is None, dependencies))
            message = "select UDT: {dep}".format(dep=dep[0])
            filepath = self.view.filepath_open(message=message, filetypes=(("UDT Files", "*.udt"),))
            if filepath == "":  # filedialog got wrong path or was closed --> break loop
                error = True
                errormessage = "Dataerror: File not found"
                break
            else:
                # save filepath to dependencies
                dependencies[dep[0]] = filepath
                # search in udt for sub udts and save them to dictionary to dependencies
                dependencies.update(readudt.get_dependencies(filepath))
        # get datastructure of the udt
        if not error:
            # get data of main UDT and sub-UDTs
            headerdata, filedata, datasize, error, errormessage = readudt.get_structure(filepath=dependencies["Source"],
                                                                                        dependencies=dependencies)
            if not error:
                self.projectfile["udt_name"] = headerdata["name"]
                self.projectfile["udt_description"] = headerdata["description"]
                self.projectfile["udt_version"] = headerdata["version"]
                self.projectfile["udt_info"] = headerdata["info"]
                self.projectfile["udt_datasize"] = str(datasize)
                self.projectfile["udt_datastructure"] = filedata
                # refresh variables on screen data
                self.view.datatree_update()
                # write eventmessage
                self.view.eventframe_post("Datastructure loaded")
        if error:
            self.projectfile["udt_name"] = ""
            self.projectfile["udt_description"] = ""
            self.projectfile["udt_version"] = ""
            self.projectfile["udt_info"] = ""
            self.projectfile["udt_datasize"] = "0"
            self.projectfile["udt_datastructure"] = []
            # refresh variables on screen data
            self.view.datatree_update()
            self.view.eventframe_post(errormessage)
        # reset csv data
        self.projectfile["csv_booltrigger"] = 0
        self.view.csv_rowdata = [{"Text": "", "Variable": 0}]
        self.projectfile["csv_rowdata"] = self.view.csv_rowdata.copy()
        self.view.csv_update()
        self.view.csv_row.set(1)
        self.view.csv_numrows.set(len(self.view.csv_rowdata))

    def server_start(self):
        """
        start server
        """
        ip = "{byte1}.{byte2}.{byte3}.{byte4}".format(byte1=str(int(self.projectfile["con_ip_byte1"])),
                                                      byte2=str(int(self.projectfile["con_ip_byte2"])),
                                                      byte3=str(int(self.projectfile["con_ip_byte3"])),
                                                      byte4=str(int(self.projectfile["con_ip_byte4"])))
        port = int(self.projectfile["con_port"])
        datasize = int(float(self.projectfile["udt_datasize"]))
        self.server.start(ip=ip, port=port, datasize=datasize)

    def server_stop(self):
        """
        stop server
        """
        self.server.stop()

    def server_message(self):
        """
        check for messages from server and post them
        """
        try:
            event, message = self.server.buffer_message.get(block=False)
            # write eventmessage
            self.view.eventframe_post(message)
            if event == "stop":
                self.view.cbx_runstop.invoke()
        except queue.Empty:  # error if queue is empty
            pass

    def server_data(self):
        """
        check for new data from server
        process data
        write answer to server
        """
        try:  # try to get data from recvbuffer
            recv = self.server.buffer_recv.get(block=False)
        except queue.Empty:  # error if recvbuffer is empty
            pass
        else:  # data from recvbuffer taken
            # convert received bytestring to list of integer
            receivedbytes = list(recv)
            # write eventmessage
            message = "Server received data"
            if self.projectfile["con_show_recvdata"]:
                message = "{msg}: {data}".format(msg=message, data=receivedbytes)
            self.view.eventframe_post(message)
            # work with received data
            readplc.get_plc_data(receivedbytes=receivedbytes, datastructure=self.projectfile["udt_datastructure"])
            # update the values in datatree with the new received data
            self.view.datatree_values_set()
            # convert list of integer to bytestring
            # TODO answer length to long, timeout when sending
            sendbytes = bytes(receivedbytes)
            # put data back in sendbuffer
            self.server.buffer_send.put(sendbytes)

    @staticmethod
    def timestamp_get():
        """
        get actual timestamp from clock
        """
        return time.strftime("%d.%m.%Y %H:%M:%S")

    def led_state(self):
        """
        change led state depending on the server state
        """
        if not self.server.active:
            self.view.led_state("error")
        elif self.server.active and not self.server.connected:
            self.view.led_state("warn")
        elif self.server.active and self.server.connected:
            self.view.led_state("ok")

    def csv_save(self):
        """
        exchange data with csv-handler
        """
        message = None
        data = self.projectfile["udt_datastructure"]
        self.csv.active = self.projectfile["csv_active"]
        self.csv.filename = self.projectfile["csv_filename"]
        self.csv.filepath = self.projectfile["csv_filepath"]
        self.csv.filemode = self.projectfile["csv_filemode"]
        self.csv.triggermode = self.projectfile["csv_triggermode"]
        self.csv.time = self.projectfile["csv_time"]
        self.csv.delimiter = self.projectfile["csv_delimiter"]
        # refresh csv header and data
        self.csv.header = []
        self.csv.data = []
        if len(data) > 0:
            for element in self.projectfile["csv_rowdata"]:
                self.csv.header.append(element["Text"])
                index = element["Variable"]
                self.csv.data.append(data[index]["value"])
        # set csv trigger from boolean variable
        if self.csv.triggermode == "boolean" and self.projectfile["csv_booltrigger"] > 0:
            index = self.projectfile["csv_booltrigger"]
            state = data[index]["value"].lower() == "true"
            self.csv.trigger = state
        # check if csv should run
        if self.csv.active and self.server.active and self.server.connected and not self.view.csv_timechange:
            message = self.csv.trigger_check()
        else:
            self.csv.trigger_reset()
            self.view.csv_timechange = False
        nexttrigger = time.strftime("%H:%M:%S", time.localtime(self.csv.nexttrigger))
        nexttrigger = "{text}: {next}".format(text="next Trigger", next=nexttrigger)
        self.view.csv_nexttrigger.set(nexttrigger)
        if message is not None:
            # write eventmessage
            self.view.eventframe_post(message)


if __name__ == '__main__':
    app = Controller()
    app.run()
