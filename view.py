import tkinter as tk
from pathlib import Path
import widgets


class View:
    def __init__(self, windowframe, config):
        self.windowframe = windowframe
        self.config = config
        # set versionnumber
        self.version = tk.StringVar()
        self.version.set(self.config["version"])
        # define font
        self.font = self.config["font"]
        # define colors
        self.color_bar = self.config["Color_bar"]
        self.color_frame = self.config["Color_frame"]
        self.color_btn_actbg = self.config["Color_btn_actbg"]
        self.color_btn_actfg = self.config["Color_btn_actfg"]
        self.color_btn_txt_fg = self.config["Color_txt_fg"]
        # change widgetstyle to see the framesize
        self.relief =   "flat"#"raised"
        # Mainframe------------------------------------------------------------
        # set Mainframe for Window
        self.mainframe = tk.Frame(master= self.windowframe,
                                  bd= 0,
                                  highlightthickness= 0)
        # set Mainframe to max size
        self.mainframe.place(x= 0,
                             y= 0,
                             height= self.config["max_height"],
                             width= self.config["max_width"])

        # Screens--------------------------------------------------------------
        # create and place Screens on Mainframe
        self.screens =\
            {"ScreenStart": ScreenStart(self),
             "ScreenPLC": ScreenPLC(self),
             "ScreenDB": ScreenDB(self),
             "ScreenSetup": ScreenSetup(self)}

        # Actionbar------------------------------------------------------------
        # create and place Actionbar on Mainframe
        self.actionbar = tk.Canvas(master= self.mainframe,
                                   relief= self.relief,
                                   bg= self.color_bar,
                                   highlightthickness= 0,
                                   highlightbackground= "black")
        self.actionbar.place(x= -2, y= 0, height= 50, width= 804)

        # create and place SAVEbutton on Actionbar
        self.icon_save = tk.PhotoImage(file= Path(self.config["Media_save"]))
        self.btn_save = widgets.Button(master= self.actionbar,
                                       relief= self.relief,
                                       bd= 0,
                                       image= self.icon_save,
                                       compound= "top",
                                       text= "Speichern",
                                       font= (self.font, 8),
                                       anchor= "s",
                                       fg= self.color_btn_txt_fg,
                                       bg= self.color_bar,
                                       activebackground= self.color_btn_actbg,
                                       activeforeground= self.color_btn_actfg,
                                       highlightthickness= 0)
        self.btn_save.place(x= 5, y= 0, width= 50, height= 50)

        # create and place IMPORTbutton on Actionbar
        self.icon_import = tk.PhotoImage(file= Path(self.config["Media_import"]))
        self.btn_import = widgets.Button(master= self.actionbar,
                                         relief= self.relief,
                                         bd= 0,
                                         image= self.icon_import,
                                         compound= "top",
                                         text= "Import",
                                         font= (self.font, 8),
                                         anchor= "s",
                                         fg= self.color_btn_txt_fg,
                                         bg= self.color_bar,
                                         activebackground= self.color_btn_actbg,
                                         activeforeground= self.color_btn_actfg,
                                         highlightthickness= 0)
        self.btn_import.place(x= 60, y= 0, width= 50, height= 50)

        # create and place EXPORTbutton on Actionbar
        self.icon_export = tk.PhotoImage(file= Path(self.config["Media_export"]))
        self.btn_export = widgets.Button(master= self.actionbar,
                                         relief= self.relief,
                                         bd= 0,
                                         image= self.icon_export,
                                         compound= "top",
                                         text= "Export",
                                         font= (self.font, 8),
                                         anchor= "s",
                                         fg= self.color_btn_txt_fg,
                                         bg= self.color_bar,
                                         activebackground= self.color_btn_actbg,
                                         activeforeground= self.color_btn_actfg,
                                         highlightthickness= 0)
        self.btn_export.place(x= 115, y= 0, width= 50, height= 50)

        # create and place STARTbutton on Actionbar
        self.icon_start = tk.PhotoImage(file= Path(self.config["Media_start"]))
        self.btn_start = widgets.Button(master= self.actionbar,
                                        relief= self.relief,
                                        bd= 0,
                                        image= self.icon_start,
                                        compound= "top",
                                        text= "Start",
                                        font= (self.font, 8),
                                        anchor= "s",
                                        fg= self.color_btn_txt_fg,
                                        bg= self.color_bar,
                                        activebackground= self.color_btn_actbg,
                                        activeforeground= self.color_btn_actfg,
                                        highlightthickness= 0)
        self.btn_start.place(x= 170, y= 0, width= 50, height= 50)

        # create and place PLCbutton on Actionbar
        self.icon_plc = tk.PhotoImage(file= Path(self.config["Media_plc"]))
        self.btn_plc = widgets.Button(master= self.actionbar,
                                      relief= self.relief,
                                      bd= 0,
                                      image= self.icon_plc,
                                      compound= "top",
                                      text= "SPS",
                                      font= (self.font, 8),
                                      anchor= "s",
                                      fg= self.color_btn_txt_fg,
                                      bg= self.color_bar,
                                      activebackground= self.color_btn_actbg,
                                      activeforeground= self.color_btn_actfg,
                                      highlightthickness= 0)
        self.btn_plc.place(x= 225, y= 0, width= 50, height= 50)

        # create and place DBbutton on Actionbar
        self.icon_db = tk.PhotoImage(file= Path(self.config["Media_db"]))
        self.btn_db = widgets.Button(master= self.actionbar,
                                     relief= self.relief,
                                     bd= 0,
                                     image= self.icon_db,
                                     compound= "top",
                                     text= "DB",
                                     font= (self.font, 8),
                                     anchor= "s",
                                     fg= self.color_btn_txt_fg,
                                     bg= self.color_bar,
                                     activebackground= self.color_btn_actbg,
                                     activeforeground= self.color_btn_actfg,
                                     highlightthickness= 0)
        self.btn_db.place(x= 280, y= 0, width= 50, height= 50)

        # create and place SETUPbutton on Actionbar
        self.icon_setup = tk.PhotoImage(file= Path(self.config["Media_setup"]))
        self.btn_setup = widgets.Button(master= self.actionbar,
                                        relief= self.relief,
                                        bd= 0,
                                        image= self.icon_setup,
                                        compound= "top",
                                        text= "Einstellen",
                                        font= (self.font, 8),
                                        anchor= "s",
                                        fg= self.color_btn_txt_fg,
                                        bg= self.color_bar,
                                        activebackground= self.color_btn_actbg,
                                        activeforeground= self.color_btn_actfg,
                                        highlightthickness= 0)
        self.btn_setup.place(x= 335, y= 0, width= 50, height= 50)

        # create and place HELPbutton on Actionbar
        self.icon_help = tk.PhotoImage(file= Path(self.config["Media_help"]))
        self.btn_help = widgets.Button(master= self.actionbar,
                                       relief= self.relief,
                                       bd= 0,
                                       image= self.icon_help,
                                       compound= "top",
                                       text= "Hilfe",
                                       font= (self.font, 8),
                                       anchor= "s",
                                       fg= self.color_btn_txt_fg,
                                       bg= self.color_bar,
                                       activebackground= self.color_btn_actbg,
                                       activeforeground= self.color_btn_actfg,
                                       highlightthickness= 0)
        self.btn_help.place(x= 390, y= 0, width= 50, height= 50)

        # create and place EXITbutton on Actionbar
        self.icon_exit = tk.PhotoImage(file= Path(self.config["Media_exit"]))
        self.btn_exit = widgets.Button(master= self.actionbar,
                                        relief= self.relief,
                                        bd= 0,
                                        image= self.icon_exit,
                                        compound= "top",
                                        text= "Exit",
                                        font= (self.font, 8),
                                        anchor= "s",
                                        fg= self.color_btn_txt_fg,
                                        bg= self.color_bar,
                                        activebackground= self.color_btn_actbg,
                                        activeforeground= self.color_btn_actfg,
                                        highlightthickness= 0,
                                        takefocus= 0)
        self.btn_exit.place(x= 695, y= 0, width= 50, height= 50)

        # create and place Logo on Actionbar
        image = Path(self.config["Media_logo"])
        self.logo = widgets.Icon(master= self.actionbar,
                                 image= image,
                                 posx= 751,
                                 posy= 0)

        # Infobar--------------------------------------------------------------
        # create and place Infobar on Mainframe
        self.infobar = tk.Canvas(master= self.mainframe,
                                 relief= self.relief,
                                 bg= self.color_bar,
                                 highlightthickness= 1,
                                 highlightbackground= "black")
        self.infobar.place(x= -2, y= 578, height= 24, width= 804)

        # create and place clock and timestamp on Infobar
        image = Path(self.config["Media_clock"])
        self.icon_clock = widgets.Icon(master= self.infobar,
                                       image= image,
                                       posx= 648,
                                       posy= 1)

        self.timestamp = tk.StringVar()
        self.lbl_timestamp = tk.Label(master= self.infobar,
                                      relief= self.relief,
                                      background= self.color_bar,
                                      anchor= "w",
                                      foreground= self.color_btn_actfg,
                                      textvariable= self.timestamp,
                                      font= (self.font, 10))
        self.lbl_timestamp.place(x= 665, y= 2, width= 150, height= 18)
        # call trigger function after label is placed

        # create and place LED for PLC state on Infobar
        self.led_plc = widgets.Led(master= self.infobar,
                                   posx= 250,
                                   posy= 2,
                                   diameter= 16,
                                   framewidth= 1,
                                   framecolor= self.color_bar,
                                   ledcolor= "yellow")

        self.lbl_led_plc = tk.Label(master= self.infobar,
                                    relief= self.relief,
                                    anchor= "w",
                                    background= self.color_bar,
                                    foreground= self.color_btn_actfg,
                                    text= "SPS",
                                    font= (self.font, 10))
        self.lbl_led_plc.place(x= 270, y= 2, width= 50, height= 18)

        # create and place LED for DB state on Infobar
        self.led_db = widgets.Led(master= self.infobar,
                                  posx= 400,
                                  posy= 3,
                                  diameter= 16,
                                  framewidth= 1,
                                  framecolor= self.color_bar,
                                  ledcolor= "yellow")

        self.lbl_led_db = tk.Label(master= self.infobar,
                                   relief= self.relief,
                                   anchor= "w",
                                   background= self.color_bar,
                                   foreground= self.color_btn_actfg,
                                   text= "DB",
                                   font= (self.font, 10))
        self.lbl_led_db.place(x= 420, y= 2, width= 50, height= 18)

        # create and place versionnumber and icon on Infobar
        image = Path(self.config["Media_version"])
        self.icon_version = widgets.Icon(master= self.infobar,
                                         image= image,
                                         posx= 5,
                                         posy= 2)

        self.lbl_version = tk.Label(master= self.infobar,
                                    relief= self.relief,
                                    anchor= "w",
                                    background= self.color_bar,
                                    foreground= self.color_btn_actfg,
                                    textvariable= self.version,
                                    font= (self.font, 10))
        self.lbl_version.place(x= 25, y= 2, width= 150, height= 18)

        # open Startscreen-----------------------------------------------------
        self.screen_change("ScreenStart")

    def screen_change(self, screenname):
        # open Screen by name (String)
        self.screens[screenname].screenframe.tkraise()
        self.btn_start.change_bg(new_bg= self.color_bar)
        self.btn_plc.change_bg(new_bg= self.color_bar)
        self.btn_db.change_bg(new_bg= self.color_bar)
        self.btn_setup.change_bg(new_bg= self.color_bar)
        if screenname == "ScreenStart":
            self.btn_start.change_bg(new_bg= self.color_frame)
        elif screenname == "ScreenPLC":
            self.btn_plc.change_bg(new_bg= self.color_frame)
        elif screenname == "ScreenDB":
            self.btn_db.change_bg(new_bg= self.color_frame)
        elif screenname == "ScreenSetup":
            self.btn_setup.change_bg(new_bg= self.color_frame)

    def scale(self):
        # calculate difference between minimal size and actual size
        # so the right scale can be calculated with individual size on startup
        # ox, oy: offset width (ox) and offset height (oy)
        ox = int(self.windowframe.winfo_width()) - self.config["min_width"]
        oy = int(self.windowframe.winfo_height()) - self.config["min_height"]
        # scale GUI elements from Mainframe, Actionbar and Infobar
        self.actionbar.place(x =-2, y= 0, height= 50, width= 804 + ox)
        self.logo.update(offsetx= ox, offsety= 0)
        self.infobar.place(x= -2, y= 578 + oy, height= 24, width= 804 + ox)
        self.icon_clock.update(offsetx= ox, offsety= 0)
        self.lbl_timestamp.place(x= 670 + ox, y= 2, width= 150, height= 18)
        self.btn_exit.place(x=695 + ox, y=0, width=50, height=50)
        # scale GUI elements from all the other Screens
        for screen in self.screens:
            self.screens[screen].scale(ox, oy)

    def appearance(self):
        self.actionbar.configure(bg= self.color_bar)

        self.btn_save.configure(fg= self.color_btn_txt_fg,
                                bg= self.color_bar,
                                activebackground= self.color_btn_actbg,
                                activeforeground= self.color_btn_actfg)

        self.btn_import.configure(fg= self.color_btn_txt_fg,
                                  bg= self.color_bar,
                                  activebackground= self.color_btn_actbg,
                                  activeforeground= self.color_btn_actfg)

        self.btn_export.configure(fg= self.color_btn_txt_fg,
                                  bg= self.color_bar,
                                  activebackground= self.color_btn_actbg,
                                  activeforeground= self.color_btn_actfg)

        self.btn_start.configure(fg= self.color_btn_txt_fg,
                                 bg= self.color_bar,
                                 activebackground= self.color_btn_actbg,
                                 activeforeground= self.color_btn_actfg)

        self.btn_plc.configure(fg= self.color_btn_txt_fg,
                               bg= self.color_bar,
                               activebackground= self.color_btn_actbg,
                               activeforeground= self.color_btn_actfg)

        self.btn_db.configure(fg= self.color_btn_txt_fg,
                              bg= self.color_bar,
                              activebackground= self.color_btn_actbg,
                              activeforeground= self.color_btn_actfg)

        self.btn_setup.configure(fg= self.color_btn_txt_fg,
                                 bg= self.color_bar,
                                 activebackground= self.color_btn_actbg,
                                 activeforeground= self.color_btn_actfg)

        self.btn_help.configure(fg= self.color_btn_txt_fg,
                                bg= self.color_bar,
                                activebackground= self.color_btn_actbg,
                                activeforeground= self.color_btn_actfg)

        self.btn_exit.configure(fg= self.color_btn_txt_fg,
                                bg= self.color_bar,
                                activebackground= self.color_btn_actbg,
                                activeforeground= self.color_btn_actfg)

        self.infobar.configure(bg= self.color_bar)

        self.lbl_timestamp.configure(background= self.color_bar,
                                     foreground= self.color_btn_actfg)

        self.led_plc.colorchange(framecolor= self.color_bar)

        self.lbl_led_plc.configure(background= self.color_bar,
                                   foreground= self.color_btn_actfg)

        self.led_db.colorchange(framecolor= self.color_bar)

        self.lbl_led_db.configure(background= self.color_bar,
                                  foreground= self.color_btn_actfg)

        self.lbl_version.configure(background= self.color_bar,
                                   foreground= self.color_btn_actfg)

        for screen in self.screens:
            self.screens[screen].appearance()


