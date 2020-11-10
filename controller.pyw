import confighandler
import view
import model


class Controller:
    def __init__(self):
        # get Configdata from Configfile
        self.config = confighandler.readconfig("config.wplc")
        # call view (handles the graphics of GUI)
        self.view = view.View(self, self.config)
        # call model (handles the functions of GUI)
        self.model = model.Model(self, self.config)
        # ---------------------------------------------------------------------
        # connect view and model and controller (Buttons, Events, Functions)
        # call scale function when windowsize gets changed
        self.view.windowframe.bind(
            "<Configure>", lambda x: self.view.scale())
        self.view.btn_home.bind(
            "<ButtonRelease>", lambda x: self.view.screen_change("ScreenStart"))
        self.view.btn_plc.bind(
            "<ButtonRelease>", lambda x: self.view.screen_change("ScreenPLC"))
        self.view.btn_data.bind(
            "<ButtonRelease>", lambda x: self.view.screen_change("ScreenData"))
        self.view.btn_setup.bind(
            "<ButtonRelease>", lambda x: self.view.screen_change("ScreenSetup"))
        self.view.btn_exit.bind(
            "<ButtonRelease>", lambda x: self.stop())
        self.view.screens["ScreenData"].btn_import_datasructure.bind(
            "<ButtonRelease>", lambda x: self.import_datasructure())

    def run(self):
        # initial trigger for 500ms loop
        self.view.windowframe.after(0, self.trigger_500ms)
        # start window
        self.view.windowframe.mainloop()

    def stop(self):
        # stop window
        self.view.windowframe.destroy()

    def trigger_500ms(self):
        # trigger every 500ms
        self.view.windowframe.after(500, self.trigger_500ms)
        # get actual time and save it to variable
        self.view.timestamp.set(self.model.get_time())


if __name__ == '__main__':
    app = Controller()
    app.run()

#import os
#        self.desktoppath = os.path.expanduser(r"~\Desktop")
#from tkinter import filedialog
#from tkinter import messagebox

#def get_filepath(message=None):
#    if message is not None:
#        tk.messagebox.showinfo(title=None, message=message)
#    path = tk.filedialog.askopenfilename(initialdir=self.desktoppath, title="UDT auswählen",
#                                         filetypes=(("UDT Files", "*.udt"),))
#    return path