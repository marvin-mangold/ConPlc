"""
ConPlc - connect PLC and PC
Copyright (C) 2020  Marvin Mangold (mangold.mangold00@googlemail.com)

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
    def __init__(self, controller):
        self.controller = controller
        # other variables------------------------------------------------------
        self.desktoppath = os.path.expanduser(r"~\Desktop")
        # general window settings----------------------------------------------
        # create window
        self.window = tk.Tk()
        # load icons
        self.img_icon = tk.PhotoImage(file=Path(self.controller.configfile["media_icon"]))
        self.img_home = tk.PhotoImage(file=Path(self.controller.configfile["media_home"]))
        self.img_server = tk.PhotoImage(file=Path(self.controller.configfile["media_server"]))
        self.img_data = tk.PhotoImage(file=Path(self.controller.configfile["media_data"]))
        self.img_setup = tk.PhotoImage(file=Path(self.controller.configfile["media_setup"]))
        self.img_logo = tk.PhotoImage(file=Path(self.controller.configfile["media_logo"]))
        self.img_exit = tk.PhotoImage(file=Path(self.controller.configfile["media_exit"]))
        self.img_clock = tk.PhotoImage(file=Path(self.controller.configfile["media_clock"]))
        self.img_version = tk.PhotoImage(file=Path(self.controller.configfile["media_version"]))
        self.img_play = tk.PhotoImage(file=Path(self.controller.configfile["media_play"]))
        self.img_pause = tk.PhotoImage(file=Path(self.controller.configfile["media_pause"]))
        self.img_led_gn = tk.PhotoImage(file=Path(self.controller.configfile["media_led_gn"]))
        self.img_led_ye = tk.PhotoImage(file=Path(self.controller.configfile["media_led_ye"]))
        self.img_led_rd = tk.PhotoImage(file=Path(self.controller.configfile["media_led_rd"]))

        # set title
        self.window.title(self.controller.configfile["title"])

        # set icon
        self.window.iconphoto(True, self.img_icon)

        # set min/max windowsize
        self.window.wm_minsize(self.controller.configfile["min_width"], self.controller.configfile["min_height"])
        self.window.wm_maxsize(self.controller.configfile["max_width"], self.controller.configfile["max_height"])

        # style settings-general-----------------------------------------------
        # load tkinter ttk style theme
        self.window.tk.call("lappend", "auto_path", Path(self.controller.configfile["style_themepath"]))
        self.window.tk.call("package", "require", Path(self.controller.configfile["style_themename"]))
        self.style_main = ttk.Style()
        self.style_main.theme_use(Path(self.controller.configfile["style_themename"]))

        # mainframe------------------------------------------------------------
        # set mainframe for window
        self.mainframe = ttk.Frame(master=self.window, style="TFrame")
        # set mainframe to max size
        self.mainframe.place(x=0,
                             y=0,
                             height=self.controller.configfile["max_height"],
                             width=self.controller.configfile["max_width"])

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
            "style_screen.TButton", font=("arial", 10), relief="solid")
        self.style_btn_screen.map(
            "style_screen.TButton", background=[('selected', self.midcolor), ('active', "#000000")])
        self.style_lbl_screen = ttk.Style()
        self.style_lbl_screen.configure(
            "style_screen.TLabel", font=("arial", 10), relief="flat", background=self.midcolor)
        self.style_lbl_var_screen = ttk.Style()
        self.style_lbl_var_screen.configure(
            "style_screen_var.TLabel", font=("arial", 10), relief="solid", background=self.backcolor)
        self.style_entry_screen = ttk.Style()
        self.style_entry_screen.configure(
            "style_screen.TEntry", font=("arial", 10), relief="flat", fieldbackground=self.backcolor)
        self.style_cbx_screen = ttk.Style()
        self.style_cbx_screen.configure(
            "style_screen.TCheckbutton", font=("arial", 10), relief="solid", background=self.midcolor)
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
        self.screen_server = ttk.Frame(self.screens, style="style_screen.TFrame")
        self.screen_data = ttk.Frame(self.screens, style="style_screen.TFrame")
        self.screen_setup = ttk.Frame(self.screens, style="style_screen.TFrame")
        self.screens.add(self.screen_home, text="Home", image=self.img_home, compound=tk.TOP)
        self.screens.add(self.screen_server, text="Server", image=self.img_server, compound=tk.TOP)
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
        self.filemenu.add_command(label="Backup", command=self.controller.file_backup)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.controller.stop)
        # help menu
        self.helpmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label="About ConPlc", command=self.about_show)

        # actionbar------------------------------------------------------------
        # create and place exit button on actionbar
        self.btn_exit = ttk.Button(master=self.mainframe,
                                   takefocus=0,
                                   text="Exit",
                                   compound=tk.TOP,
                                   image=self.img_exit,
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

        # create and place LED and label for connectionstate on infobar
        self.lbl_led_connection = ttk.Label(master=self.infobar,
                                     style="style_infobar.TLabel",
                                     text="Connection",
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
        self.version.set(self.controller.configfile["version"])
        self.lbl_version = ttk.Label(master=self.infobar,
                                     style="style_infobar.TLabel",
                                     textvariable=self.version,
                                     anchor="w")

        # screen home--------------------------------------------------------
        # create and place eventframe on screen home
        self.eventframe = tk.Canvas(master=self.screen_home,
                                    relief="flat",
                                    bg=self.frontcolor,
                                    highlightthickness=1,
                                    highlightbackground="black")

        # create and place label for eventframe
        self.lbl_eventframe = ttk.Label(master=self.eventframe,
                                        style="style_infobar.TLabel",
                                        text="Eventlog",
                                        anchor="w")

        # change mouse cursor when mouse over label
        self.lbl_eventframe.configure(cursor="sb_v_double_arrow")
        self.eventframediff = 0
        self.eventframeoffs = 100
        self.lbl_eventframe.bind("<Button-1>", lambda x: self.eventframe_drag(mode="start"))
        self.lbl_eventframe.bind("<B1-Motion>", lambda x: self.eventframe_drag(mode="move"))
        self.lbl_eventframe.bind("<ButtonRelease-1>", lambda x: self.eventframe_drag(mode="stop"))

        # create an place textfield on eventframe
        self.txt_eventframe = tk.Text(self.eventframe,
                                      width=10,
                                      bg=self.frontcolor,
                                      fg=self.textcolor,
                                      wrap="none",
                                      font=("arial", 10),
                                      state="disabled",
                                      relief="flat")

        # add scrollbar to eventframe
        self.eventframe_scrollx = ttk.Scrollbar(self.eventframe, orient="horizontal", command=self.txt_eventframe.xview)
        self.eventframe_scrolly = ttk.Scrollbar(self.eventframe, orient="vertical", command=self.txt_eventframe.yview)
        self.txt_eventframe.configure(xscrollcommand=self.eventframe_scrollx.set)
        self.txt_eventframe.configure(yscrollcommand=self.eventframe_scrolly.set)

        # screen server------------------------------------------------------
        # create and place label for connection ip-address
        self.lbl_con_ip = ttk.Label(master=self.screen_server,
                                    style="style_screen.TLabel",
                                    text="IP-Address:",
                                    anchor="w")

        # create and place entry for connection ip-address
        # byte 1
        self.con_ip_byte1 = tk.StringVar()
        self.con_ip_byte1.set(self.controller.projectfile["con_ip_byte1"])
        self.con_ip_byte1.trace("w", lambda *args: self.entry_validate(var=self.con_ip_byte1, mode="ip", length=3))
        self.entry_con_ip_byte1 = ttk.Entry(master=self.screen_server,
                                            style="style_screen.TEntry",
                                            textvariable=self.con_ip_byte1)
        self.entry_con_ip_byte1.bind("<KeyRelease>", lambda x: self.entry_after())

        # byte 2
        self.con_ip_byte2 = tk.StringVar()
        self.con_ip_byte2.set(self.controller.projectfile["con_ip_byte2"])
        self.con_ip_byte2.trace("w", lambda *args: self.entry_validate(var=self.con_ip_byte2, mode="ip", length=3))
        self.entry_con_ip_byte2 = ttk.Entry(master=self.screen_server,
                                            style="style_screen.TEntry",
                                            textvariable=self.con_ip_byte2)
        self.entry_con_ip_byte2.bind("<KeyRelease>", lambda x: self.entry_after())

        # byte 3
        self.con_ip_byte3 = tk.StringVar()
        self.con_ip_byte3.set(self.controller.projectfile["con_ip_byte3"])
        self.con_ip_byte3.trace("w", lambda *args: self.entry_validate(var=self.con_ip_byte3, mode="ip", length=3))
        self.entry_con_ip_byte3 = ttk.Entry(master=self.screen_server,
                                            style="style_screen.TEntry",
                                            textvariable=self.con_ip_byte3)
        self.entry_con_ip_byte3.bind("<KeyRelease>", lambda x: self.entry_after())

        # byte 4
        self.con_ip_byte4 = tk.StringVar()
        self.con_ip_byte4.set(self.controller.projectfile["con_ip_byte4"])
        self.con_ip_byte4.trace("w", lambda *args: self.entry_validate(var=self.con_ip_byte4, mode="ip", length=3))
        self.entry_con_ip_byte4 = ttk.Entry(master=self.screen_server,
                                            style="style_screen.TEntry",
                                            textvariable=self.con_ip_byte4)
        self.entry_con_ip_byte4.bind("<KeyRelease>", lambda x: self.entry_after())

        # create and place label for connection port number
        self.lbl_con_port = ttk.Label(master=self.screen_server,
                                      style="style_screen.TLabel",
                                      text="Portnumber:",
                                      anchor="w")

        # create and place entry for connection port number
        self.con_port = tk.StringVar()
        self.con_port.set(self.controller.projectfile["con_port"])
        self.con_port.trace("w", lambda *args: self.entry_validate(var=self.con_port, mode="port", length=5))
        self.entry_con_port = ttk.Entry(master=self.screen_server,
                                        style="style_screen.TEntry",
                                        textvariable=self.con_port)
        self.entry_con_port.bind("<KeyRelease>", lambda x: self.entry_after())

        # create and place label for play pause connection
        self.lbl_playpause = ttk.Label(master=self.screen_server,
                                       style="style_screen.TLabel",
                                       text="Run/Stop:",
                                       anchor="w")

        # create checkbox autoplay connection
        self.con_autorun = tk.BooleanVar()
        self.con_autorun.set(self.controller.projectfile["con_autorun"])
        self.cbx_autoplay = ttk.Checkbutton(master=self.screen_server,
                                            text="Autorun",
                                            variable=self.con_autorun,
                                            command=self.connect_autorun,
                                            style="style_screen.TCheckbutton")

        # create checkboxbutton for play pause connection
        self.playpause = tk.BooleanVar()
        self.cbx_playpause = tk.Checkbutton(master=self.screen_server,
                                            bd=0,
                                            bg=self.backcolor,
                                            selectcolor=self.backcolor,
                                            highlightcolor=self.backcolor,
                                            activebackground=self.backcolor,
                                            relief="flat",
                                            variable=self.playpause,
                                            command=self.connect_state,
                                            image=self.img_play,
                                            selectimage=self.img_pause,
                                            indicatoron=False)

        # screen data----------------------------------------------------------
        # create frame on screen data for UDT name + description + version + info
        self.udt_infos = tk.Canvas(master=self.screen_data,
                                   relief="flat",
                                   highlightthickness=0,
                                   bg=self.midcolor)

        # create and place label for UDT name
        self.lbl_udt_name = ttk.Label(master=self.udt_infos,
                                      style="style_screen.TLabel",
                                      text="Name:",
                                      anchor="w")

        # create and place variable label for UDT name
        self.udt_name = tk.StringVar()
        self.lbl_udt_name_var = ttk.Label(master=self.udt_infos,
                                          style="style_screen_var.TLabel",
                                          textvariable=self.udt_name,
                                          anchor="w")

        # create and place label for UDT description
        self.lbl_udt_description = ttk.Label(master=self.udt_infos,
                                             style="style_screen.TLabel",
                                             text="Description:",
                                             anchor="w")

        # create and place variable label for UDT description
        self.udt_description = tk.StringVar()
        self.lbl_udt_description_var = ttk.Label(master=self.udt_infos,
                                                 style="style_screen_var.TLabel",
                                                 textvariable=self.udt_description,
                                                 anchor="w")

        # create and place label for UDT version
        self.lbl_udt_version = ttk.Label(master=self.udt_infos,
                                         style="style_screen.TLabel",
                                         text="Version:",
                                         anchor="w")

        # create and place variable label for UDT version
        self.udt_version = tk.StringVar()
        self.lbl_udt_version_var = ttk.Label(master=self.udt_infos,
                                             style="style_screen_var.TLabel",
                                             textvariable=self.udt_version,
                                             anchor="w")

        # create and place label for UDT info
        self.lbl_udt_info = ttk.Label(master=self.udt_infos,
                                      style="style_screen.TLabel",
                                      text="Information:",
                                      anchor="w")

        # create and place variable label for UDT info
        self.udt_info = tk.StringVar()
        self.lbl_udt_info_var = ttk.Label(master=self.udt_infos,
                                          style="style_screen_var.TLabel",
                                          textvariable=self.udt_info,
                                          anchor="w")

        # create and place treeview for data structure
        self.datatree = ttk.Treeview(self.screen_data)
        self.datatree["columns"] = ("Datatype", "Comment")
        self.datatree.column("#0", width=200, minwidth=100, stretch=tk.NO)
        self.datatree.column("Datatype", width=200, minwidth=100, stretch=tk.NO)
        self.datatree.column("Comment", width=200, minwidth=100, stretch=tk.YES)
        self.datatree.heading("#0", text="Name", anchor=tk.W)
        self.datatree.heading("Datatype", text="Datatype", anchor=tk.W)
        self.datatree.heading("Comment", text="Comment", anchor=tk.W)
        # add scrollbar to treeview
        self.datatree_scrollx = ttk.Scrollbar(self.screen_data, orient="horizontal", command=self.datatree.xview)
        self.datatree_scrolly = ttk.Scrollbar(self.screen_data, orient="vertical", command=self.datatree.yview)
        self.datatree.configure(xscrollcommand=self.datatree_scrollx.set)
        self.datatree.configure(yscrollcommand=self.datatree_scrolly.set)

        # create button for datasructure import
        self.btn_import_datasructure = ttk.Button(master=self.screen_data,
                                                  takefocus=0,
                                                  text='load Datastructure',
                                                  style="style_screen.TButton",
                                                  command=self.controller.data_get)

        # screen setup---------------------------------------------------------
        # create checkbox for option fullscreen
        self.opt_fullscreen = tk.BooleanVar()
        self.opt_fullscreen.set(self.controller.projectfile["opt_fullscreen"])
        self.cbx_fullscreen = ttk.Checkbutton(master=self.screen_setup,
                                              text="Fullscreen",
                                              variable=self.opt_fullscreen,
                                              command=self.window_update,
                                              style="style_screen.TCheckbutton")

        # Key events-----------------------------------------------------------
        self.window.bind("<KeyPress>", self.keydown)
        self.window.bind("<KeyRelease>", self.keyup)

        # screensize-----------------------------------------------------------
        # call scale function when windowsize gets changed
        self.window.bind("<Configure>", lambda x: self.window_scale())
        # set window startposisiton and startsize
        # window zoomed without titlebar optional
        self.window_update()
        # initial trigger for 250ms loop

    def window_scale(self):
        # calculate difference between minimal size and actual size
        # so the right scale can be calculated with individual size on startup
        # ox, oy: offset width (ox) and offset height (oy)
        ox = int(self.window.winfo_width()) - self.controller.configfile["min_width"]
        oy = int(self.window.winfo_height()) - self.controller.configfile["min_height"]
        # scale gui elements from Mainframe------------------------------------
        self.screens.place(x=0, y=0, width=802 + ox, height=578 + oy)
        self.btn_exit.place(x=623 + ox, y=0, width=58, height=58)
        self.icon_logo.place(x=687 + ox, y=0, width=114, height=58)
        self.infobar.place(x=0, y=576 + oy, width=800 + ox, height=24)
        self.icon_clock.place(x=670 + ox, y=3, width=20, height=20)
        self.lbl_timestamp.place(x=690 + ox, y=1, width=150, height=24)
        self.icon_led.place(x=246, y=3, width=20, height=20)
        self.lbl_led_connection.place(x=270, y=3, width=80, height=18)
        self.icon_version.place(x=5, y=3, width=20, height=20)
        self.lbl_version.place(x=25, y=3, width=150, height=18)
        # scale gui elements from screen home----------------------------------
        self.eventframe.place(x=0, y=482 + oy - self.eventframeoffs, height=35 + self.eventframeoffs, width=797 + ox)
        self.lbl_eventframe.place(x=1, y=1, width=795 + ox, height=20)
        self.txt_eventframe.place(x=1, y=20, width=782 + ox, height=10 + self.eventframeoffs)
        self.eventframe_scrollx.place(x=1, y=20 + self.eventframeoffs, width=782 + ox)
        self.eventframe_scrolly.place(x=782 + ox, y=20, height=15 + self.eventframeoffs)
        # scale gui elements from screen server--------------------------------
        self.lbl_con_ip.place(x=50, y=25, width=80, height=25)
        self.entry_con_ip_byte1.place(x=135, y=25, width=35, height=25)
        self.entry_con_ip_byte2.place(x=175, y=25, width=35, height=25)
        self.entry_con_ip_byte3.place(x=215, y=25, width=35, height=25)
        self.entry_con_ip_byte4.place(x=255, y=25, width=35, height=25)
        self.lbl_con_port.place(x=50, y=58, width=80, height=25)
        self.entry_con_port.place(x=135, y=58, width=45, height=25)
        self.lbl_playpause.place(x=50, y=97, width=80, height=25)
        self.cbx_playpause.place(x=135, y=91, width=40, height=40)
        self.cbx_autoplay.place(x=180, y=91, width=80, height=40)
        # scale gui elements from screen data----------------------------------
        self.udt_infos.place(x=50, y=25, width=750 + ox, height=58)
        self.lbl_udt_name.place(x=0, y=0, width=50, height=25)
        self.lbl_udt_name_var.place(x=55, y=0, width=250, height=25)
        self.lbl_udt_description.place(x=330, y=0, width=85, height=25)
        self.lbl_udt_description_var.place(x=420, y=0, width=283 + ox, height=25)
        self.lbl_udt_version.place(x=0, y=33, width=50, height=25)
        self.lbl_udt_version_var.place(x=55, y=33, width=250, height=25)
        self.lbl_udt_info.place(x=330, y=33, width=85, height=25)
        self.lbl_udt_info_var.place(x=420, y=33, width=283 + ox, height=25)
        # scale gui elements from treeview-------------------------------------
        self.datatree.place(x=50, y=90, width=691 + ox, height=325 + oy)
        self.datatree_scrollx.place(x=50, y=415 + oy, width=691 + ox)
        self.datatree_scrolly.place(x=740 + ox, y=92, height=337 + oy)
        self.btn_import_datasructure.place(x=50, y=437 + oy, width=150, height=30)
        # scale gui elements from screen setup---------------------------------
        self.cbx_fullscreen.place(x=50, y=25, width=90, height=40)
        if not self.controller.projectfile["opt_fullscreen"]:
            self.controller.projectfile["opt_windowwidth"] = self.window.winfo_width()
            self.controller.projectfile["opt_windowheight"] = self.window.winfo_height()

    def window_update(self):
        fullscreen = self.opt_fullscreen.get()
        self.controller.projectfile["opt_fullscreen"] = fullscreen
        if fullscreen:
            self.window.overrideredirect(True)
            self.window.state("zoomed")
        else:
            self.window.overrideredirect(False)
            self.window.state("normal")
            # set window startposisiton and startsize
            screenwidth = self.window.winfo_screenwidth()
            screenheight = self.window.winfo_screenheight()
            windowwidth = self.controller.projectfile["opt_windowwidth"]
            windowheight = self.controller.projectfile["opt_windowheight"]
            windowstartposx = (screenwidth / 2) - (windowwidth / 2)
            windowstartposy = (screenheight / 2) - (windowheight / 2)
            self.window.geometry("%dx%d+%d+%d" % (windowwidth, windowheight, windowstartposx, windowstartposy))

    def eventframe_drag(self, mode):
        if mode == "start":
            self.eventframediff = self.eventframe.winfo_rooty() + self.eventframe.winfo_height() - 35
        elif mode == "move":
            self.eventframeoffs = self.eventframediff - self.window.winfo_pointery()
            if self.eventframeoffs < 0:
                self.eventframeoffs = 0
            if self.eventframeoffs > 300:
                self.eventframeoffs = 300
            self.window_scale()

    def eventframe_post(self, text):
        self.txt_eventframe.configure(state="normal")
        timestamp = self.controller.timestamp_get()
        self.txt_eventframe.insert(tk.END, "{timestamp}: {text}\n".format(timestamp=timestamp, text=text))
        self.txt_eventframe.configure(state="disabled")
        self.txt_eventframe.yview_moveto('1.0')

    def keyup(self, event):
        # print(event)
        # if event.keysym == "Tab": self.method()
        pass

    def keydown(self, event):
        # print(event)
        pass

    @staticmethod
    def entry_validate(var, mode, length):
        text = var.get()
        # check if text is a number between 0 and 65535
        if mode == "port":
            # set text to maximum length
            if len(text) > length:
                text = text[:length]
            # delete all non digits
            newtext = ""
            for char in text:
                if str.isdigit(char):
                    newtext += char
            text = newtext
            # set min max values
            if str.isdigit(text):
                if int(text) < 0:
                    text = "0"
                elif int(text) > 65535:
                    text = "65535"
        # check if text is a number between 0 and 255
        if mode == "ip":
            # set text to maximum length
            if len(text) > length:
                text = text[:length]
            # delete all non digits
            newtext = ""
            for char in text:
                if str.isdigit(char):
                    newtext += char
            text = newtext
            # set min max values
            if str.isdigit(text):
                if int(text) < 0:
                    text = "0"
                elif int(text) > 255:
                    text = "255"
        var.set(text)

    def entry_after(self):
        self.controller.projectfile["con_ip_byte1"] = self.con_ip_byte1.get()
        self.controller.projectfile["con_ip_byte2"] = self.con_ip_byte2.get()
        self.controller.projectfile["con_ip_byte3"] = self.con_ip_byte3.get()
        self.controller.projectfile["con_ip_byte4"] = self.con_ip_byte4.get()
        self.controller.projectfile["con_port"] = self.con_port.get()

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
        txt_version = self.controller.configfile["version"]
        txt_copyright = self.controller.configfile["about_copyright"]
        txt_name = self.controller.configfile["about_name"]
        txt_mail = self.controller.configfile["about_mail"]
        txt_license = self.controller.configfile["about_license"]
        message = "{version}\n" \
                  "{copyright} {name}\n" \
                  "{mail}\n" \
                  "{license}".format(version=txt_version,
                                     name=txt_name,
                                     mail=txt_mail,
                                     license=txt_license,
                                     copyright=txt_copyright)
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

    def datatree_update(self):
        name = self.controller.projectfile["udt_name"]
        description = self.controller.projectfile["udt_description"]
        version = self.controller.projectfile["udt_version"]
        info = self.controller.projectfile["udt_info"]
        data = self.controller.projectfile["udt_data"]
        # clear data in datatree
        self.datatree_clear()
        # fill data in datatree
        self.datatree_fill(name, description, version, info, data)

    def server_update(self):
        self.con_ip_byte1.set(self.controller.projectfile["con_ip_byte1"])
        self.con_ip_byte2.set(self.controller.projectfile["con_ip_byte2"])
        self.con_ip_byte3.set(self.controller.projectfile["con_ip_byte3"])
        self.con_ip_byte4.set(self.controller.projectfile["con_ip_byte4"])
        self.con_port.set(self.controller.projectfile["con_port"])
        self.con_autorun.set(self.controller.projectfile["con_autorun"])

    def setup_update(self):
        self.opt_fullscreen.set(self.controller.projectfile["opt_fullscreen"])

    def led_state(self, state="error"):
        if state == "error":
            self.icon_led.create_image(0, 0, image=self.img_led_rd, anchor="nw")
        elif state == "warn":
            self.icon_led.create_image(0, 0, image=self.img_led_ye, anchor="nw")
        elif state == "ok":
            self.icon_led.create_image(0, 0, image=self.img_led_gn, anchor="nw")
        else:
            self.icon_led.create_image(0, 0, image=self.img_led_rd, anchor="nw")

    def connect_autorun(self):
        self.controller.projectfile["con_autorun"] = self.con_autorun.get()

    def connect_state(self):
        state = self.playpause.get()
        if state:
            self.controller.server_start()
        elif not state:
            self.controller.server_stop()
