import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path
import widgets


class View:
    def __init__(self, config):
        self.config = config

        # general window settings----------------------------------------------
        # set title
        self.windowframe = tk.Tk()
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

        # style settings-general-----------------------------------------------
        # load tkinter ttk style theme
        self.windowframe.tk.call("lappend", "auto_path", Path(self.config["Style_themepath"]))
        self.windowframe.tk.call("package", "require", Path(self.config["Style_themename"]))
        self.style_main = ttk.Style()
        self.style_main.theme_use(Path(self.config["Style_themename"]))
        # copy colorcodes
        self.color_btn_fg_main = self.style_main.lookup('TButton', 'foreground')
        self.color_btn_bg_main = self.style_main.lookup('TButton', 'background')
        self.color_bg_contrast = "#3d4145"

        # mainframe------------------------------------------------------------
        # set mainframe for window
        self.mainframe = ttk.Frame(master=self.windowframe, style="TFrame")
        # set mainframe to max size
        self.mainframe.place(x=0, y=0, height=self.config["max_height"], width=self.config["max_width"])

        # style customisation--------------------------------------------------
        self.style_btn_actionbar = ttk.Style()
        self.style_btn_actionbar.configure("style_actionbar.TButton",
                                           font=("arial", 8),
                                           relief="flat")
        self.style_lbl_infobar = ttk.Style()
        self.style_lbl_infobar.configure("style_infobar.TLabel",
                                         foreground=self.color_btn_fg_main,
                                         background=self.color_btn_bg_main)

        # screens--------------------------------------------------------------
        # create and place screens on mainframe
        self.screens =\
            {"ScreenStart": ScreenStart(self),
             "ScreenPLC": ScreenPLC(self),
             "ScreenData": ScreenData(self),
             "ScreenSetup": ScreenSetup(self)}

        # actionbar------------------------------------------------------------
        # create and place actionbar on mainframe
        self.actionbar = tk.Canvas(master=self.mainframe,
                                   relief="flat",
                                   bg=self.color_btn_bg_main,
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

        # infobar--------------------------------------------------------------
        # create and place infobar on mainframe
        self.infobar = tk.Canvas(master=self.mainframe,
                                 relief="flat",
                                 bg=self.color_btn_bg_main,
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

        # open startscreen-----------------------------------------------------
        self.screen_change("ScreenStart")

    def screen_change(self, screenname):
        # open Screen by name (String)
        self.screens[screenname].screenframe.tkraise()

    def scale(self):
        # calculate difference between minimal size and actual size
        # so the right scale can be calculated with individual size on startup
        # ox, oy: offset width (ox) and offset height (oy)
        ox = int(self.windowframe.winfo_width()) - self.config["min_width"]
        oy = int(self.windowframe.winfo_height()) - self.config["min_height"]
        # scale GUI elements from Mainframe, Actionbar and Infobar
        self.actionbar.place(x=0, y=0, height=50, width=800 + ox)
        self.logo.update(offsetx=ox, offsety=0)
        self.infobar.place(x=0, y=576 + oy, height=24, width=800 + ox)
        self.icon_clock.update(offsetx=ox, offsety=0)
        self.lbl_timestamp.place(x=690 + ox, y=0, width=150, height=24)
        self.btn_exit.place(x=695 + ox, y=0, width=50, height=50)
        # scale GUI elements from all the other Screens
        for screen in self.screens:
            self.screens[screen].scale(ox, oy)


class ScreenStart:
    def __init__(self, master):
        self.master = master
        self.screenframe = ttk.Frame(master=self.master.mainframe, style="TFrame")
        self.screenframe.place(x=0, y=50, height=526, width=800)

        # create and place screenframe background
        self.background = tk.Canvas(master=self.screenframe,
                                    relief="flat",
                                    bg=self.master.color_bg_contrast,
                                    highlightthickness=0,
                                    highlightbackground="black")
        self.background.place(x=0, y=0, height=1080, width=1924)

        self.lbl_start = ttk.Label(master=self.background,
                                   style="TLabel",
                                   text="Startscreen",
                                   anchor="w")
        self.lbl_start.place(x=400, y=400, width=150, height=25)

    def scale(self, ox, oy):
        # scale GUI elements
        # ox, oy: offset width (ox) and offset height (oy)
        self.screenframe.place(x=0, y=50, height=526 + oy, width=800 + ox)
        self.background.place(x=0, y=0, height=1080 + oy, width=1924 + ox)


class ScreenPLC:
    def __init__(self, master):
        self.master = master
        self.screenframe = ttk.Frame(master=self.master.mainframe, style="TFrame")
        self.screenframe.place(x=0, y=50, height=526, width=800)

        # create and place screenframe background
        self.background = tk.Canvas(master=self.screenframe,
                                    relief="flat",
                                    bg=self.master.color_bg_contrast,
                                    highlightthickness=0,
                                    highlightbackground="black")
        self.background.place(x=0, y=0, height=1080, width=1924)

        self.lbl_plc = ttk.Label(master=self.background,
                                 style="TLabel",
                                 text="PLCscreen",
                                 anchor="w")
        self.lbl_plc.place(x=400, y=400, width=150, height=25)

    def scale(self, ox, oy):
        # scale GUI elements
        # ox, oy: offset width (ox) and offset height (oy)
        self.screenframe.place(x=0, y=50, height=526 + oy, width=800 + ox)
        self.background.place(x=0, y=0, height=1080 + oy, width=1924 + ox)


class ScreenData:
    def __init__(self, master):
        self.master = master
        self.screenframe = ttk.Frame(master=self.master.mainframe, style="TFrame")
        self.screenframe.place(x=0, y=50, height=526, width=800)

        # create and place screenframe background
        self.background = tk.Canvas(master=self.screenframe,
                                    relief="flat",
                                    bg=self.master.color_bg_contrast,
                                    highlightthickness=0,
                                    highlightbackground="black")
        self.background.place(x=0, y=0, height=1080, width=1924)

        # create and place treeview for data structure
        self.datatree = ttk.Treeview(self.screenframe)
        self.datatree["columns"] = ("Datentyp", "Kommentar")
        self.datatree.column("#0", width=200, minwidth=100, stretch=tk.NO)
        self.datatree.column("Datentyp", width=200, minwidth=100, stretch=tk.NO)
        self.datatree.column("Kommentar", width=200, minwidth=100, stretch=tk.YES)
        self.datatree.heading("#0", text="Name", anchor=tk.W)
        self.datatree.heading("Datentyp", text="Datentyp", anchor=tk.W)
        self.datatree.heading("Kommentar", text="Kommentar", anchor=tk.W)
        self.datatree.place(x=50, y=200, height=324, width=690)
        # add scrollbar to treeview
        self.datatree_scrollx = ttk.Scrollbar(self.screenframe, orient="horizontal", command=self.datatree.xview)
        self.datatree_scrollx.place(x=50, y=475, width=691)
        self.datatree_scrolly = ttk.Scrollbar(self.screenframe, orient="vertical", command=self.datatree.yview)
        self.datatree_scrolly.place(x=740, y=152, height=337)
        self.datatree.configure(xscrollcommand=self.datatree_scrollx.set)
        self.datatree.configure(yscrollcommand=self.datatree_scrolly.set)

        for x in range(0, 100):
            self.datatree.insert("", "end", text="photo1.png", values=("23-Jun-17 11:28", "PNG file", "2.6 KB"))

    def scale(self, ox, oy):
        # scale GUI elements
        # ox, oy: offset width (ox) and offset height (oy)
        self.screenframe.place(x=0, y=50, height=526 + oy, width=800 + ox)
        self.background.place(x=0, y=0, height=1080 + oy, width=1924 + ox)
        self.datatree.place(x=50, y=150, height=325 + oy, width=691 + ox)
        self.datatree_scrollx.place(x=50, y=475 + oy, width=691 + ox)
        self.datatree_scrolly.place(x=740 + ox, y=152, height=337 + oy)


class ScreenSetup:
    def __init__(self, master):
        self.master = master
        self.screenframe = ttk.Frame(master=self.master.mainframe, style="TFrame")
        self.screenframe.place(x=0, y=50, height=526, width=800)

        # create and place screenframe background
        self.background = tk.Canvas(master=self.screenframe,
                                    relief="flat",
                                    bg=self.master.color_bg_contrast,
                                    highlightthickness=0,
                                    highlightbackground="black")
        self.background.place(x=0, y=0, height=1080, width=1924)

        self.lbl_setup = ttk.Label(master=self.background,
                                   style="TLabel",
                                   text="Setupscreen",
                                   anchor="w")
        self.lbl_setup.place(x=400, y=400, width=150, height=25)

    def scale(self, ox, oy):
        # scale GUI elements
        # ox, oy: offset width (ox) and offset height (oy)
        self.screenframe.place(x=0, y=50, height=526 + oy, width=800 + ox)
        self.background.place(x=0, y=0, height=1080 + oy, width=1924 + ox)
