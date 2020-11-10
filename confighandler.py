import configparser


def readconfig(filepath="config.wdb"):
    # read data from configfile
    configfile = configparser.ConfigParser()
    configfile.read(filepath)
    configdata = {}
    # get GENERAL settings
    configdata["version"] = configfile["GENERAL"].get("version")
    configdata["title"] = configfile["GENERAL"].get("title")
    configdata["font"] = configfile["GENERAL"].get("font")
    # get WINDOW settings
    configdata["fullscreen"] = configfile["WINDOW"].getboolean("fullscreen")
    configdata["min_width"] = configfile["WINDOW"].getint("min_width")
    configdata["min_height"] = configfile["WINDOW"].getint("min_height")
    configdata["max_width"] = configfile["WINDOW"].getint("max_width")
    configdata["max_height"] = configfile["WINDOW"].getint("max_height")
    configdata["start_width"] = configfile["WINDOW"].getint("start_width")
    configdata["start_height"] = configfile["WINDOW"].getint("start_height")
    # get MEDIA settings
    configdata["Media_icon"] = configfile["MEDIA"].get("icon")
    configdata["Media_logo"] = configfile["MEDIA"].get("logo")
    configdata["Media_save"] = configfile["MEDIA"].get("save")
    configdata["Media_import"] = configfile["MEDIA"].get("import")
    configdata["Media_export"] = configfile["MEDIA"].get("export")
    configdata["Media_start"] = configfile["MEDIA"].get("start")
    configdata["Media_plc"] = configfile["MEDIA"].get("plc")
    configdata["Media_daten"] = configfile["MEDIA"].get("daten")
    configdata["Media_setup"] = configfile["MEDIA"].get("setup")
    configdata["Media_help"] = configfile["MEDIA"].get("help")
    configdata["Media_exit"] = configfile["MEDIA"].get("exit")
    configdata["Media_version"] = configfile["MEDIA"].get("version")
    configdata["Media_clock"] = configfile["MEDIA"].get("clock")
    # get COLOR settings
    configdata["Color_bar"] = configfile["COLOR"]["bar"]
    configdata["Color_frame"] = configfile["COLOR"]["frame"]
    configdata["Color_btn_actbg"] = configfile["COLOR"]["btn_actbg"]
    configdata["Color_btn_actfg"] = configfile["COLOR"]["btn_actfg"]
    configdata["Color_txt_fg"] = configfile["COLOR"]["txt_fg"]
    return configdata

def writeconfig(configdata, filepath="config.wdb"):
    configfile = configparser.ConfigParser()
    # set GENERAL settings
    configfile['GENERAL'] = {}
    configfile["GENERAL"]["version"] = configdata["version"]
    configfile["GENERAL"]["title"] = configdata["title"]
    configfile["GENERAL"]["font"] = configdata["font"]
    # get WINDOW settings
    configfile["WINDOW"]["fullscreen"] = str(configdata["fullscreen"])
    configfile["WINDOW"]["min_width"] = str(configdata["min_width"])
    configfile["WINDOW"]["min_height"] = str(configdata["min_height"])
    configfile["WINDOW"]["max_width"] = str(configdata["max_width"])
    configfile["WINDOW"]["max_height"] = str(configdata["max_height"])
    configfile["WINDOW"]["start_width"] = str(configdata["start_width"])
    configfile["WINDOW"]["start_height"] = str(configdata["start_height"])
    # set MEDIA settings
    configfile["MEDIA"]["icon"] = configdata["Media_icon"]
    configfile["MEDIA"]["logo"] = configdata["Media_logo"]
    configfile["MEDIA"]["save"] = configdata["Media_save"]
    configfile["MEDIA"]["import"] = configdata["Media_import"]
    configfile["MEDIA"]["export"] = configdata["Media_export"]
    configfile["MEDIA"]["start"] = configdata["Media_start"]
    configfile["MEDIA"]["plc"] = configdata["Media_plc"]
    configfile["MEDIA"]["daten"] = configdata["Media_daten"]
    configfile["MEDIA"]["setup"] = configdata["Media_setup"]
    configfile["MEDIA"]["help"] = configdata["Media_help"]
    configfile["MEDIA"]["exit"] = configdata["Media_exit"]
    configfile["MEDIA"]["version"] = configdata["Media_version"]
    configfile["MEDIA"]["clock"] = configdata["Media_clock"]
    # set COLOR settings
    configfile["COLOR"]["bar"] = configdata["Color_bar"]
    configfile["COLOR"]["frame"] = configdata["Color_frame"]
    configfile["COLOR"]["btn_actbg"] = configdata["Color_btn_actbg"]
    configfile["COLOR"]["btn_actfg"] = configdata["Color_btn_actfg"]
    configfile["COLOR"]["txt_fg"] = configdata["Color_txt_fg"]
    # write data to configfile
    with open(filepath, 'w') as configuration:
        configfile.write(configuration)