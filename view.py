import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path
import widgets


class View:
    def __init__(self, windowframe, config):
        self.windowframe = windowframe
        self.config = config

        # general window settings----------------------------------------------
        # set title
        self.windowframe.title(self.config["title"])
        # set icon
        icon = tk.PhotoImage(file=Path(self.config["Media_icon"]))
        self.windowframe.iconphoto(True, icon)
        # set min/max windowsize
        self.windowframe.wm_minsize(self.config["min_width"], self.config["min_height"])
        self.windowframe.wm_maxsize(self.config["max_width"], self.config["max_height"])
        # set window startposisiton and startsize
        screenwidth = self.windowframe.winfo_screenwidth()
        screenheight = self.windowframe.winfo_screenheight()
        windowwidth = self.config["start_width"]
        windowheight = self.config["start_height"]
        windowstartposx = (screenwidth / 2) - (windowwidth / 2)
        windowstartposy = (screenheight / 2) - (windowheight / 2)
        self.windowframe.geometry("%dx%d+%d+%d" % (windowwidth, windowheight, windowstartposx, windowstartposy))
        # window zoomed without titlebar optional
        if self.config["fullscreen"]:
            self.windowframe.overrideredirect(True)
            self.windowframe.state("zoomed")

        # style settings-------------------------------------------------------
        # load tkinter ttk style theme
        self.windowframe.tk.call("lappend", "auto_path", Path(self.config["Style_themepath"]))
        self.windowframe.tk.call("package", "require", Path(self.config["Style_themename"]))
        self.style_main = ttk.Style()
        self.style_main.theme_use(Path(self.config["Style_themename"]))
        self.style_fg_main = self.style_main.lookup('TButton', 'foreground')
        self.style_bg_main = self.style_main.lookup('TButton', 'background')
        self.style_btn_actionbar = ttk.Style()
        self.style_btn_actionbar.configure("style_actionbar.TButton",
                                           font=("arial", 8),
                                           relief="flat")
        self.style_lbl_infobar = ttk.Style()
        self.style_lbl_infobar.configure("style_infobar.TLabel",
                                         foreground=self.style_fg_main,
                                         background=self.style_bg_main)

        # mainframe------------------------------------------------------------
        # set mainframe for window
        self.mainframe = ttk.Frame(master=self.windowframe, style="TFrame")
        # set mainframe to max size
        self.mainframe.place(x=0, y=0, height=self.config["max_height"], width=self.config["max_width"])

         # screens--------------------------------------------------------------
         # create and place screens on mainframe
