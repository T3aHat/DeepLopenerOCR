import eel
import time
import keyboard
import pyperclip
import configparser
import os
import getpass


# batから実行する場合はcmd.exeが出てしまうので
# .lnkを作成してStart Menuに実行した方が見栄えが良い

def add_to_startup_bat():
    folder_path = os.path.dirname(os.path.realpath(__file__))
    file_path = folder_path+"\deeplopenerproexe.py"
    bat_path = r"C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup" % getpass.getuser()
    with open(bat_path + "\\" + "open.bat", "w+") as bat_file:
        bat_file.write("cd "+folder_path+'\nstart "" ' +
                       folder_path+"\dist\deeplopenerproexe.exe")
    return folder_path

# add_to_startup_bat()


@eel.expose
def py_get_settings():
    global firstFlag
    if(firstFlag):
        firstFlag = False
        return target_lang, command, api_key, True
    else:
        firstFlag = False
        return target_lang, command, api_key, False


@ eel.expose
def py_save_settings(targetlang, cmd, apikey):
    global target_lang, command, api_key
    command = cmd
    target_lang = targetlang

    config.set(section, "target_lang", target_lang)
    if(apikey != ""):
        api_key = apikey
        config.set(section, "api_key", api_key)
    keyboard.unhook_all_hotkeys()
    keyboard.add_hotkey('ctrl+C', send_clipboard,
                        args=[target_lang, api_key])
    config.set(section, "command", command)
    if(command != "ctrl+C"):
        keyboard.add_hotkey(command, send_clipboard,
                            args=[target_lang, api_key])
    with open("config.ini", "w")as f:
        config.write(f)
    return "saved"+command


@eel.expose
def py_open_options():
    global optionsFlag
    optionsFlag = True


def send_clipboard(target_lang, api_key):
    print("key detect")
    global now, beforekeycc, beforetxt
    if(not keyboard.is_pressed("ctrl+C") and not beforekeycc):
        pass
    elif(time.time()-now < 1 and pyperclip.paste() != "" and pyperclip.paste() != beforetxt):
        eel.start("main.html", block=False, clsose_callback=onCloseWindow)
        eel.sleep(1)  # 読み込まれるまで待機(雑)
        eel.js_translate(pyperclip.paste(), target_lang, api_key)
        beforetxt = pyperclip.paste()
    now = time.time()
    beforekeycc = keyboard.is_pressed("ctrl+C")


def onCloseWindow(page, sockets):
    pass


if __name__ == '__main__':
    now = time.time()
    config = configparser.ConfigParser()
    section = "DeepLopenerPROEXE"
    beforekeycc = True
    optionsFlag = False
    firstFlag = True
    beforetxt = ""

    try:
        config.read("config.ini")
        target_lang = config.get(section, "target_lang")
        api_key = config.get(section, "api_key")
        command = config.get(section, "command")
        if(command != "ctrl+C"):
            keyboard.add_hotkey(command, send_clipboard,
                                args=[target_lang, api_key])
    except:
        target_lang = "JA"
        api_key = ""
        command = "ctrl+C"
        config.add_section(section)
        config.set(section, "target_lang", target_lang)
        config.set(section, "api_key", api_key)
        config.set(section, "command", command)
        with open("config.ini", "w")as f:
            config.write(f)

    keyboard.add_hotkey('ctrl+C', send_clipboard,
                        args=[target_lang, api_key])
    eel.init("assets")
    while True:
        eel.start("main.html", close_callback=onCloseWindow)