class ScreenStart:
    def __init__(self, master):
        self.master = master
        self.screenframe = tk.Frame(master= self.master.mainframe)
        self.screenframe.place(x= 0, y= 50, height= 528, width= 800)

        # create and place screenframe background
        self.background = tk.Canvas(master= self.screenframe,
                                    relief= self.master.relief,
                                    bg= self.master.color_frame,
                                    bd= 0,
                                    highlightthickness= 0)

        self.background.place(x= 0, y= 0, height= 1080, width= 1924)
        self.label_mainmenue = tk.Label(master= self.screenframe,
                                        relief= self.master.relief,
                                        text= "Hauptmenü",
                                        anchor= "w",
                                        font = (self.master.font, 10))
        self.label_mainmenue.place(x= 205, y= 335, width= 100, height= 17)

    def scale(self, ox, oy):
        # scale GUI elements
        # ox, oy: offset width (ox) and offset height (oy)
        self.screenframe.place(x= 0, y= 50, height= 528 + oy, width= 800 + ox)
        self.background.place(x= 0, y= 0, height= 1080 + oy, width= 1924 + ox)

    def appearance(self):
        # refresh GUI elements
        self.background.configure(bg= self.master.color_frame)


class ScreenPLC:
    def __init__(self, master):
        self.master = master
        self.screenframe = tk.Frame(master= self.master.mainframe)
        self.screenframe.place(x= 0, y= 50, height= 528, width= 800)

        # create and place screenframe background
        self.background = tk.Canvas(master= self.screenframe,
                                    relief=self.master.relief,
                                    bg= self.master.color_frame,
                                    bd= 0,
                                    highlightthickness= 0)

        self.background.place(x= -2, y= 0, height= 1080, width= 1924)
        self.label_sps = tk.Label(master= self.screenframe,
                                  relief= self.master.relief,
                                  text= "Steuerung",
                                  anchor= "w",
                                  font = (self.master.font, 10))
        self.label_sps.place(x= 205, y= 335, width= 100, height= 17)

    def scale(self, ox, oy):
        # scale GUI elements
        # ox, oy: offset width (ox) and offset height (oy)
        self.screenframe.place(x= 0, y= 50, height= 528 + oy, width= 800 + ox)
        self.background.place(x= 0, y= 0, height= 1080 + oy, width= 1924 + ox)

    def appearance(self):
        # refresh GUI elements
        self.background.configure(bg= self.master.color_frame)