#         self.screens =\
#             {"ScreenStart": ScreenStart(self)}# ,
#              "ScreenPLC": ScreenPLC(self),
#              "ScreenDaten": ScreenDaten(self),
#              "ScreenSetup": ScreenSetup(self)}

        # actionbar------------------------------------------------------------
        # create and place actionbar on mainframe
        self.actionbar = tk.Canvas(master=self.mainframe,
                                   relief="flat",
                                   bg=self.style_bg_main,
                                   highlightthickness=0,
                                   highlightbackground="black")
        self.actionbar.place(x=0, y=0, height=50, width=800)

        # create and place save button on actionbar
        self.icon_save = tk.PhotoImage(file=Path(self.config["Media_save"]))
        self.btn_save = ttk.Button(master=self.actionbar,
                                   takefocus=0,
                                   text="Save",
                                   compound=tk.TOP,
                                   image=self.icon_save,
                                   style="style_actionbar.TButton")
        self.btn_save.place(x=5, y=0, width=50, height=50)

        # create and place import button on actionbar
        self.icon_import = tk.PhotoImage(file=Path(self.config["Media_import"]))
        self.btn_import = ttk.Button(master=self.actionbar,
                                     takefocus=0,
                                     text="Import",
                                     compound=tk.TOP,
                                     image=self.icon_import,
                                     style="style_actionbar.TButton")
        self.btn_import.place(x=60, y=0, width=50, height=50)

        # create and place export button on actionbar
        self.icon_export = tk.PhotoImage(file=Path(self.config["Media_export"]))
        self.btn_export = ttk.Button(master=self.actionbar,
                                     takefocus=0,
                                     text="Export",
                                     compound=tk.TOP,
                                     image=self.icon_export,
                                     style="style_actionbar.TButton")
        self.btn_export.place(x=115, y=0, width=50, height=50)

        # create and place home button on actionbar
        self.icon_home = tk.PhotoImage(file=Path(self.config["Media_home"]))
        self.btn_home = ttk.Button(master=self.actionbar,
                                   takefocus=0,
                                   text="Home",
                                   compound=tk.TOP,
                                   image=self.icon_home,
                                   style="style_actionbar.TButton")
        self.btn_home.place(x=170, y=0, width=50, height=50)

        # create and place plc button on actionbar
        self.icon_plc = tk.PhotoImage(file=Path(self.config["Media_plc"]))
        self.btn_plc = ttk.Button(master=self.actionbar,
                                  takefocus=0,
                                  text="Plc",
                                  compound=tk.TOP,
                                  image=self.icon_plc,
                                  style="style_actionbar.TButton")
        self.btn_plc.place(x=225, y=0, width=50, height=50)

        # create and place data button on actionbar
        self.icon_data = tk.PhotoImage(file=Path(self.config["Media_data"]))
        self.btn_data = ttk.Button(master=self.actionbar,
                                   takefocus=0,
                                   text="Data",
                                   compound=tk.TOP,
                                   image=self.icon_data,
                                   style="style_actionbar.TButton")
        self.btn_data.place(x=280, y=0, width=50, height=50)

        # create and place setup button on actionbar
        self.icon_setup = tk.PhotoImage(file=Path(self.config["Media_setup"]))
        self.btn_setup = ttk.Button(master=self.actionbar,
                                    takefocus=0,
                                    text="Setup",
                                    compound=tk.TOP,
                                    image=self.icon_setup,
                                    style="style_actionbar.TButton")
        self.btn_setup.place(x=335, y=0, width=50, height=50)

        # create and place help button on actionbar
        self.icon_help = tk.PhotoImage(file=Path(self.config["Media_help"]))
        self.btn_help = ttk.Button(master=self.actionbar,
                                   takefocus=0,
                                   text="Help",
                                   compound=tk.TOP,
                                   image=self.icon_help,
                                   style="style_actionbar.TButton")
        self.btn_help.place(x=390, y=0, width=50, height=50)

        # create and place exit button on actionbar
        self.icon_exit = tk.PhotoImage(file=Path(self.config["Media_exit"]))
        self.btn_exit = ttk.Button(master=self.actionbar,
                                   takefocus=0,
                                   text="Exit",
                                   compound=tk.TOP,
                                   image=self.icon_exit,
                                   style="style_actionbar.TButton")
        self.btn_exit.place(x=695, y=0, width=50, height=50)

        # create and place Logo on Actionbar
        image = Path(self.config["Media_logo"])
        self.logo = widgets.Icon(master=self.actionbar,
                                 image=image,
                                 posx=751,
                                 posy=0)

        # Infobar--------------------------------------------------------------
        # create and place Infobar on mainframe
        self.infobar = tk.Canvas(master=self.mainframe,
                                 relief="flat",
                                 bg=self.style_bg_main,
                                 highlightthickness=0,
                                 highlightbackground="black")
        self.infobar.place(x=0, y=576, height=24, width=800)

        # create and place clock and timestamp on infobar
        image = Path(self.config["Media_clock"])
        self.icon_clock = widgets.Icon(master=self.infobar,
                                       image=image,
                                       posx=670,
                                       posy=2)

        self.timestamp = tk.StringVar()
        self.lbl_timestamp = ttk.Label(master=self.infobar,
                                       style="style_infobar.TLabel",
                                       textvariable=self.timestamp,
                                       anchor="w")
        self.lbl_timestamp.place(x=690, y=0, width=150, height=24)

        # create and place LED and label for PLC state on infobar
        self.led_plc = widgets.Led(master=self.infobar,
                                   posx=250,
                                   posy=3,
                                   diameter=16,
                                   framewidth=1,
                                   framecolor="black",
                                   ledcolor="yellow")

        self.lbl_led_plc = ttk.Label(master=self.infobar,
                                     style="style_infobar.TLabel",
                                     text="PLC",
                                     anchor="w")
        self.lbl_led_plc.place(x=270, y=2, width=50, height=18)

        # create and place versionnumber and icon on infobar
        image = Path(self.config["Media_version"])
        self.icon_version = widgets.Icon(master=self.infobar,
                                         image=image,
                                         posx=5,
                                         posy=2)

        self.version = tk.StringVar()
        self.version.set(self.config["version"])
        self.lbl_version = ttk.Label(master=self.infobar,
                                     style="style_infobar.TLabel",
                                     textvariable=self.version,
                                     anchor="w")
        self.lbl_version.place(x=25, y=2, width=150, height=18)

