import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path


class Led:  # LED with color, color changes by String
    def __init__(self, master, posx, posy, diameter, framewidth,
                 framecolor, ledcolor):
        self.root = master
        self.ledcolor = ledcolor
        self.framecolor = framecolor
        self.diameter = diameter
        self.framewidth = framewidth
        self.offsetx = 0
        self.offsety = 0
        self.led = self.root.create_oval(
            posx, posy, posx + self.diameter, posy + self.diameter,
            width=self.framewidth, fill=self.ledcolor, outline=self.framecolor)

    def update(self, offsetx=0, offsety=0):
        differenzx = offsetx - self.offsetx
        differenzy = offsety - self.offsety
        self.offsetx = self.offsetx + differenzx
        self.offsety = self.offsety + differenzy
        self.root.move(self.led, differenzx, differenzy)

    def colorchange(self, ledcolor="yellow", framecolor="black"):
        self.ledcolor = ledcolor
        self.framecolor = framecolor
        self.root.itemconfig(self.led,
                             fill=self.ledcolor,
                             outline=self.framecolor)


class View:
    def __init__(self, controller, config, parameter):
        self.controller = controller
        self.model = None
        self.config = config
        self.parameter = parameter

        # other variables------------------------------------------------------
        self.desktoppath = os.path.expanduser(r"~\Desktop")

        # general window settings----------------------------------------------
        # set title
        self.window = tk.Tk()
        self.window.title(self.config["title"])

        # set window icon
        icon = tk.PhotoImage(file=Path(self.config["media_icon"]))
        self.window.iconphoto(True, icon)

        # set min/max windowsize
        self.window.wm_minsize(self.config["min_width"], self.config["min_height"])
        self.window.wm_maxsize(self.config["max_width"], self.config["max_height"])

        # set window startposisiton and startsize
        # window zoomed without titlebar optional
        self.window_size()

        # style settings-general-----------------------------------------------
        # load tkinter ttk style theme
        self.window.tk.call("lappend", "auto_path", Path(self.config["style_themepath"]))
        self.window.tk.call("package", "require", Path(self.config["style_themename"]))
        self.style_main = ttk.Style()
        self.style_main.theme_use(Path(self.config["style_themename"]))
        # copy colorcodes
        self.color_btn_fg_main = self.style_main.lookup('TButton', 'foreground')
        self.color_btn_bg_main = self.style_main.lookup('TButton', 'background')
        self.color_bg_contrast = "#3d4145"

        # mainframe------------------------------------------------------------
        # set mainframe for window
        self.mainframe = ttk.Frame(master=self.window, style="TFrame")
        # set mainframe to max size
        self.mainframe.place(x=0, y=0, height=self.config["max_height"], width=self.config["max_width"])

        # load icons-----------------------------------------------------------
        self.img_home = tk.PhotoImage(file=Path(self.config["media_home"]))
        self.img_plc = tk.PhotoImage(file=Path(self.config["media_plc"]))
        self.img_data = tk.PhotoImage(file=Path(self.config["media_data"]))
        self.img_setup = tk.PhotoImage(file=Path(self.config["media_setup"]))
        self.img_logo = tk.PhotoImage(file=Path(self.config["media_logo"]))
        self.icon_exit = tk.PhotoImage(file=Path(self.config["media_exit"]))
        self.img_clock = tk.PhotoImage(file=Path(self.config["media_clock"]))
        self.img_version = tk.PhotoImage(file=Path(self.config["media_version"]))

        # style customisation--------------------------------------------------
        # actionbar
        self.style_btn_actionbar = ttk.Style()
        self.style_btn_actionbar.configure(
            "style_actionbar.TButton", font=("arial", 8), relief="flat")
        self.style_btn_actionbar.map(
            "style_actionbar.TButton", background=[('selected', self.color_bg_contrast), ('active', "#000000")])
        # infobar
        self.style_lbl_infobar = ttk.Style()
        self.style_lbl_infobar.configure(
            "style_infobar.TLabel", foreground=self.color_btn_fg_main, background=self.color_btn_bg_main)
        # screen
        self.style_btn_screen = ttk.Style()
        self.style_btn_screen.configure(
            "style_screen.TButton", font=("arial", 10), relief="flat")
        self.style_btn_screen.map(
            "style_screen.TButton", background=[('selected', self.color_bg_contrast), ('active', "#000000")])
        self.style_lbl_screen = ttk.Style()
        self.style_lbl_screen.configure(
            "style_screen.TLabel", font=("arial", 10), relief="flat", background=self.color_btn_bg_main)
        self.style_text_screen = ttk.Style()
        self.style_text_screen.configure(
            "style_text_screen.TLabel", font=("arial", 10), relief="flat", background=self.color_bg_contrast)
        self.style_cbx_screen = ttk.Style()
        self.style_cbx_screen.configure(
            "style_screen.TCheckbutton", font=("arial", 10), relief="flat", background=self.color_bg_contrast)
        self.style_screen = ttk.Style()
        self.style_screen.configure(
            "style_screen.TFrame", background=self.color_bg_contrast)
        self.style_nb_screen = ttk.Style()
        self.style_nb_screen.configure(
            "style_screen.TNotebook", background=self.color_btn_bg_main, relief="flat")
        self.style_nb_screen.configure(
            "style_screen.TNotebook.Tab", focuscolor=self.style_nb_screen.configure(".")["background"])
        self.style_nb_screen.map(
            "style_screen.TNotebook.Tab", background=[('selected', self.color_bg_contrast), ('active', "#000000")])
        self.style_treeview = ttk.Style()
        self.style_treeview.configure(
            "Treeview.Heading", font=("arial", 10))

        # create Tabs----------------------------------------------------------
        self.screens = ttk.Notebook(self.mainframe, style="style_screen.TNotebook")
        self.screen_home = ttk.Frame(self.screens, style="style_screen.TFrame")
        self.screen_plc = ttk.Frame(self.screens, style="style_screen.TFrame")
        self.screen_data = ttk.Frame(self.screens, style="style_screen.TFrame")
        self.screen_setup = ttk.Frame(self.screens, style="style_screen.TFrame")
        self.screens.add(self.screen_home, text="Home", image=self.img_home, compound=tk.TOP)
        self.screens.add(self.screen_plc, text="PLC", image=self.img_plc, compound=tk.TOP)
        self.screens.add(self.screen_data, text="Data", image=self.img_data, compound=tk.TOP)
        self.screens.add(self.screen_setup, text="Setup", image=self.img_setup, compound=tk.TOP)

        # menubar--------------------------------------------------------------
        self.menu = tk.Menu(self.window)
        self.window.config(menu=self.menu)
        self.window.option_add('*tearOff', False)
        # file menu
        self.filemenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="New", command=self.controller.file_new)
        self.filemenu.add_command(label="Open", command=self.controller.file_open)
        self.filemenu.add_command(label="Save", command=self.controller.file_save)
        self.filemenu.add_command(label="Save As", command=self.controller.file_saveas)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.controller.stop)
        # help menu
        self.helpmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label="About", command=self.about_show)

        # actionbar------------------------------------------------------------
        # create and place exit button on actionbar
        self.btn_exit = ttk.Button(master=self.mainframe,
                                   takefocus=0,
                                   text="Exit",
                                   compound=tk.TOP,
                                   image=self.icon_exit,
                                   style="style_actionbar.TButton")

        # create and place Logo on top
        self.icon_logo = tk.Canvas(master=self.mainframe, relief="flat", highlightthickness=0)
        self.icon_logo.create_image(0, 0, image=self.img_logo, anchor="nw")

        # infobar--------------------------------------------------------------
        # create and place infobar on mainframe
        self.infobar = tk.Canvas(master=self.mainframe,
                                 relief="flat",
                                 bg=self.color_btn_bg_main,
                                 highlightthickness=0,
                                 highlightbackground="black")

        # create and place clock and timestamp on infobar
        self.icon_clock = tk.Canvas(master=self.infobar,
                                    relief="flat",
                                    highlightthickness=0,
                                    bg=self.color_btn_bg_main)
        self.icon_clock.create_image(0, 0, image=self.img_clock, anchor="nw")

        self.timestamp = tk.StringVar()
        self.lbl_timestamp = ttk.Label(master=self.infobar,
                                       style="style_infobar.TLabel",
                                       textvariable=self.timestamp,
                                       anchor="w")

        # create and place LED and label for PLC state on infobar
        self.led_plc = Led(master=self.infobar,
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

        # create and place versionnumber and icon on infobar
        self.icon_version = tk.Canvas(master=self.infobar,
                                      relief="flat",
                                      highlightthickness=0,
                                      bg=self.color_btn_bg_main)
        self.icon_version.create_image(0, 0, image=self.img_version, anchor="nw")

        self.version = tk.StringVar()
        self.version.set(self.config["version"])
        self.lbl_version = ttk.Label(master=self.infobar,
                                     style="style_infobar.TLabel",
                                     textvariable=self.version,
                                     anchor="w")

        # screen data----------------------------------------------------------
        # create frame on screen data for UDT name + description + version + info
        # create and place label for UDT name
        self.udt_infos = tk.Canvas(master=self.screen_data,
                                   relief="flat",
                                   highlightthickness=0,
                                   bg=self.color_bg_contrast)

        self.udt_name = tk.StringVar()
        self.lbl_udt_name_info = ttk.Label(master=self.udt_infos,
                                           style="style_screen.TLabel",
                                           text="Name:",
                                           anchor="w")

        self.lbl_udt_name = ttk.Label(master=self.udt_infos,
                                      style="style_screen.TLabel",
                                      textvariable=self.udt_name,
                                      anchor="w")

        # create and place label for UDT description
        self.udt_description = tk.StringVar()
        self.lbl_udt_description_info = ttk.Label(master=self.udt_infos,
                                                  style="style_screen.TLabel",
                                                  text="Beschreibung:",
                                                  anchor="w")

        self.lbl_udt_description = ttk.Label(master=self.udt_infos,
                                             style="style_screen.TLabel",
                                             textvariable=self.udt_description,
                                             anchor="w")

        # create and place label for UDT version
        self.udt_version = tk.StringVar()
        self.lbl_udt_version_info = ttk.Label(master=self.udt_infos,
                                              style="style_screen.TLabel",
                                              text="Version:",
                                              anchor="w")

        self.lbl_udt_version = ttk.Label(master=self.udt_infos,
                                         style="style_screen.TLabel",
                                         textvariable=self.udt_version,
                                         anchor="w")

        # create and place label for UDT info
        self.udt_info = tk.StringVar()
        self.lbl_udt_info_info = ttk.Label(master=self.udt_infos,
                                           style="style_screen.TLabel",
                                           text="Info:",
                                           anchor="w")

        self.lbl_udt_info = ttk.Label(master=self.udt_infos,
                                      style="style_screen.TLabel",
                                      textvariable=self.udt_info,
                                      anchor="w")

        # create and place treeview for data structure
        self.datatree = ttk.Treeview(self.screen_data)
        self.datatree["columns"] = ("Datentyp", "Kommentar")
        self.datatree.column("#0", width=200, minwidth=100, stretch=tk.NO)
        self.datatree.column("Datentyp", width=200, minwidth=100, stretch=tk.NO)
        self.datatree.column("Kommentar", width=200, minwidth=100, stretch=tk.YES)
        self.datatree.heading("#0", text="Name", anchor=tk.W)
        self.datatree.heading("Datentyp", text="Datentyp", anchor=tk.W)
        self.datatree.heading("Kommentar", text="Kommentar", anchor=tk.W)
        # add scrollbar to treeview
        self.datatree_scrollx = ttk.Scrollbar(self.screen_data, orient="horizontal", command=self.datatree.xview)
        self.datatree_scrolly = ttk.Scrollbar(self.screen_data, orient="vertical", command=self.datatree.yview)
        self.datatree.configure(xscrollcommand=self.datatree_scrollx.set)
        self.datatree.configure(yscrollcommand=self.datatree_scrolly.set)

        # create button for datasructure import
        self.btn_import_datasructure = ttk.Button(master=self.screen_data,
                                                  takefocus=0,
                                                  text='Datenstruktur einlesen',
                                                  style="style_screen.TButton")

        # screen setup---------------------------------------------------------
        # create checkbox for option fullscreen
        self.opt_fullscreen = tk.BooleanVar()
        self.opt_fullscreen.set(self.parameter["opt_fullscreen"])
        self.cbx_fullscreen = ttk.Checkbutton(master=self.screen_setup,
                                              text="Fullscreen",
                                              variable=self.opt_fullscreen,
                                              command=self.controller.window_fullscreen,
                                              style="style_screen.TCheckbutton")

    def window_scale(self):
        # calculate difference between minimal size and actual size
        # so the right scale can be calculated with individual size on startup
        # ox, oy: offset width (ox) and offset height (oy)
        ox = int(self.window.winfo_width()) - self.config["min_width"]
        oy = int(self.window.winfo_height()) - self.config["min_height"]
        # scale GUI elements from Mainframe
        self.screens.place(x=0, y=0, width=802 + ox, height=578 + oy)
        self.btn_exit.place(x=623 + ox, y=0, width=58, height=58)
        self.icon_logo.place(x=687 + ox, y=0, width=114, height=58)
        self.infobar.place(x=0, y=576 + oy, height=24, width=800 + ox)
        self.icon_clock.place(x=670 + ox, y=2, height=20, width=20)
        self.lbl_timestamp.place(x=690 + ox, y=0, width=150, height=24)
        self.lbl_led_plc.place(x=270, y=2, width=50, height=18)
        self.icon_version.place(x=5, y=2, height=20, width=20)
        self.lbl_version.place(x=25, y=2, width=150, height=18)
        # scale GUI elements from screen data
        self.udt_infos.place(x=50, y=25, height=58, width=690 + ox)
        self.lbl_udt_name_info.place(x=0, y=0, width=50, height=25)
        self.lbl_udt_name.place(x=50, y=0, width=250, height=25)
        self.lbl_udt_description_info.place(x=330, y=0, width=85, height=25)
        self.lbl_udt_description.place(x=415, y=0, width=500 + ox, height=25)
        self.lbl_udt_version_info.place(x=0, y=33, width=50, height=25)
        self.lbl_udt_version.place(x=50, y=33, width=250, height=25)
        self.lbl_udt_info_info.place(x=330, y=33, width=85, height=25)
        self.lbl_udt_info.place(x=415, y=33, width=500 + ox, height=25)
        # scale Gui elements from treeview
        self.datatree.place(x=50, y=90, height=325 + oy, width=691 + ox)
        self.datatree_scrollx.place(x=50, y=415 + oy, width=691 + ox)
        self.datatree_scrolly.place(x=740 + ox, y=92, height=337 + oy)
        self.btn_import_datasructure.place(x=50, y=437 + oy, height=30, width=150)
        # scale Gui elements from screen setup
        self.cbx_fullscreen.place(x=50, y=25)
        return self.window.winfo_width(), self.window.winfo_height()

    def window_size(self):
        if self.parameter["opt_fullscreen"]:
            self.window.overrideredirect(True)
            self.window.state("zoomed")
        else:
            self.window.overrideredirect(False)
            self.window.state("normal")
            # set window startposisiton and startsize
            screenwidth = self.window.winfo_screenwidth()
            screenheight = self.window.winfo_screenheight()
            windowwidth = self.parameter["opt_windowwidth"]
            windowheight = self.parameter["opt_windowheight"]
            windowstartposx = (screenwidth / 2) - (windowwidth / 2)
            windowstartposy = (screenheight / 2) - (windowheight / 2)
            self.window.geometry("%dx%d+%d+%d" % (windowwidth, windowheight, windowstartposx, windowstartposy))

    def filepath_open(self, message=None, filetypes=((), ("all files", "*.*"))):
        if message is not None:
            tk.messagebox.showinfo(title=None, message=message)
        path = tk.filedialog.askopenfilename(initialdir=self.desktoppath, title="select File",
                                             filetypes=filetypes)
        return path

    def filepath_saveas(self, filetypes=((), ("all files", "*.*"))):
        path = tk.filedialog.asksaveasfilename(initialdir=self.desktoppath, title="Save as...",
                                               filetypes=filetypes,
                                               defaultextension=filetypes[0][1])
        return path

    def about_show(self):
        version = self.config["version"]
        name = self.config["customer_name"]
        mail = self.config["customer_mail"]
        message = "{version}\n{name}\n{mail}".format(version=version, name=name, mail=mail)
        tk.messagebox.showinfo(title="About", message=message)

    def datatree_clear(self):
        for element in self.datatree.get_children():
            self.datatree.delete(element)
        self.udt_name.set("")
        self.udt_description.set("")
        self.udt_version.set("")
        self.udt_info.set("")

    def datatree_fill(self, name, description, version, info, data):
        self.udt_name.set(name)
        self.udt_description.set(description)
        self.udt_version.set(version)
        self.udt_info.set(info)
        # check every element,
        folderpath = ["", ""]
        for element in data:
            # put actual data in datatree in the actual folder
            name = element["name"]
            datatype = element["datatype"]
            comment = element["comment"]
            visible = element["visible"]
            action = element["action"]
            # insert element if element has "visible" flag
            if visible:
                data = self.datatree.insert(folderpath[-1], "end", text=name, values=(datatype, comment))
            # open new folder if element has "open" flag
            if action == "open":
                # save name to folderpath
                folderpath.append(data)
            # close folder if element has "close" flag
            elif action == "close":
                # delete name from folderpath
                folderpath.pop()
            # else keep folder
            else:
                pass