class ScreenDB:
    def __init__(self, master):
        self.master = master
        self.screenframe = tk.Frame(master= self.master.mainframe)
        self.screenframe.place(x= 0, y= 50, height= 528, width= 800)

        # create and place screenframe background
        self.background = tk.Canvas(master= self.screenframe,
                                    relief= self.master.relief,
                                    bg= self.master.color_frame,
                                    bd= 0,
                                    highlightthickness= 0)

        self.background.place(x= -2, y= 0, height= 1080, width= 1924)
        self.label_db = tk.Label(master= self.screenframe,
                                 relief= self.master.relief,
                                 text= "Datenbank",
                                 anchor= "w",
                                 font = (self.master.font, 10))
        self.label_db.place(x= 205, y= 335, width= 100, height= 17)

    def scale(self, ox, oy):
        # scale GUI elements
        # ox, oy: offset width (ox) and offset height (oy)
        self.screenframe.place(x= 0, y= 50, height= 528 + oy, width= 800 + ox)
        self.background.place(x= 0, y= 0, height= 1080 + oy, width= 1924 + ox)

    def appearance(self):
        # refresh GUI elements
        self.background.configure(bg= self.master.color_frame)


class ScreenSetup:
    def __init__(self, master):
        self.master = master
        self.screenframe = tk.Frame(master= self.master.mainframe)
        self.screenframe.place(x= 0, y= 50, height= 528, width= 800)

        # create and place screenframe background
        self.background = tk.Canvas(master= self.screenframe,
                                    relief= self.master.relief,
                                    bg= self.master.color_frame,
                                    bd= 0,
                                    highlightthickness= 0)
        self.background.place(x= -2, y= 0, height= 1080, width= 1924)

        # create and place Label for resolution settings
        self.lbl_resolution = tk.Label(master= self.screenframe,
                                       relief= self.master.relief,
                                       text= "Auflösung:",
                                       background= self.master.color_frame,
                                       foreground= self.master.color_btn_txt_fg,
                                       anchor= "w",
                                       font = (self.master.font, 15))
        self.lbl_resolution.place(x= 25, y= 25, width= 100, height= 30)

        # create and place Label for resolutionwidth
        self.lbl_resolutionwidth = tk.Label(master= self.screenframe,
                                            relief= self.master.relief,
                                            text= "Breite",
                                            background= self.master.color_frame,
                                            foreground= self.master.color_btn_txt_fg,
                                            anchor= "w",
                                            font = (self.master.font, 10))
        self.lbl_resolutionwidth.place(x= 280, y= 65, width= 40, height= 10)

        # create and place Label for resolutionheight
        self.lbl_resolutionheight = tk.Label(master= self.screenframe,
                                            relief= self.master.relief,
                                            text= "Höhe",
                                            background= self.master.color_frame,
                                            foreground= self.master.color_btn_txt_fg,
                                            anchor= "w",
                                            font = (self.master.font, 10))
        self.lbl_resolutionheight.place(x= 580, y= 65, width= 40, height= 10)

        # create and place Scalebar for resolutionwidth
        self.resolutionwidth = tk.IntVar()
        self.resolutionwidth.set(self.master.config["start_width"])
        self.scale_resolutionwidth = tk.Scale(master= self.screenframe,
                                              relief= self.master.relief,
                                              orient= "horizontal",
                                              background=self.master.color_bar,
                                              activebackground=self.master.color_bar,
                                              foreground=self.master.color_btn_txt_fg,
                                              from_= self.master.config["min_width"],
                                              to= self.master.config["max_width"],
                                              variable= self.resolutionwidth)
        self.scale_resolutionwidth.place(x= 200, y= 20, width= 200, height= 40)

        # create and place Button for resolutionwidth -1
        self.btn_resolutionwidth_minus = tk.Button(master= self.screenframe,
                                                   relief="raised",
                                                   text= "<",
                                                   fg=self.master.color_btn_txt_fg,
                                                   bg=self.master.color_bar,
                                                   activebackground=self.master.color_btn_actbg,
                                                   activeforeground=self.master.color_btn_actfg,
                                                   highlightthickness=0,
                                                   borderwidth=4)
        self.btn_resolutionwidth_minus.place(x= 180, y= 20, width= 20, height= 42)

        # create and place Button for resolutionwidth +1
        self.btn_resolutionwidth_plus = tk.Button(master= self.screenframe,
                                                   relief="raised",
                                                   text= ">",
                                                   fg=self.master.color_btn_txt_fg,
                                                   bg=self.master.color_bar,
                                                   activebackground=self.master.color_btn_actbg,
                                                   activeforeground=self.master.color_btn_actfg,
                                                   highlightthickness=0,
                                                   borderwidth=4)
        self.btn_resolutionwidth_plus.place(x= 402, y= 20, width= 20, height= 42)

        # create and place Scalebar for resolutionheight
        self.resolutionheight = tk.IntVar()
        self.resolutionheight.set(self.master.config["start_height"])
        self.scale_resolutionheight = tk.Scale(master= self.screenframe,
                                               relief=self.master.relief,
                                               orient="horizontal",
                                               background=self.master.color_bar,
                                               activebackground=self.master.color_bar,
                                               foreground=self.master.color_btn_txt_fg,
                                               from_=self.master.config["min_height"],
                                               to=self.master.config["max_height"],
                                               variable=self.resolutionheight)
        self.scale_resolutionheight.place(x= 500, y= 20, width= 200, height= 40)

        # create and place Button for resolutionheight -1
        self.btn_resolutionheight_minus = tk.Button(master= self.screenframe,
                                                   relief="raised",
                                                   text= "<",
                                                   fg=self.master.color_btn_txt_fg,
                                                   bg=self.master.color_bar,
                                                   activebackground=self.master.color_btn_actbg,
                                                   activeforeground=self.master.color_btn_actfg,
                                                   highlightthickness=0,
                                                   borderwidth=4)
        self.btn_resolutionheight_minus.place(x= 480, y= 20, width= 20, height= 42)

        # create and place Button for resolutionheight +1
        self.btn_resolutionheight_plus = tk.Button(master= self.screenframe,
                                                   relief="raised",
                                                   text= ">",
                                                   fg=self.master.color_btn_txt_fg,
                                                   bg=self.master.color_bar,
                                                   activebackground=self.master.color_btn_actbg,
                                                   activeforeground=self.master.color_btn_actfg,
                                                   highlightthickness=0,
                                                   borderwidth=4)
        self.btn_resolutionheight_plus.place(x= 702, y= 20, width= 20, height= 42)

    def scale(self, ox, oy):
        # scale GUI elements
        # ox, oy: offset width (ox) and offset height (oy)
        self.screenframe.place(x= 0, y= 50, height= 528 + oy, width= 800 + ox)
        self.background.place(x= 0, y= 0, height= 1080 + oy, width= 1924 + ox)

    def appearance(self):
        # refresh GUI elements
        self.background.configure(bg= self.master.color_frame)