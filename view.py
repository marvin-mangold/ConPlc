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
    def __init__(self, controller, config):
        self.controller = controller
        self.model = None
        self.config = config

        # other variables------------------------------------------------------
        self.desktoppath = os.path.expanduser(r"~\Desktop")

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
        # actionbar
        self.style_btn_actionbar = ttk.Style()
        self.style_btn_actionbar.configure("style_actionbar.TButton",
                                           font=("arial", 8),
                                           relief="flat")
        # infobar
        self.style_lbl_infobar = ttk.Style()
        self.style_lbl_infobar.configure("style_infobar.TLabel",
                                         foreground=self.color_btn_fg_main,
                                         background=self.color_btn_bg_main)
        # screen
        self.style_btn_screen = ttk.Style()
        self.style_btn_screen.configure("style_screen.TButton",
                                        font=("arial", 10),
                                        relief="flat")
        self.style_lbl_screen = ttk.Style()
        self.style_lbl_screen.configure("style_screen.TLabel",
                                        font=("arial", 10),
                                        relief="flat",
                                        background=self.color_btn_bg_main)
        self.style_text_screen = ttk.Style()
        self.style_text_screen.configure("style_text_screen.TLabel",
                                         font=("arial", 10),
                                         relief="flat",
                                         background=self.color_bg_contrast)
        self.style_btn_screen = ttk.Style()
        self.style_btn_screen.configure("style_screen.TFrame",
                                        background=self.color_bg_contrast)
        self.style_btn_screen = ttk.Style()
        self.style_btn_screen.configure("style_screen.TNotebook",
                                        background=self.color_btn_bg_main,
                                        relief="flat")
        self.style_treeview = ttk.Style()
        self.style_treeview.configure("Treeview.Heading",
                                      font=("arial", 10))

        # create Tabs----------------------------------------------------------
        self.screens = ttk.Notebook(self.mainframe, style="style_screen.TNotebook")
        self.screen_home = ttk.Frame(self.screens, style="style_screen.TFrame")
        self.screen_plc = ttk.Frame(self.screens, style="style_screen.TFrame")
        self.screen_data = ttk.Frame(self.screens, style="style_screen.TFrame")
        self.screen_setup = ttk.Frame(self.screens, style="style_screen.TFrame")
        self.img_home = tk.PhotoImage(file=Path(self.config["Media_home"]))
        self.img_plc = tk.PhotoImage(file=Path(self.config["Media_plc"]))
        self.img_data = tk.PhotoImage(file=Path(self.config["Media_data"]))
        self.img_setup = tk.PhotoImage(file=Path(self.config["Media_setup"]))
        self.screens.add(self.screen_home, text="Home", image=self.img_home, compound=tk.TOP)
        self.screens.add(self.screen_plc, text="PLC", image=self.img_plc, compound=tk.TOP)
        self.screens.add(self.screen_data, text="Data", image=self.img_data, compound=tk.TOP)
        self.screens.add(self.screen_setup, text="Setup", image=self.img_setup, compound=tk.TOP)
        self.screens.place(x=0, y=0, width=802, height=578)

        # actionbar------------------------------------------------------------
        # create and place exit button on actionbar
        self.icon_exit = tk.PhotoImage(file=Path(self.config["Media_exit"]))
        self.btn_exit = ttk.Button(master=self.mainframe,
                                   takefocus=0,
                                   text="Exit",
                                   compound=tk.TOP,
                                   image=self.icon_exit,
                                   style="style_actionbar.TButton")
        self.btn_exit.place(x=679, y=0, width=58, height=58)

        # create and place Logo on top
        self.img_logo = tk.PhotoImage(file=Path(self.config["Media_logo"]))
        self.icon_logo = tk.Canvas(master=self.mainframe, relief="flat", highlightthickness=0)
        self.icon_logo.create_image(0, 0, image=self.img_logo, anchor="nw")
        self.icon_logo.place(x=743, y=0, height=58, width=58)

        # infobar--------------------------------------------------------------
        # create and place infobar on mainframe
        self.infobar = tk.Canvas(master=self.mainframe,
                                 relief="flat",
                                 bg=self.color_btn_bg_main,
                                 highlightthickness=0,
                                 highlightbackground="black")
        self.infobar.place(x=0, y=576, height=24, width=800)

        # create and place clock and timestamp on infobar
        self.img_clock = tk.PhotoImage(file=Path(self.config["Media_clock"]))
        self.icon_clock = tk.Canvas(master=self.infobar, relief="flat", highlightthickness=0, bg=self.color_btn_bg_main)
        self.icon_clock.create_image(0, 0, image=self.img_clock, anchor="nw")
        self.icon_clock.place(x=670, y=2, height=20, width=20)

        self.timestamp = tk.StringVar()
        self.lbl_timestamp = ttk.Label(master=self.infobar,
                                       style="style_infobar.TLabel",
                                       textvariable=self.timestamp,
                                       anchor="w")
        self.lbl_timestamp.place(x=690, y=0, width=150, height=24)

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
        self.lbl_led_plc.place(x=270, y=2, width=50, height=18)

        # create and place versionnumber and icon on infobar
        self.img_version = tk.PhotoImage(file=Path(self.config["Media_version"]))
        self.icon_version = tk.Canvas(master=self.infobar,
                                      relief="flat",
                                      highlightthickness=0,
                                      bg=self.color_btn_bg_main)
        self.icon_version.create_image(0, 0, image=self.img_version, anchor="nw")
        self.icon_version.place(x=5, y=2, height=20, width=20)

        self.version = tk.StringVar()
        self.version.set(self.config["version"])
        self.lbl_version = ttk.Label(master=self.infobar,
                                     style="style_infobar.TLabel",
                                     textvariable=self.version,
                                     anchor="w")
        self.lbl_version.place(x=25, y=2, width=150, height=18)

        # screen data----------------------------------------------------------
        # create and place treeview for data structure
        self.datatree = ttk.Treeview(self.screen_data)
        self.datatree["columns"] = ("Datentyp", "Kommentar")
        self.datatree.column("#0", width=200, minwidth=100, stretch=tk.NO)
        self.datatree.column("Datentyp", width=200, minwidth=100, stretch=tk.NO)
        self.datatree.column("Kommentar", width=200, minwidth=100, stretch=tk.YES)
        self.datatree.heading("#0", text="Name", anchor=tk.W)
        self.datatree.heading("Datentyp", text="Datentyp", anchor=tk.W)
        self.datatree.heading("Kommentar", text="Kommentar", anchor=tk.W)
        self.datatree.place(x=50, y=140, height=324, width=690)
        # add scrollbar to treeview
        self.datatree_scrollx = ttk.Scrollbar(self.screen_data, orient="horizontal", command=self.datatree.xview)
        self.datatree_scrollx.place(x=50, y=465, width=691)
        self.datatree_scrolly = ttk.Scrollbar(self.screen_data, orient="vertical", command=self.datatree.yview)
        self.datatree_scrolly.place(x=740, y=142, height=337)
        self.datatree.configure(xscrollcommand=self.datatree_scrollx.set)
        self.datatree.configure(yscrollcommand=self.datatree_scrolly.set)

        # create button for datasructure import
        self.btn_import_datasructure = ttk.Button(master=self.screen_data,
                                                  takefocus=0,
                                                  text='Datenstruktur einlesen',
                                                  style="style_screen.TButton")
        self.btn_import_datasructure.place(x=50, y=650, height=30, width=150)

        # create frame on screen data for UDT name + description + version + info
        # create and place label for UDT name
        self.udt_infos = tk.Canvas(master=self.screen_data,
                                   relief="flat",
                                   highlightthickness=0,
                                   bg=self.color_bg_contrast)
        self.udt_infos.place(x=50, y=75, height=58, width=690)

        self.udt_name = tk.StringVar()
        self.lbl_udt_name_info = ttk.Label(master=self.udt_infos,
                                           style="style_screen.TLabel",
                                           text="Name:",
                                           anchor="w")
        self.lbl_udt_name_info.place(x=0, y=0, width=50, height=25)
        self.lbl_udt_name = ttk.Label(master=self.udt_infos,
                                      style="style_screen.TLabel",
                                      textvariable=self.udt_name,
                                      anchor="w")
        self.lbl_udt_name.place(x=50, y=0, width=250, height=25)

        # create and place label for UDT description
        self.udt_description = tk.StringVar()
        self.lbl_udt_description_info = ttk.Label(master=self.udt_infos,
                                                  style="style_screen.TLabel",
                                                  text="Beschreibung:",
                                                  anchor="w")
        self.lbl_udt_description_info.place(x=330, y=0, width=85, height=25)
        self.lbl_udt_description = ttk.Label(master=self.udt_infos,
                                             style="style_screen.TLabel",
                                             textvariable=self.udt_description,
                                             anchor="w")
        self.lbl_udt_description.place(x=415, y=0, width=500, height=25)

        # create and place label for UDT version
        self.udt_version = tk.StringVar()
        self.lbl_udt_version_info = ttk.Label(master=self.udt_infos,
                                              style="style_screen.TLabel",
                                              text="Version:",
                                              anchor="w")
        self.lbl_udt_version_info.place(x=0, y=33, width=50, height=25)
        self.lbl_udt_version = ttk.Label(master=self.udt_infos,
                                         style="style_screen.TLabel",
                                         textvariable=self.udt_version,
                                         anchor="w")
        self.lbl_udt_version.place(x=50, y=33, width=250, height=25)

        # create and place label for UDT info
        self.udt_info = tk.StringVar()
        self.lbl_udt_info_info = ttk.Label(master=self.udt_infos,
                                           style="style_screen.TLabel",
                                           text="Info:",
                                           anchor="w")
        self.lbl_udt_info_info.place(x=330, y=33, width=85, height=25)
        self.lbl_udt_info = ttk.Label(master=self.udt_infos,
                                      style="style_screen.TLabel",
                                      textvariable=self.udt_info,
                                      anchor="w")
        self.lbl_udt_info.place(x=415, y=33, width=500, height=25)

    def scale(self):
        # calculate difference between minimal size and actual size
        # so the right scale can be calculated with individual size on startup
        # ox, oy: offset width (ox) and offset height (oy)
        ox = int(self.windowframe.winfo_width()) - self.config["min_width"]
        oy = int(self.windowframe.winfo_height()) - self.config["min_height"]
        # scale GUI elements from Mainframe
        self.screens.place(x=0, y=0, width=802 + ox, height=578 + oy)
        self.btn_exit.place(x=679 + ox, y=0, width=58, height=58)
        self.icon_logo.place(x=743 + ox, y=0, height=58, width=58)
        self.infobar.place(x=0, y=576 + oy, height=24, width=800 + ox)
        self.icon_clock.place(x=670 + ox, y=2, height=20, width=20)
        self.lbl_timestamp.place(x=690 + ox, y=0, width=150, height=24)
        # scale GUI elements from screen data
        self.datatree.place(x=50, y=140, height=325 + oy, width=691 + ox)
        self.datatree_scrollx.place(x=50, y=465 + oy, width=691 + ox)
        self.datatree_scrolly.place(x=740 + ox, y=142, height=337 + oy)

    def get_filepath(self, message=None):
        if message is not None:
            tk.messagebox.showinfo(title=None, message=message)
        path = tk.filedialog.askopenfilename(initialdir=self.desktoppath, title="UDT auswählen",
                                             filetypes=(("UDT Files", "*.udt"),))
        return path

    def clear_udt_data(self):
        for element in self.datatree.get_children():
            self.datatree.delete(element)
        self.udt_name.set("")
        self.udt_description.set("")
        self.udt_version.set("")
        self.udt_info.set("")

    def fill_udt_data(self, name, description, version, info, data):
        self.udt_name.set(name)
        self.udt_description.set(description)
        self.udt_version.set(version)
        self.udt_info.set(info)
        # check every element,
        # if element is standard datatype --> insert
        # elif element is special datatype --> insert in folder
        depth = 0
        depthlist = [""]
        elementlist = []
        for element in data:
            # open new folder if structure depth increases
            if element[0] > depth:
                # mark last data as folder
                depthlist.append(elementlist[-1])
            # close folder if structure depth decreases
            elif element[0] < depth:
                # unmark last folder
                depthlist.pop()
            # else keep folder
            else:
                pass
            # put actual data in datatree in the actual folder
            data = self.datatree.insert(depthlist[-1], "end", text=element[1], values=(element[2], element[3]))
            # save actual data in list
            elementlist.append(data)
            # buffer actual structure depth for next loop
            depth = element[0]
