import tkinter as tk
import tkinter.ttk as ttk 
from pathlib import Path
import confighandler
import time
import random
import view
import model


class Controller:
    def __init__(self):
        self.windowframe = tk.Tk()
        # get Configdata from Configfile
        self.config = confighandler.readconfig("config.plc")
        # set Title
        self.windowframe.title(self.config["title"])
        # set Icon
        icon = tk.PhotoImage(file=Path(self.config["Media_icon"]))
        self.windowframe.iconphoto(True, icon)
        # set min/max Windowsize
        self.windowframe.wm_minsize(self.config["min_width"],
                                    self.config["min_height"])
        self.windowframe.wm_maxsize(self.config["max_width"],
                                    self.config["max_height"])
        # ---------------------------------------------------------------------
        # set Window startposisiton and startsize
        screenwidth = self.windowframe.winfo_screenwidth()
        screenheight = self.windowframe.winfo_screenheight()
        windowwidth = self.config["start_width"]
        windowheight = self.config["start_height"]
        windowstartposx = (screenwidth / 2) - (windowwidth / 2)
        windowstartposy = (screenheight / 2) - (windowheight / 2)
        self.windowframe.geometry(
            "%dx%d+%d+%d" % (windowwidth, windowheight,
                             windowstartposx, windowstartposy))
        # window zoomed without Titlebar optional
        if self.config["fullscreen"]:
            self.windowframe.overrideredirect(True)
            self.windowframe.state("zoomed")
        # ---------------------------------------------------------------------
        # call view (handles the graphics of GUI)
        self.view = view.View(self.windowframe, self.config)
        # call model (handles the functions of GUI)
        self.model = model.Model(self.config)
        # ---------------------------------------------------------------------
        # call scale funktion when windowsize gets changed
        self.windowframe.bind(
            "<Configure>", lambda x: self.view.scale())
        # ---------------------------------------------------------------------
        # connect view and model and controller (Buttons, Events, Functions)
        self.view.btn_start.bind(
            "<ButtonRelease>", lambda x: self.view.screen_change("ScreenStart"))
        self.view.btn_plc.bind(
            "<ButtonRelease>", lambda x: self.view.screen_change("ScreenPLC"))
        self.view.btn_db.bind(
            "<ButtonRelease>", lambda x: self.view.screen_change("ScreenDB"))
        self.view.btn_setup.bind(
            "<ButtonRelease>", lambda x: self.view.screen_change("ScreenSetup"))
        self.view.btn_exit.bind(
            "<ButtonRelease>", lambda x: self.stop())

    def run(self):
        # initial trigger for 500ms loop
        self.windowframe.after(0, self.trigger_500ms)
        # start window
        self.windowframe.mainloop()

    def stop(self):
        # stop window
        self.windowframe.destroy()

    def trigger_500ms(self):
        # Trigger every 500ms
        self.windowframe.after(500, self.trigger_500ms)
        # get actual time and save it to variable
        self.view.timestamp.set(time.strftime("%d.%m.%Y %H:%M:%S"))
        rnd = random.choice(["red", "green", "yellow"])
        self.view.led_plc.colorchange(ledcolor= rnd)
        rnd = random.choice(["red", "green", "yellow"])
        self.view.led_db.colorchange(ledcolor= rnd)


if __name__ == '__main__':
    app = Controller()
    app.run()
