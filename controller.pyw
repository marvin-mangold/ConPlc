import tkinter as tk
import confighandler
import time
import random
import view
import model


class Controller:
    def __init__(self):
        # initialise window
        self.windowframe = tk.Tk()
        # get Configdata from Configfile
        self.config = confighandler.readconfig("config.wplc")
        # call view (handles the graphics of GUI)
        self.view = view.View(self.windowframe, self.config)
        # call model (handles the functions of GUI)
        self.model = model.Model(self.config)

        # ---------------------------------------------------------------------
        # call scale function when windowsize gets changed
        #self.windowframe.bind(
        #    "<Configure>", lambda x: self.view.scale())

        # ---------------------------------------------------------------------
        # connect view and model and controller (Buttons, Events, Functions)
        #self.view.btn_start.bind(
        #    "<ButtonRelease>", lambda x: self.view.screen_change("ScreenStart"))
        #self.view.btn_plc.bind(
        #    "<ButtonRelease>", lambda x: self.view.screen_change("ScreenPLC"))
        #self.view.btn_daten.bind(
        #    "<ButtonRelease>", lambda x: self.view.screen_change("ScreenDaten"))
        #self.view.btn_setup.bind(
        #    "<ButtonRelease>", lambda x: self.view.screen_change("ScreenSetup"))
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
        # trigger every 500ms
        self.windowframe.after(500, self.trigger_500ms)
        # get actual time and save it to variable
        self.view.timestamp.set(time.strftime("%d.%m.%Y %H:%M:%S"))
        rnd = random.choice(["red", "green", "yellow"])
        self.view.led_plc.colorchange(ledcolor=rnd)


if __name__ == '__main__':
    app = Controller()
    app.run()