#         # open Startscreen-----------------------------------------------------
#         self.screen_change("ScreenStart")
#
#     def screen_change(self, screenname):
#         # open Screen by name (String)
#         self.screens[screenname].screenframe.tkraise()
#         self.btn_start.change_bg(new_bg= self.color_bar)
#         self.btn_plc.change_bg(new_bg= self.color_bar)
#         self.btn_daten.change_bg(new_bg= self.color_bar)
#         self.btn_setup.change_bg(new_bg= self.color_bar)
#         if screenname == "ScreenStart":
#             self.btn_start.change_bg(new_bg= self.color_frame)
#         elif screenname == "ScreenPLC":
#             self.btn_plc.change_bg(new_bg= self.color_frame)
#         elif screenname == "ScreenDaten":
#             self.btn_daten.change_bg(new_bg= self.color_frame)
#         elif screenname == "ScreenSetup":
#             self.btn_setup.change_bg(new_bg= self.color_frame)
#
#     def scale(self):
#         # calculate difference between minimal size and actual size
#         # so the right scale can be calculated with individual size on startup
#         # ox, oy: offset width (ox) and offset height (oy)
#         ox = int(self.windowframe.winfo_width()) - self.config["min_width"]
#         oy = int(self.windowframe.winfo_height()) - self.config["min_height"]
#         # scale GUI elements from Mainframe, Actionbar and Infobar
#         self.actionbar.place(x =-2, y= 0, height= 50, width= 804 + ox)
#         self.logo.update(offsetx= ox, offsety= 0)
#         self.infobar.place(x= -2, y= 578 + oy, height= 24, width= 804 + ox)
#         self.icon_clock.update(offsetx= ox, offsety= 0)
#         self.lbl_timestamp.place(x= 670 + ox, y= 2, width= 150, height= 18)
#         self.btn_exit.place(x=695 + ox, y=0, width=50, height=50)
#         # scale GUI elements from all the other Screens
#         for screen in self.screens:
#             self.screens[screen].scale(ox, oy)
#
#     def appearance(self):
#         self.actionbar.configure(bg= self.color_bar)
#
#         self.btn_save.configure(fg= self.color_btn_txt_fg,
#                                 bg= self.color_bar,
#                                 activebackground= self.color_btn_actbg,
#                                 activeforeground= self.color_btn_actfg)
#
#         self.btn_import.configure(fg= self.color_btn_txt_fg,
#                                   bg= self.color_bar,
#                                   activebackground= self.color_btn_actbg,
#                                   activeforeground= self.color_btn_actfg)
#
#         self.btn_export.configure(fg= self.color_btn_txt_fg,
#                                   bg= self.color_bar,
#                                   activebackground= self.color_btn_actbg,
#                                   activeforeground= self.color_btn_actfg)
#
#         self.btn_start.configure(fg= self.color_btn_txt_fg,
#                                  bg= self.color_bar,
#                                  activebackground= self.color_btn_actbg,
#                                  activeforeground= self.color_btn_actfg)
#
#         self.btn_plc.configure(fg= self.color_btn_txt_fg,
#                                bg= self.color_bar,
#                                activebackground= self.color_btn_actbg,
#                                activeforeground= self.color_btn_actfg)
#
#         self.btn_daten.configure(fg= self.color_btn_txt_fg,
#                               bg= self.color_bar,
#                               activebackground= self.color_btn_actbg,
#                               activeforeground= self.color_btn_actfg)
#
#         self.btn_setup.configure(fg= self.color_btn_txt_fg,
#                                  bg= self.color_bar,
#                                  activebackground= self.color_btn_actbg,
#                                  activeforeground= self.color_btn_actfg)
#
#         self.btn_help.configure(fg= self.color_btn_txt_fg,
#                                 bg= self.color_bar,
#                                 activebackground= self.color_btn_actbg,
#                                 activeforeground= self.color_btn_actfg)
#
#         self.btn_exit.configure(fg= self.color_btn_txt_fg,
#                                 bg= self.color_bar,
#                                 activebackground= self.color_btn_actbg,
#                                 activeforeground= self.color_btn_actfg)
#
#         self.infobar.configure(bg= self.color_bar)
#
#         self.lbl_timestamp.configure(background= self.color_bar,
#                                      foreground= self.color_btn_actfg)
#
#         self.led_plc.colorchange(framecolor= self.color_bar)
#
#         self.lbl_led_plc.configure(background= self.color_bar,
#                                    foreground= self.color_btn_actfg)
#
#         self.lbl_version.configure(background= self.color_bar,
#                                    foreground= self.color_btn_actfg)
#
#         for screen in self.screens:
#             self.screens[screen].appearance()
#
#
# class ScreenStart:
#     def __init__(self, master):
#         self.master = master
#         self.screenframe = tk.Frame(master= self.master.mainframe)
#         self.screenframe.place(x= 0, y= 50, height= 528, width= 800)
#
#         # create and place screenframe background
#         self.background = tk.Canvas(master= self.screenframe,
#                                     relief= self.master.relief,
#                                     bg= self.master.color_frame,
#                                     bd= 0,
#                                     highlightthickness= 0)
#
#         self.background.place(x= 0, y= 0, height= 1080, width= 1924)
#         self.label_mainmenue = tk.Label(master= self.screenframe,
#                                         relief= self.master.relief,
#                                         text= "Hauptmenü",
#                                         anchor= "w",
#                                         font = (self.master.font, 10))
#         self.label_mainmenue.place(x= 205, y= 335, width= 100, height= 17)
#
#     def scale(self, ox, oy):
#         # scale GUI elements
#         # ox, oy: offset width (ox) and offset height (oy)
#         self.screenframe.place(x= 0, y= 50, height= 528 + oy, width= 800 + ox)
#         self.background.place(x= 0, y= 0, height= 1080 + oy, width= 1924 + ox)
#
#     def appearance(self):
#         # refresh GUI elements
#         self.background.configure(bg= self.master.color_frame)
#
#
# class ScreenPLC:
#     def __init__(self, master):
#         self.master = master
#         self.screenframe = tk.Frame(master= self.master.mainframe)
#         self.screenframe.place(x= 0, y= 50, height= 528, width= 800)
#
#         # create and place screenframe background
#         self.background = tk.Canvas(master= self.screenframe,
#                                     relief=self.master.relief,
#                                     bg= self.master.color_frame,
#                                     bd= 0,
#                                     highlightthickness= 0)
#
#         self.background.place(x= -2, y= 0, height= 1080, width= 1924)
#         self.label_sps = tk.Label(master= self.screenframe,
#                                   relief= self.master.relief,
#                                   text= "Steuerung",
#                                   anchor= "w",
#                                   font = (self.master.font, 10))
#         self.label_sps.place(x= 205, y= 335, width= 100, height= 17)
#
#     def scale(self, ox, oy):
#         # scale GUI elements
#         # ox, oy: offset width (ox) and offset height (oy)
#         self.screenframe.place(x= 0, y= 50, height= 528 + oy, width= 800 + ox)
#         self.background.place(x= 0, y= 0, height= 1080 + oy, width= 1924 + ox)
#
#     def appearance(self):
#         # refresh GUI elements
#         self.background.configure(bg= self.master.color_frame)
#
#
# class ScreenDaten:
#     def __init__(self, master):
#         self.master = master
#         self.screenframe = tk.Frame(master= self.master.mainframe)
#         self.screenframe.place(x= 0, y= 50, height= 528, width= 800)
#
#         # create and place screenframe background
#         self.background = tk.Canvas(master= self.screenframe,
#                                     relief= self.master.relief,
#                                     bg= self.master.color_frame,
#                                     bd= 0,
#                                     highlightthickness= 0)
#
#         self.background.place(x= -2, y= 0, height= 1080, width= 1924)
#         self.label_daten = tk.Label(master= self.screenframe,
#                                  relief= self.master.relief,
#                                  text= "Daten",
#                                  anchor= "w",
#                                  font = (self.master.font, 10))
#         self.label_daten.place(x= 205, y= 335, width= 100, height= 17)
#
#     def scale(self, ox, oy):
#         # scale GUI elements
#         # ox, oy: offset width (ox) and offset height (oy)
#         self.screenframe.place(x= 0, y= 50, height= 528 + oy, width= 800 + ox)
#         self.background.place(x= 0, y= 0, height= 1080 + oy, width= 1924 + ox)
#
#     def appearance(self):
#         # refresh GUI elements
#         self.background.configure(bg= self.master.color_frame)
#
#
# class ScreenSetup:
#     def __init__(self, master):
#         self.master = master
#         self.screenframe = tk.Frame(master= self.master.mainframe)
#         self.screenframe.place(x= 0, y= 50, height= 528, width= 800)
#
#         # create and place screenframe background
#         self.background = tk.Canvas(master= self.screenframe,
#                                     relief= self.master.relief,
#                                     bg= self.master.color_frame,
#                                     bd= 0,
#                                     highlightthickness= 0)
#         self.background.place(x= -2, y= 0, height= 1080, width= 1924)
#
#     def scale(self, ox, oy):
#         # scale GUI elements
#         # ox, oy: offset width (ox) and offset height (oy)
#         self.screenframe.place(x= 0, y= 50, height= 528 + oy, width= 800 + ox)
#         self.background.place(x= 0, y= 0, height= 1080 + oy, width= 1924 + ox)
#
#     def appearance(self):
#         # refresh GUI elements
#         self.background.configure(bg= self.master.color_frame)