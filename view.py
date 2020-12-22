"""
Wicke PLC - connect PLC and PC
Copyright (C) 2020  Marvin Mangold

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

import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path


class View(object):
    def __init__(self, controller, configfile, projectfile):
        self.controller = controller
        self.configfile = configfile
        self.projectfile = projectfile

        # other variables------------------------------------------------------
        self.desktoppath = os.path.expanduser(r"~\Desktop")

        # general window settings----------------------------------------------
        # create window
        self.window = tk.Tk()

        # load icons
        self.img_icon = tk.PhotoImage(file=Path(self.configfile["media_icon"]))
        self.img_home = tk.PhotoImage(file=Path(self.configfile["media_home"]))
        self.img_plc = tk.PhotoImage(file=Path(self.configfile["media_plc"]))
        self.img_data = tk.PhotoImage(file=Path(self.configfile["media_data"]))
        self.img_setup = tk.PhotoImage(file=Path(self.configfile["media_setup"]))
        self.img_logo = tk.PhotoImage(file=Path(self.configfile["media_logo"]))
        self.icon_exit = tk.PhotoImage(file=Path(self.configfile["media_exit"]))
        self.img_clock = tk.PhotoImage(file=Path(self.configfile["media_clock"]))
        self.img_version = tk.PhotoImage(file=Path(self.configfile["media_version"]))
        self.img_led_gn = tk.PhotoImage(file=Path(self.configfile["media_led_gn"]))
        self.img_led_ye = tk.PhotoImage(file=Path(self.configfile["media_led_ye"]))
        self.img_led_rd = tk.PhotoImage(file=Path(self.configfile["media_led_rd"]))

        # set title
        self.window_title("default.wplc")

        # set icon
        self.window.iconphoto(True, self.img_icon)

        # set min/max windowsize
        self.window.wm_minsize(self.configfile["min_width"], self.configfile["min_height"])
        self.window.wm_maxsize(self.configfile["max_width"], self.configfile["max_height"])

        # style settings-general-----------------------------------------------
        # load tkinter ttk style theme
        self.window.tk.call("lappend", "auto_path", Path(self.configfile["style_themepath"]))
        self.window.tk.call("package", "require", Path(self.configfile["style_themename"]))
        self.style_main = ttk.Style()
        self.style_main.theme_use(Path(self.configfile["style_themename"]))

        # mainframe------------------------------------------------------------
        # set mainframe for window
        self.mainframe = ttk.Frame(master=self.window, style="TFrame")
        # set mainframe to max size
        self.mainframe.place(x=0, y=0, height=self.configfile["max_height"], width=self.configfile["max_width"])

        # style customisation--------------------------------------------------
        # define main colors
        self.backcolor = self.style_main.lookup('TButton', 'background')
        self.midcolor = "#3d4145"
        self.frontcolor = self.style_main.lookup('TTreeview', 'background')
        self.textcolor = self.style_main.lookup('TButton', 'foreground')
        # actionbar
        self.style_btn_actionbar = ttk.Style()
        self.style_btn_actionbar.configure(
            "style_actionbar.TButton", font=("arial", 8), relief="flat")
        self.style_btn_actionbar.map(
            "style_actionbar.TButton", background=[('selected', self.midcolor), ('active', "#000000")])
        # infobar
        self.style_lbl_infobar = ttk.Style()
        self.style_lbl_infobar.configure(
            "style_infobar.TLabel", foreground=self.textcolor, background=self.backcolor)
        # screen
        self.style_btn_screen = ttk.Style()
        self.style_btn_screen.configure(
            "style_screen.TButton", font=("arial", 10), relief="flat")
        self.style_btn_screen.map(
            "style_screen.TButton", background=[('selected', self.midcolor), ('active', "#000000")])
        self.style_lbl_screen = ttk.Style()
        self.style_lbl_screen.configure(
            "style_screen.TLabel", font=("arial", 10), relief="flat", background=self.backcolor)
        self.style_text_screen = ttk.Style()
        self.style_text_screen.configure(
            "style_text_screen.TLabel", font=("arial", 10), relief="flat", background=self.midcolor)
        self.style_cbx_screen = ttk.Style()
        self.style_cbx_screen.configure(
            "style_screen.TCheckbutton", font=("arial", 10), relief="flat", background=self.midcolor)
        self.style_screen = ttk.Style()
        self.style_screen.configure(
            "style_screen.TFrame", background=self.midcolor)
        self.style_nb_screen = ttk.Style()
        self.style_nb_screen.configure(
            "style_screen.TNotebook", background=self.backcolor, relief="flat")
        self.style_nb_screen.configure(
            "style_screen.TNotebook.Tab", focuscolor=self.style_nb_screen.configure(".")["background"])
        self.style_nb_screen.map(
            "style_screen.TNotebook.Tab", background=[('selected', self.midcolor), ('active', "#000000")])
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
                                   style="style_actionbar.TButton",
                                   command=self.controller.stop)

        # create and place Logo on top
        self.icon_logo = tk.Canvas(master=self.mainframe, relief="flat", highlightthickness=0)
        self.icon_logo.create_image(0, 0, image=self.img_logo, anchor="nw")

        # infobar--------------------------------------------------------------
        # create and place infobar on mainframe
        self.infobar = tk.Canvas(master=self.mainframe,
                                 relief="flat",
                                 bg=self.backcolor,
                                 highlightthickness=0,
                                 highlightbackground="black")

        # create and place clock and timestamp on infobar
        self.icon_clock = tk.Canvas(master=self.infobar,
                                    relief="flat",
                                    highlightthickness=0,
                                    bg=self.backcolor)
        self.icon_clock.create_image(0, 0, image=self.img_clock, anchor="nw")

        self.timestamp = tk.StringVar()
        self.lbl_timestamp = ttk.Label(master=self.infobar,
                                       style="style_infobar.TLabel",
                                       textvariable=self.timestamp,
                                       anchor="w")

        # create and place LED and label for PLC state on infobar
        self.lbl_led_plc = ttk.Label(master=self.infobar,
                                     style="style_infobar.TLabel",
                                     text="PLC",
                                     anchor="w")

        self.icon_led = tk.Canvas(master=self.infobar, relief="flat", highlightthickness=0, bg=self.backcolor)
        self.icon_led.create_image(0, 0, image=self.img_led_gn, anchor="nw")
        self.icon_led.create_image(0, 0, image=self.img_led_rd, anchor="nw")
        self.icon_led.create_image(0, 0, image=self.img_led_ye, anchor="nw")

        # create and place versionnumber and icon on infobar
        self.icon_version = tk.Canvas(master=self.infobar,
                                      relief="flat",
                                      highlightthickness=0,
                                      bg=self.backcolor)
        self.icon_version.create_image(0, 0, image=self.img_version, anchor="nw")

        self.version = tk.StringVar()
        self.version.set(self.configfile["version"])
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
                                   bg=self.midcolor)

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
                                                  style="style_screen.TButton",
                                                  command=self.controller.data_get)

        # screen setup---------------------------------------------------------
        # create checkbox for option fullscreen
        self.opt_fullscreen = tk.BooleanVar()
        self.opt_fullscreen.set(self.projectfile["opt_fullscreen"])
        self.cbx_fullscreen = ttk.Checkbutton(master=self.screen_setup,
                                              text="Fullscreen",
                                              variable=self.opt_fullscreen,
                                              command=self.window_size,
                                              style="style_screen.TCheckbutton")

        # screensize-----------------------------------------------------------
        # call scale function when windowsize gets changed
        self.window.bind("<Configure>", lambda x: self.window_scale())
        # set window startposisiton and startsize
        # window zoomed without titlebar optional
        self.window_size()

    def window_scale(self):
        # calculate difference between minimal size and actual size
        # so the right scale can be calculated with individual size on startup
        # ox, oy: offset width (ox) and offset height (oy)
        ox = int(self.window.winfo_width()) - self.configfile["min_width"]
        oy = int(self.window.winfo_height()) - self.configfile["min_height"]
        # scale GUI elements from Mainframe
        self.screens.place(x=0, y=0, width=802 + ox, height=578 + oy)
        self.btn_exit.place(x=623 + ox, y=0, width=58, height=58)
        self.icon_logo.place(x=687 + ox, y=0, width=114, height=58)
        self.infobar.place(x=0, y=576 + oy, height=24, width=800 + ox)
        self.icon_clock.place(x=670 + ox, y=3, height=20, width=20)
        self.lbl_timestamp.place(x=690 + ox, y=1, width=150, height=24)
        self.icon_led.place(x=246, y=3, width=20, height=20)
        self.lbl_led_plc.place(x=270, y=3, width=50, height=18)
        self.icon_version.place(x=5, y=3, height=20, width=20)
        self.lbl_version.place(x=25, y=3, width=150, height=18)
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
        if not self.projectfile["opt_fullscreen"]:
            self.projectfile["opt_windowwidth"] = self.window.winfo_width()
            self.projectfile["opt_windowheight"] = self.window.winfo_height()

    def window_size(self):
        fullscreen = self.opt_fullscreen.get()
        self.projectfile["opt_fullscreen"] = fullscreen
        if fullscreen:
            self.window.overrideredirect(True)
            self.window.state("zoomed")
        else:
            self.window.overrideredirect(False)
            self.window.state("normal")
            # set window startposisiton and startsize
            screenwidth = self.window.winfo_screenwidth()
            screenheight = self.window.winfo_screenheight()
            windowwidth = self.projectfile["opt_windowwidth"]
            windowheight = self.projectfile["opt_windowheight"]
            windowstartposx = (screenwidth / 2) - (windowwidth / 2)
            windowstartposy = (screenheight / 2) - (windowheight / 2)
            self.window.geometry("%dx%d+%d+%d" % (windowwidth, windowheight, windowstartposx, windowstartposy))

    def window_title(self, text):
        title = "{title} - {project}".format(title=self.configfile["title"], project=text)
        self.window.title(title)

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
        version = self.configfile["version"]
        name = self.configfile["customer_name"]
        mail = self.configfile["customer_mail"]
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

    def datatree_update(self, projectfile):
        self.projectfile = projectfile
        name = self.projectfile["udt_name"]
        description = self.projectfile["udt_description"]
        version = self.projectfile["udt_version"]
        info = self.projectfile["udt_info"]
        data = self.projectfile["udt_data"]
        # clear data in datatree
        self.datatree_clear()
        # fill data in datatree
        self.datatree_fill(name, description, version, info, data)

    def led_state(self, state="error"):
        if state == "error":
            self.icon_led.create_image(0, 0, image=self.img_led_rd, anchor="nw")
        elif state == "warn":
            self.icon_led.create_image(0, 0, image=self.img_led_ye, anchor="nw")
        elif state == "ok":
            self.icon_led.create_image(0, 0, image=self.img_led_gn, anchor="nw")
        else:
            self.icon_led.create_image(0, 0, image=self.img_led_rd, anchor="nw")
