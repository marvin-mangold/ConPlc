"""
ConPlc - connect PLC and PC
Copyright (C) 2021  Marvin Mangold (Marvin.Mangold00@googlemail.com)

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
        """
        setup window
        load images
        configure style
        create gui elements
        """
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
        self.img_csv = tk.PhotoImage(file=Path(self.controller.configfile["media_csv"]))
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
        self.backcolor = self.style_main.lookup("TButton", "background")
        self.midcolor = "#3d4145"
        self.frontcolor = self.style_main.lookup("TTreeview", "background")
        self.textcolor = self.style_main.lookup("TButton", "foreground")
        # actionbar
        self.style_btn_actionbar = ttk.Style()
        self.style_btn_actionbar.configure(
            "style_actionbar.TButton", font=("arial", 8), relief="flat")
        self.style_btn_actionbar.map(
            "style_actionbar.TButton", background=[("selected", self.midcolor), ("active", "#000000")])
        # infobar
        self.style_lbl_infobar = ttk.Style()
        self.style_lbl_infobar.configure(
            "style_infobar.TLabel", foreground=self.textcolor, background=self.backcolor)
        # eventframe_autoscroll
        self.style_btn_eventframe = ttk.Style()
        self.style_btn_eventframe.configure(
            "style_eventframe.TButton", relief="flat", background="#000000")
        self.style_btn_eventframe.map(
            "style_eventframe.TButton", background=[("selected", self.midcolor), ("active", "#111111")])
        # csv_table_autoscroll
        self.style_btn_csv_table = ttk.Style()
        self.style_btn_csv_table.configure(
            "style_csv_table.TButton", relief="flat", background="#000000", anchor=tk.N)
        self.style_btn_csv_table.map(
            "style_csv_table.TButton", background=[("selected", self.midcolor), ("active", "#111111")])
        # screen
        self.style_btn_screen = ttk.Style()
        self.style_btn_screen.configure(
            "style_screen.TButton", font=("arial", 10), relief="solid")
        self.style_btn_screen.map(
            "style_screen.TButton", background=[("selected", self.midcolor), ("active", "#000000")])
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
            "style_screen.TNotebook.Tab", background=[("selected", self.midcolor), ("active", "#000000")])
        self.style_treeview = ttk.Style()
        self.style_treeview.configure("Treeview", bordercolor="black")
        self.style_rad_screen = ttk.Style()
        self.style_rad_screen.configure(
            "style_screen.TRadiobutton", font=("arial", 10), relief="solid", background=self.midcolor)
        self.style_men_screen = ttk.Style()
        self.style_men_screen.configure(
            "style_screen.TMenubutton", font=("arial", 10), relief="solid", background=self.midcolor)

        # create Tabs----------------------------------------------------------
        self.screens = ttk.Notebook(self.mainframe, style="style_screen.TNotebook")
        self.screen_home = ttk.Frame(self.screens, style="style_screen.TFrame")
        self.screen_server = ttk.Frame(self.screens, style="style_screen.TFrame")
        self.screen_data = ttk.Frame(self.screens, style="style_screen.TFrame")
        self.screen_setup = ttk.Frame(self.screens, style="style_screen.TFrame")
        self.screen_csv = ttk.Frame(self.screens, style="style_screen.TFrame")
        self.screens.add(self.screen_home, text="Home", image=self.img_home, compound=tk.TOP)
        self.screens.add(self.screen_server, text="Server", image=self.img_server, compound=tk.TOP)
        self.screens.add(self.screen_data, text="Data", image=self.img_data, compound=tk.TOP)
        self.screens.add(self.screen_setup, text="Setup", image=self.img_setup, compound=tk.TOP)
        self.screens.add(self.screen_csv, text="CSV", image=self.img_csv, compound=tk.TOP)

        # menubar--------------------------------------------------------------
        self.menu = tk.Menu(self.window)
        self.window.config(menu=self.menu)
        self.window.option_add("*tearOff", False)
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
        self.icon_led_last_state = ""
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

        # signal to rebuild table
        self.csv_table_rebuild = True
        # create and place treeview for data structure
        self.csv_table = ttk.Treeview(self.screen_home, style="Treeview")
        # add scrollbar to treeview
        self.csv_table_scrollx = ttk.Scrollbar(self.screen_home,
                                               orient="horizontal",
                                               command=self.csv_table.xview,
                                               cursor="hand2")
        self.csv_table_scrolly = ttk.Scrollbar(self.screen_home,
                                               orient="vertical",
                                               command=self.csv_table.yview,
                                               cursor="hand2")
        self.csv_table.configure(xscrollcommand=self.csv_table_scrollx.set)
        self.csv_table.configure(yscrollcommand=self.csv_table_scrolly.set)

        # create an place button autoscroll on csv_table
        self.csv_table_autoscroll_var = tk.BooleanVar()
        self.csv_table_autoscroll_var.set(True)
        self.btn_csv_autoscroll = ttk.Button(master=self.csv_table,
                                             takefocus=0,
                                             text="autoscroll",
                                             style="style_csv_table.TButton",
                                             command=self.csv_table_autoscroll)

        # create and place eventframe on screen home
        self.eventframe = tk.Canvas(master=self.screen_home,
                                    relief="flat",
                                    bg=self.frontcolor,
                                    highlightthickness=1,
                                    highlightbackground="black")

        # create and place label for eventframe
        self.lbl_eventframe = ttk.Label(master=self.eventframe,
                                        style="style_infobar.TLabel",
                                        text="Event Log",
                                        anchor="w")

        # change mouse cursor when mouse over label
        self.lbl_eventframe.configure(cursor="sb_v_double_arrow")
        self.eventframediff = 0
        self.eventframeoffs = 100
        self.lbl_eventframe.bind("<Button-1>", lambda x: self.eventframe_drag(mode="start"))
        self.lbl_eventframe.bind("<B1-Motion>", lambda x: self.eventframe_drag(mode="move"))
        self.lbl_eventframe.bind("<ButtonRelease-1>", lambda x: self.eventframe_drag(mode="stop"))

        # create an place button autoscroll on eventframe
        self.eventlog_autoscroll_var = tk.BooleanVar()
        self.eventlog_autoscroll_var.set(True)
        self.btn_eve_autoscroll = ttk.Button(master=self.eventframe,
                                             takefocus=0,
                                             text="autoscroll",
                                             style="style_eventframe.TButton",
                                             command=self.eventlog_autoscroll)

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
        self.eventframe_scrollx = ttk.Scrollbar(self.eventframe,
                                                orient="horizontal",
                                                command=self.txt_eventframe.xview,
                                                cursor="hand2")
        self.eventframe_scrolly = ttk.Scrollbar(self.eventframe,
                                                orient="vertical",
                                                command=self.txt_eventframe.yview,
                                                cursor="hand2")
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

        # create and place label for run stop connection
        self.lbl_runstop = ttk.Label(master=self.screen_server,
                                     style="style_screen.TLabel",
                                     text="Run/Stop:",
                                     anchor="w")

        # create checkbox autostart connection
        self.con_autostart = tk.BooleanVar()
        self.con_autostart.set(self.controller.projectfile["con_autostart"])
        self.cbx_autostart = ttk.Checkbutton(master=self.screen_server,
                                             text="Autostart",
                                             variable=self.con_autostart,
                                             command=self.connect_autostart,
                                             style="style_screen.TCheckbutton")

        # create checkboxbutton for run stop connection
        self.runstop = tk.BooleanVar()
        self.cbx_runstop = tk.Checkbutton(master=self.screen_server,
                                          bd=0,
                                          bg=self.backcolor,
                                          selectcolor=self.backcolor,
                                          highlightcolor=self.backcolor,
                                          activebackground=self.backcolor,
                                          relief="flat",
                                          variable=self.runstop,
                                          command=self.connect_state,
                                          image=self.img_play,
                                          selectimage=self.img_pause,
                                          indicatoron=False)

        # create and place label for show received data in eventlog
        self.lbl_show_recvdata = ttk.Label(master=self.screen_server,
                                           style="style_screen.TLabel",
                                           text="Show received Data in Event log:",
                                           anchor="w")

        # create checkbox for show received data in eventlog
        self.con_show_recvdata = tk.BooleanVar()
        self.con_show_recvdata.set(self.controller.projectfile["con_show_recvdata"])
        self.cbx_show_recvdata = ttk.Checkbutton(master=self.screen_server,
                                                 variable=self.con_show_recvdata,
                                                 command=self.connect_show_recvdata,
                                                 style="style_screen.TCheckbutton")

        # screen data----------------------------------------------------------
        # create frame on screen data for udt name + description + version + info
        self.udt_infos = tk.Canvas(master=self.screen_data,
                                   relief="flat",
                                   highlightthickness=0,
                                   bg=self.midcolor)

        # create and place label for udt name
        self.lbl_udt_name = ttk.Label(master=self.udt_infos,
                                      style="style_screen.TLabel",
                                      text="Name:",
                                      anchor="w")

        # create and place variable label for udt name
        self.udt_name = tk.StringVar()
        self.lbl_udt_name_var = ttk.Label(master=self.udt_infos,
                                          style="style_screen_var.TLabel",
                                          textvariable=self.udt_name,
                                          anchor="w")

        # create and place label for udt description
        self.lbl_udt_description = ttk.Label(master=self.udt_infos,
                                             style="style_screen.TLabel",
                                             text="Description:",
                                             anchor="w")

        # create and place variable label for udt description
        self.udt_description = tk.StringVar()
        self.lbl_udt_description_var = ttk.Label(master=self.udt_infos,
                                                 style="style_screen_var.TLabel",
                                                 textvariable=self.udt_description,
                                                 anchor="w")

        # create and place label for udt version
        self.lbl_udt_version = ttk.Label(master=self.udt_infos,
                                         style="style_screen.TLabel",
                                         text="Version:",
                                         anchor="w")

        # create and place variable label for udt version
        self.udt_version = tk.StringVar()
        self.lbl_udt_version_var = ttk.Label(master=self.udt_infos,
                                             style="style_screen_var.TLabel",
                                             textvariable=self.udt_version,
                                             anchor="w")

        # create and place label for udt info
        self.lbl_udt_info = ttk.Label(master=self.udt_infos,
                                      style="style_screen.TLabel",
                                      text="Information:",
                                      anchor="w")

        # create and place variable label for udt info
        self.udt_info = tk.StringVar()
        self.lbl_udt_info_var = ttk.Label(master=self.udt_infos,
                                          style="style_screen_var.TLabel",
                                          textvariable=self.udt_info,
                                          anchor="w")

        # create and place treeview for data structure
        self.datatree = ttk.Treeview(self.screen_data)
        self.datatree["columns"] = ("Datatype", "Value", "Byte", "Comment")
        self.datatree.column("#0", width=200, minwidth=50, stretch=tk.NO)
        self.datatree.column("Datatype", width=150, minwidth=50, stretch=tk.NO)
        self.datatree.column("Value", width=100, minwidth=50, stretch=tk.NO)
        self.datatree.column("Byte", width=50, minwidth=50, stretch=tk.NO)
        self.datatree.column("Comment", width=200, minwidth=50, stretch=tk.YES)
        self.datatree.heading("#0", text="Name", anchor=tk.W)
        self.datatree.heading("Datatype", text="Datatype", anchor=tk.W)
        self.datatree.heading("Value", text="Value", anchor=tk.W)
        self.datatree.heading("Byte", text="Byte", anchor=tk.W)
        self.datatree.heading("Comment", text="Comment", anchor=tk.W)
        # add scrollbar to treeview
        self.datatree_scrollx = ttk.Scrollbar(self.screen_data, orient="horizontal", command=self.datatree.xview)
        self.datatree_scrolly = ttk.Scrollbar(self.screen_data, orient="vertical", command=self.datatree.yview)
        self.datatree.configure(xscrollcommand=self.datatree_scrollx.set)
        self.datatree.configure(yscrollcommand=self.datatree_scrolly.set)

        # create button for datasructure import
        self.btn_import_datasructure = ttk.Button(master=self.screen_data,
                                                  takefocus=0,
                                                  text="load Datastructure",
                                                  style="style_screen.TButton",
                                                  command=self.controller.data_get)

        # create and place label for udt info
        self.lbl_udt_datasize = ttk.Label(master=self.screen_data,
                                          style="style_screen.TLabel",
                                          text="Size [Bytes]:",
                                          anchor="w")

        # create and place variable label for udt info
        self.udt_datasize = tk.StringVar()
        self.lbl_udt_datasize_var = ttk.Label(master=self.screen_data,
                                              style="style_screen_var.TLabel",
                                              textvariable=self.udt_datasize,
                                              anchor="center")

        # create checkbox for show offset data in treeview
        self.udt_show_offset = tk.BooleanVar()
        self.udt_show_offset.set(False)
        self.cbx_show_offset = ttk.Checkbutton(master=self.screen_data,
                                               text="Show offset",
                                               variable=self.udt_show_offset,
                                               command=self.treeview_show_offset,
                                               style="style_screen.TCheckbutton")

        # screen setup---------------------------------------------------------
        # create checkbox for option fullscreen
        self.opt_fullscreen = tk.BooleanVar()
        self.opt_fullscreen.set(self.controller.projectfile["opt_fullscreen"])
        self.cbx_fullscreen = ttk.Checkbutton(master=self.screen_setup,
                                              text="Fullscreen",
                                              variable=self.opt_fullscreen,
                                              command=self.window_update,
                                              style="style_screen.TCheckbutton")

        # screen csv---------------------------------------------------------
        # create checkbox for option fullscreen
        self.csv_active = tk.BooleanVar()
        self.csv_active.set(self.controller.projectfile["csv_active"])
        self.cbx_active = ttk.Checkbutton(master=self.screen_csv,
                                          text="Active",
                                          variable=self.csv_active,
                                          command=self.entry_after,
                                          style="style_screen.TCheckbutton")

        # create and place label for filename
        self.lbl_csv_filename = ttk.Label(master=self.screen_csv,
                                          style="style_screen.TLabel",
                                          text="Filename:",
                                          anchor="w")

        # create and place entry for filename
        self.csv_filename = tk.StringVar()
        self.csv_filename.set(self.controller.projectfile["csv_filename"])
        self.entry_csv_filename = ttk.Entry(master=self.screen_csv,
                                            style="style_screen.TEntry",
                                            textvariable=self.csv_filename)
        self.entry_csv_filename.bind("<KeyRelease>", lambda x: self.entry_after())

        # create and place label for filepath
        self.lbl_csv_filepath = ttk.Label(master=self.screen_csv,
                                          style="style_screen.TLabel",
                                          text="Filepath:",
                                          anchor="w")

        # create and place entry for filepath
        self.csv_filepath = tk.StringVar()
        self.csv_filepath.set(self.controller.projectfile["csv_filepath"])
        self.entry_csv_filepath = ttk.Entry(master=self.screen_csv,
                                            style="style_screen.TEntry",
                                            textvariable=self.csv_filepath)
        self.entry_csv_filepath.bind("<KeyRelease>", lambda x: self.entry_after())

        # create button for set filepath
        self.btn_csv_filepath = ttk.Button(master=self.screen_csv,
                                           takefocus=0,
                                           text="set Filepath",
                                           style="style_screen.TButton",
                                           command=self.csv_filepath_get)

        # create and place label for filemode
        self.lbl_csv_filemode = ttk.Label(master=self.screen_csv,
                                          style="style_screen.TLabel",
                                          text="Filemode:",
                                          anchor="w")

        # create radiobutton for filemode1
        self.csv_filemode = tk.IntVar()
        self.csv_filemode.set(self.controller.projectfile["csv_filemode"])
        self.rad_csv_filemode1 = ttk.Radiobutton(master=self.screen_csv,
                                                 takefocus=0,
                                                 text="one file per day",
                                                 style="style_screen.TRadiobutton",
                                                 value=1,
                                                 variable=self.csv_filemode,
                                                 command=self.entry_after)

        # create radiobutton for filemode2
        self.rad_csv_filemode2 = ttk.Radiobutton(master=self.screen_csv,
                                                 takefocus=0,
                                                 text="one big file",
                                                 style="style_screen.TRadiobutton",
                                                 value=2,
                                                 variable=self.csv_filemode,
                                                 command=self.entry_after)

        # create and place label for delimiter
        self.lbl_csv_delimiter = ttk.Label(master=self.screen_csv,
                                           style="style_screen.TLabel",
                                           text="Delimiter:",
                                           anchor="w")

        # create entry for csv delimiter
        self.csv_delimiter = tk.StringVar()
        self.csv_delimiter.set(self.controller.projectfile["csv_delimiter"])
        self.csv_delimiter.trace("w", lambda *args: self.entry_validate(var=self.csv_delimiter, mode="char", length=1))
        self.entry_csv_delimiter = ttk.Entry(master=self.screen_csv,
                                             style="style_screen.TEntry",
                                             textvariable=self.csv_delimiter,
                                             justify="center")
        self.entry_csv_delimiter.bind("<KeyRelease>", lambda x: self.entry_after())

        # create label for Triggermode
        self.lbl_csv_Trigger = ttk.Label(master=self.screen_csv,
                                         style="style_screen.TLabel",
                                         text="Trigger:",
                                         anchor="w")

        # create menu for triggermode
        self.csv_triggermode = tk.StringVar()
        self.csv_triggermode.set(self.controller.projectfile["csv_triggermode"])
        self.csv_triggerchoices = ["boolean", "seconds", "minutes", "hours"]
        self.men_csv_trigger = ttk.OptionMenu(self.screen_csv,  # master=
                                              self.csv_triggermode,  # value=
                                              "None",  # default=
                                              *self.csv_triggerchoices,  # values=
                                              style="style_screen.TMenubutton",
                                              command=lambda x: self.csv_triggermode_change())

        # create entry for time value to save csv
        self.csv_timechange = False
        self.csv_time = tk.StringVar()
        self.csv_time.set(self.controller.projectfile["csv_time"])
        self.csv_time.trace("w", lambda *args: self.entry_validate(var=self.csv_time, mode="min_1", length=2))
        self.entry_csv_time = ttk.Entry(master=self.screen_csv,
                                        style="style_screen.TEntry",
                                        textvariable=self.csv_time)
        self.entry_csv_time.bind("<KeyRelease>", lambda x: self.entry_after())

        # create button for set trigger time
        self.btn_csv_timeset = ttk.Button(master=self.screen_csv,
                                          takefocus=0,
                                          text="set",
                                          style="style_screen.TButton",
                                          command=self.csv_time_change)

        # create label for next trigger time
        self.csv_nexttrigger = tk.StringVar()
        self.lbl_csv_nexttrigger = ttk.Label(master=self.screen_csv,
                                             style="style_screen.TLabel",
                                             textvariable=self.csv_nexttrigger,
                                             anchor="w")

        # create variable label for csv boolean trigger
        self.csv_booltrigger = tk.StringVar()
        self.csv_trigger_name()
        self.lbl_csv_booltrigger_var = ttk.Label(master=self.screen_csv,
                                                 style="style_screen_var.TLabel",
                                                 textvariable=self.csv_booltrigger,
                                                 anchor="center")

        # create button for set csv boolean trigger
        self.btn_csv_booltrigger = ttk.Button(master=self.screen_csv,
                                              takefocus=0,
                                              text="set Trigger",
                                              style="style_screen.TButton",
                                              command=self.csv_trigger_set)

        # create label for csv number of rows
        self.lbl_csv_numrows = ttk.Label(master=self.screen_csv,
                                         style="style_screen.TLabel",
                                         text="Number of Rows:",
                                         anchor="w")

        # create list of csv rowdata (headertext, variabletext, variableindex)
        self.csv_rowdata = self.controller.projectfile["csv_rowdata"].copy()

        # create variable label for csv number of rows
        self.csv_numrows = tk.IntVar()
        self.csv_numrows.set(len(self.csv_rowdata))
        self.lbl_csv_numrows_var = ttk.Label(master=self.screen_csv,
                                             style="style_screen_var.TLabel",
                                             textvariable=self.csv_numrows,
                                             anchor="center")

        # create button for csv number of rows minus
        self.btn_csv_numrowminus = ttk.Button(master=self.screen_csv,
                                              takefocus=0,
                                              text="del",
                                              style="style_screen.TButton",
                                              command=lambda: self.csv_numrows_change(mode="-"))

        # create button for csv number of rows plus
        self.btn_csv_numrowplus = ttk.Button(master=self.screen_csv,
                                             takefocus=0,
                                             text="add",
                                             style="style_screen.TButton",
                                             command=lambda: self.csv_numrows_change(mode="+"))

        # create label for csv actual row
        self.lbl_csv_row = ttk.Label(master=self.screen_csv,
                                     style="style_screen.TLabel",
                                     text="Actual Row:",
                                     anchor="w")

        # create variable label for csv actual row
        self.csv_row = tk.IntVar()
        self.csv_row.set(1)
        self.lbl_csv_row_var = ttk.Label(master=self.screen_csv,
                                         style="style_screen_var.TLabel",
                                         textvariable=self.csv_row,
                                         anchor="center")

        # create button for csv actual row minus
        self.btn_csv_rowminus = ttk.Button(master=self.screen_csv,
                                           takefocus=0,
                                           text="-",
                                           style="style_screen.TButton",
                                           command=lambda: self.csv_actualrow_change(mode="-"))

        # create button for csv actual row plus
        self.btn_csv_rowplus = ttk.Button(master=self.screen_csv,
                                          takefocus=0,
                                          text="+",
                                          style="style_screen.TButton",
                                          command=lambda: self.csv_actualrow_change(mode="+"))

        # create label for csv name of row
        self.lbl_csv_rowtext = ttk.Label(master=self.screen_csv,
                                         style="style_screen.TLabel",
                                         text="Name of Row:",
                                         anchor="w")

        # create entry for csv name of row
        self.csv_rowname = tk.StringVar()
        self.csv_rowname_name()
        self.entry_csv_rowname = ttk.Entry(master=self.screen_csv,
                                           style="style_screen.TEntry",
                                           textvariable=self.csv_rowname,
                                           justify="center")

        # create button for set csv name of row
        self.btn_csv_rowname = ttk.Button(master=self.screen_csv,
                                          takefocus=0,
                                          text="set Name",
                                          style="style_screen.TButton",
                                          command=self.csv_rowname_set)

        # create label for csv data of row
        self.lbl_csv_rowvariable = ttk.Label(master=self.screen_csv,
                                             style="style_screen.TLabel",
                                             text="Data of Row:",
                                             anchor="w")

        # create variable label for csv data of row
        self.csv_rowvariable = tk.StringVar()
        self.csv_rowvariable_name()
        self.lbl_csv_rowvariable_var = ttk.Label(master=self.screen_csv,
                                                 style="style_screen_var.TLabel",
                                                 textvariable=self.csv_rowvariable,
                                                 anchor="center")

        # create button for set csv data of row
        self.btn_csv_rowvariable = ttk.Button(master=self.screen_csv,
                                              takefocus=0,
                                              text="set Variable",
                                              style="style_screen.TButton",
                                              command=self.csv_rowvariable_set)
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
        """
        scale window
        place gui elements
        """
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
        self.csv_table.place(x=10, y=10, width=772 + ox, height=325 + oy)
        self.csv_table_scrollx.place(x=10, y=335 + oy, width=759 + ox)
        self.csv_table_scrolly.place(x=768 + ox, y=30, height=319 + oy)
        self.btn_csv_autoscroll.place(x=700 + ox, y=-4, width=74, height=24)
        self.eventframe.place(x=0, y=482 + oy - self.eventframeoffs, height=35 + self.eventframeoffs, width=797 + ox)
        self.lbl_eventframe.place(x=1, y=1, width=795 + ox, height=20)
        self.btn_eve_autoscroll.place(x=724 + ox, y=-10, width=74, height=40)
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
        self.lbl_runstop.place(x=50, y=97, width=80, height=25)
        self.cbx_runstop.place(x=135, y=91, width=40, height=40)
        self.cbx_autostart.place(x=180, y=91, width=80, height=40)
        self.lbl_show_recvdata.place(x=50, y=136, width=192, height=25)
        self.cbx_show_recvdata.place(x=245, y=129, width=21, height=40)
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
        self.lbl_udt_datasize.place(x=580 + ox, y=437 + oy, width=85, height=25)
        self.lbl_udt_datasize_var.place(x=670 + ox, y=437 + oy, width=83, height=25)
        self.cbx_show_offset.place(x=580 + ox, y=465 + oy, width=100, height=25)
        # scale gui elements from screen setup---------------------------------
        self.cbx_fullscreen.place(x=50, y=25, width=90, height=40)
        # scale gui elements from screen csv-----------------------------------
        self.cbx_active.place(x=50, y=25, width=90, height=40)
        self.lbl_csv_filename.place(x=50, y=58, width=80, height=25)
        self.entry_csv_filename.place(x=135, y=58, width=300, height=25)
        self.lbl_csv_filepath.place(x=50, y=91, width=80, height=25)
        self.entry_csv_filepath.place(x=135, y=91, width=300, height=25)
        self.btn_csv_filepath.place(x=445, y=91, width=100, height=25)
        self.lbl_csv_filemode.place(x=50, y=124, width=80, height=25)
        self.rad_csv_filemode1.place(x=135, y=124, width=120, height=25)
        self.rad_csv_filemode2.place(x=280, y=124, width=95, height=25)
        self.lbl_csv_delimiter.place(x=400, y=124, width=95, height=25)
        self.entry_csv_delimiter.place(x=480, y=124, width=30, height=25)
        self.lbl_csv_Trigger.place(x=50, y=157, width=80, height=25)
        self.men_csv_trigger.place(x=135, y=157, width=95, height=25)
        if self.csv_triggermode.get() == "boolean":
            self.entry_csv_time.place_forget()
            self.btn_csv_timeset.place_forget()
            self.lbl_csv_nexttrigger.place_forget()
            self.lbl_csv_booltrigger_var.place(x=240, y=157, width=195, height=25)
            self.btn_csv_booltrigger.place(x=445, y=157, width=100, height=25)
        else:
            self.lbl_csv_booltrigger_var.place_forget()
            self.btn_csv_booltrigger.place_forget()
            self.entry_csv_time.place(x=240, y=157, width=30, height=25)
            self.btn_csv_timeset.place(x=280, y=157, width=60, height=25)
            self.lbl_csv_nexttrigger.place(x=350, y=157, width=440, height=25)
        self.lbl_csv_numrows.place(x=50, y=190, width=110, height=25)
        self.lbl_csv_numrows_var.place(x=240, y=190, width=30, height=25)
        self.btn_csv_numrowminus.place(x=170, y=190, width=60, height=25)
        self.btn_csv_numrowplus.place(x=280, y=190, width=60, height=25)
        self.lbl_csv_row.place(x=50, y=223, width=110, height=25)
        self.lbl_csv_row_var.place(x=240, y=223, width=30, height=25)
        self.btn_csv_rowminus.place(x=170, y=223, width=60, height=25)
        self.btn_csv_rowplus.place(x=280, y=223, width=60, height=25)
        self.lbl_csv_rowtext.place(x=50, y=256, width=110, height=25)
        self.entry_csv_rowname.place(x=170, y=256, width=265, height=25)
        self.btn_csv_rowname.place(x=445, y=256, width=100, height=25)
        self.lbl_csv_rowvariable.place(x=50, y=289, width=110, height=25)
        self.lbl_csv_rowvariable_var.place(x=170, y=289, width=265, height=25)
        self.btn_csv_rowvariable.place(x=445, y=289, width=100, height=25)
        if not self.controller.projectfile["opt_fullscreen"]:
            self.controller.projectfile["opt_windowwidth"] = self.window.winfo_width()
            self.controller.projectfile["opt_windowheight"] = self.window.winfo_height()

    def window_update(self):
        """
        update windowsize and position
        """
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
        """
        change height of event log while dragging it with the mouse
        """
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
        """
        write text into event log with timestamp
        """
        self.txt_eventframe.configure(state="normal")
        timestamp = self.controller.timestamp_get()
        self.txt_eventframe.insert(tk.END, "{timestamp}: {text}\n".format(timestamp=timestamp, text=text))
        self.txt_eventframe.configure(state="disabled")
        if self.eventlog_autoscroll_var.get():
            self.txt_eventframe.yview_moveto("1.0")

    def keyup(self, event):
        """
        special actions when a key gets released
        """
        # print(event)
        # if event.keysym == "Tab": self.method()
        pass

    def keydown(self, event):
        """
        special actions when a key gets pressed
        """
        # print(event)
        pass

    @staticmethod
    def entry_validate(var, mode, length):
        """
        check keyboard input on gui element depending on the selected mode
        """
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
        if mode == "number":
            # set text to maximum length
            if len(text) > length:
                text = text[:length]
            # delete all non digits
            newtext = ""
            for char in text:
                if str.isdigit(char):
                    newtext += char
            text = newtext
        if mode == "min_1":
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
                if int(text) < 1:
                    text = "1"
        if mode == "char":
            # set text to maximum length
            if len(text) > length:
                text = text[:length]
        var.set(text)

    def entry_after(self):
        """
        save content of gui element after the input is done
        """
        self.controller.projectfile["con_ip_byte1"] = self.con_ip_byte1.get()
        self.controller.projectfile["con_ip_byte2"] = self.con_ip_byte2.get()
        self.controller.projectfile["con_ip_byte3"] = self.con_ip_byte3.get()
        self.controller.projectfile["con_ip_byte4"] = self.con_ip_byte4.get()
        self.controller.projectfile["con_port"] = self.con_port.get()
        self.controller.projectfile["csv_active"] = self.csv_active.get()
        self.controller.projectfile["csv_filename"] = self.csv_filename.get()
        self.controller.projectfile["csv_filepath"] = self.csv_filepath.get()
        self.controller.projectfile["csv_filemode"] = self.csv_filemode.get()
        self.controller.projectfile["csv_triggermode"] = self.csv_triggermode.get()
        self.controller.projectfile["csv_time"] = self.csv_time.get()
        self.controller.projectfile["csv_delimiter"] = self.csv_delimiter.get()

    def filepath_open(self, message=None, filetypes=((), ("all files", "*.*"))):
        """
        show message if message is not None
        open file dialog and return the filepath
        """
        if message is not None:
            tk.messagebox.showinfo(title=None, message=message)
        path = tk.filedialog.askopenfilename(initialdir=self.desktoppath, title="select File",
                                             filetypes=filetypes)
        return path

    def filepath_saveas(self, filetypes=((), ("all files", "*.*"))):
        """
        open file dialog and return the filepath
        """
        path = tk.filedialog.asksaveasfilename(initialdir=self.desktoppath, title="save as...",
                                               filetypes=filetypes,
                                               defaultextension=filetypes[0][1])
        return path

    def filepath_directory(self):
        """
        open file dialog and return the directory path
        """
        path = tk.filedialog.askdirectory(initialdir=self.desktoppath, title="choose Folder")
        return path

    def about_show(self):
        """
        show software infos
        """
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
        """
        clear data on screen data
        delete all entries in datatree
        """
        for element in self.datatree.get_children():
            self.datatree.delete(element)
        self.udt_name.set("")
        self.udt_description.set("")
        self.udt_version.set("")
        self.udt_info.set("")
        self.udt_datasize.set("")

    def datatree_fill(self, name, description, version, info, data):
        """
        insert entries in datatree
        """
        self.udt_name.set(name)
        self.udt_description.set(description)
        self.udt_version.set(version)
        self.udt_info.set(info)
        # check every element,
        folderpath = [""]
        for element in data:
            # put actual data in datatree in the actual folder
            el_name = element["name"]
            el_datatype = element["datatype"]
            el_byte = element["byte"]
            el_comment = element["comment"]
            el_visible = element["visible"]
            el_action = element["action"]
            el_value = element["value"]
            el_address = None
            # insert element to treeview if element has "visible" flag
            if el_visible:
                el_address = self.datatree.insert(folderpath[-1],
                                                  "end",
                                                  text=el_name,
                                                  values=(el_datatype, el_value, el_byte, el_comment))
            # insert element to treeview if element has "offset" flag
            if el_action == "offset" and self.udt_show_offset.get():
                el_address = self.datatree.insert(folderpath[-1],
                                                  "end",
                                                  text=el_name,
                                                  values=(el_datatype, el_value, el_byte, el_comment))
            # open this element as new folder if element has "open" flag
            if el_action == "open":
                # save name to folderpath
                folderpath.append(el_address)
            # close folder if element has "close" flag
            if el_action == "close":
                # delete name from folderpath
                folderpath.pop()
            # save element id in data
            element["variable"] = el_address

    def datatree_update(self):
        """
        update data on screen data
        update all entries in datatree
        """
        name = self.controller.projectfile["udt_name"]
        description = self.controller.projectfile["udt_description"]
        version = self.controller.projectfile["udt_version"]
        info = self.controller.projectfile["udt_info"]
        datasize = self.controller.projectfile["udt_datasize"]
        data = self.controller.projectfile["udt_datastructure"]
        # clear data in datatree
        self.datatree_clear()
        # fill data in datatree
        self.datatree_fill(name, description, version, info, data)
        self.udt_datasize.set(datasize)

    def datatree_values_set(self):
        """
        update value in datatree
        """
        data = self.controller.projectfile["udt_datastructure"]
        for element in data:
            # find the elements where "variable" is stored (elements that are shown in treeview)
            if element["variable"] is not None:
                # get values from this entry in datatree
                entry_data = self.datatree.item(element["variable"])
                entry_values = entry_data["values"]
                # update values
                entry_values[1] = element["value"]
                # save values
                self.datatree.item(element["variable"], values=entry_values)

    def csv_table_clear(self):
        """
        clear data on screen home csv table
        delete all entries in datatree
        """
        self.csv_table_rebuild = True
        for element in self.csv_table.get_children():
            self.csv_table.delete(element)
        self.csv_table["columns"] = ""
        self.csv_table.column("#0", width=self.csv_table.winfo_width())
        self.csv_table.heading("#0", text="")

    def csv_table_insert(self, timestamp, header, data):
        """
        fill table with data
        """
        if self.csv_table_rebuild:
            self.csv_table.column("#0", width=120, minwidth=50, stretch=tk.YES, anchor="center")
            self.csv_table.heading("#0", text="Time", anchor="center")
            header.append("last")
            self.csv_table["columns"] = header
            for col in self.csv_table["columns"]:
                self.csv_table.column(col, width=100, minwidth=50, stretch=tk.YES, anchor="center")
                self.csv_table.heading(col, text=col, anchor="center")
            self.csv_table.column("last", width=100, minwidth=100, stretch=tk.NO, anchor="center")
            self.csv_table.heading("last", text="", anchor="center")
            self.csv_table_rebuild = False
        self.csv_table.insert("", "end", text=timestamp, values=" ".join(data))
        self.csv_table_scroll()

    def csv_table_scroll(self):
        """
        scroll Treeview to the end if scroll is activated
        """
        if self.csv_table_autoscroll_var.get():
            self.csv_table.yview_moveto(1)

    def csv_table_autoscroll(self):
        """
        toggle autoscroll
        """
        if self.csv_table_autoscroll_var.get():
            self.csv_table_autoscroll_var.set(False)
            self.style_btn_csv_table.configure("style_csv_table.TButton", foreground=self.midcolor, anchor=tk.N)
        else:
            self.csv_table_autoscroll_var.set(True)
            self.style_btn_csv_table.configure("style_csv_table.TButton", foreground="#FFFFFF", anchor=tk.S)

    def home_update(self):
        """
        update data on screen home
        """
        self.csv_table_clear()

    def server_update(self):
        """
        update data on screen server
        """
        self.con_ip_byte1.set(self.controller.projectfile["con_ip_byte1"])
        self.con_ip_byte2.set(self.controller.projectfile["con_ip_byte2"])
        self.con_ip_byte3.set(self.controller.projectfile["con_ip_byte3"])
        self.con_ip_byte4.set(self.controller.projectfile["con_ip_byte4"])
        self.con_port.set(self.controller.projectfile["con_port"])
        self.con_autostart.set(self.controller.projectfile["con_autostart"])
        self.con_show_recvdata.set(self.controller.projectfile["con_show_recvdata"])
        self.csv_delimiter.set(self.controller.projectfile["csv_delimiter"])

    def setup_update(self):
        """
        update data on screen setup
        """
        self.opt_fullscreen.set(self.controller.projectfile["opt_fullscreen"])

    def csv_update(self):
        """
        update data on screen csv
        """
        self.csv_active.set(self.controller.projectfile["csv_active"])
        self.csv_filename.set(self.controller.projectfile["csv_filename"])
        self.csv_filepath.set(self.controller.projectfile["csv_filepath"])
        self.csv_filemode.set(self.controller.projectfile["csv_filemode"])
        self.csv_triggermode.set(self.controller.projectfile["csv_triggermode"])
        self.csv_time.set(self.controller.projectfile["csv_time"])
        self.csv_trigger_name()
        self.csv_rowdata = self.controller.projectfile["csv_rowdata"].copy()
        self.csv_row.set(1)
        self.csv_numrows.set(len(self.csv_rowdata))
        self.csv_rowname_name()
        self.csv_rowvariable_name()

    def led_state(self, state="error"):
        """
        change image of led element depending on its state
        """
        if state != self.icon_led_last_state:
            if state == "error":
                self.icon_led.create_image(0, 0, image=self.img_led_rd, anchor="nw")
            elif state == "warn":
                self.icon_led.create_image(0, 0, image=self.img_led_ye, anchor="nw")
            elif state == "ok":
                self.icon_led.create_image(0, 0, image=self.img_led_gn, anchor="nw")
            else:
                self.icon_led.create_image(0, 0, image=self.img_led_rd, anchor="nw")
        self.icon_led_last_state = state

    def connect_autostart(self):
        """
        save content of checkbox after the state has changed
        """
        self.controller.projectfile["con_autostart"] = self.con_autostart.get()

    def connect_show_recvdata(self):
        """
        save content of checkbox after the state has changed
        """
        self.controller.projectfile["con_show_recvdata"] = self.con_show_recvdata.get()

    def connect_state(self):
        """
        toggle checkbutton
        """
        state = self.runstop.get()
        if state:
            self.controller.server_start()
        elif not state:
            self.controller.server_stop()

    def eventlog_autoscroll(self):
        """
        toggle autoscroll
        """
        if self.eventlog_autoscroll_var.get():
            self.eventlog_autoscroll_var.set(False)
            self.style_btn_eventframe.configure("style_eventframe.TButton", foreground=self.midcolor)
        else:
            self.eventlog_autoscroll_var.set(True)
            self.style_btn_eventframe.configure("style_eventframe.TButton", foreground="#FFFFFF")

    def treeview_show_offset(self):
        """
        trigger datatree_update after state has changed
        """
        self.datatree_update()

    def csv_filepath_get(self):
        """
        save content of chosen directory path
        """
        filepath = self.filepath_directory()
        self.csv_filepath.set(filepath)
        self.entry_after()

    def csv_triggermode_change(self):
        """
        if triggermode is changed
        call window scale to hide or show the depending elements
        refresh list of all possible boolean triggers
        """
        self.controller.projectfile["csv_triggermode"] = self.csv_triggermode.get()
        self.window_scale()

    def csv_time_change(self):
        """
        set csv trigger time
        """
        self.controller.projectfile["csv_time"] = self.csv_time.get()
        self.csv_timechange = True

    def csv_numrows_change(self, mode=""):
        """
        change the number of csv rows
        """
        numberofrows = self.csv_numrows.get()
        if mode == "+":
            numberofrows += 1
            self.csv_rowdata.append({"Text": "", "Variable": 0})
        elif mode == "-":
            if numberofrows > 1:
                numberofrows -= 1
                self.csv_rowdata.pop()
        else:
            pass
        self.controller.projectfile["csv_rowdata"] = self.csv_rowdata.copy()
        self.csv_row.set(1)
        self.csv_numrows.set(len(self.csv_rowdata))
        self.csv_rowname_name()
        self.csv_rowvariable_name()
        self.csv_table_clear()

    def csv_actualrow_change(self, mode=""):
        """
        change the actual shown csv rowdata
        actual row + or -
        check boundaries
        """
        row = self.csv_row.get()
        maximum = int(self.csv_numrows.get())
        minimum = 1
        if mode == "+":
            row += 1
        elif mode == "-":
            row -= 1
        else:
            pass
        if row > maximum:
            row = minimum
        if row < minimum:
            row = maximum
        self.csv_row.set(row)
        self.csv_rowname_name()
        self.csv_rowvariable_name()

    def csv_trigger_set(self):
        """
        get selected element in Data and save its address in projectfile
        """
        data = self.controller.projectfile["udt_datastructure"]
        selected_id = self.datatree.focus()
        selected_name = self.datatree.item(selected_id, "text")
        for element in data:
            if element["name"] == selected_name and element["datatype"] == "Bool" and element["access"] is True:
                self.controller.projectfile["csv_booltrigger"] = data.index(element)
        self.csv_trigger_name()

    def csv_trigger_name(self):
        """
        read name of trigger from datastructure and set the variable name of trigger
        """
        data = self.controller.projectfile["udt_datastructure"]
        index = self.controller.projectfile["csv_booltrigger"]
        if len(data) > 0:
            text = data[index]["name"]
        else:
            text = ""
        self.csv_booltrigger.set(text)

    def csv_rowvariable_set(self):
        """
        get selected element in Data and save its address in projectfile
        """
        data = self.controller.projectfile["udt_datastructure"]
        selected_id = self.datatree.focus()
        selected_name = self.datatree.item(selected_id, "text")
        for element in data:
            if element["name"] == selected_name and element["access"] is True:
                self.csv_rowdata[self.csv_row.get() - 1]["Variable"] = data.index(element)
                self.controller.projectfile["csv_rowdata"] = self.csv_rowdata.copy()
        self.csv_rowvariable_name()
        self.csv_table_clear()

    def csv_rowvariable_name(self):
        """
        read name of variable from datastructure and set the variable name
        """
        data = self.controller.projectfile["udt_datastructure"]
        self.csv_rowdata = self.controller.projectfile["csv_rowdata"].copy()
        index = self.csv_rowdata[self.csv_row.get() - 1]["Variable"]
        if len(data) > 0:
            text = data[index]["name"]
        else:
            text = ""
        self.csv_rowvariable.set(text)

    def csv_rowname_set(self):
        """
        get data from entry and save its text in projectfile
        """
        self.csv_rowdata[self.csv_row.get() - 1]["Text"] = self.csv_rowname.get()
        self.controller.projectfile["csv_rowdata"] = self.csv_rowdata.copy()
        self.csv_rowvariable_name()
        self.csv_table_clear()

    def csv_rowname_name(self):
        """
        read name of variable from projectfile and set the variable name
        """
        self.csv_rowdata = self.controller.projectfile["csv_rowdata"].copy()
        self.csv_rowname.set(self.csv_rowdata[self.csv_row.get() - 1]["Text"])
