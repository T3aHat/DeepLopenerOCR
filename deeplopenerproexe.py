from re import T
import eel
import sys
import time
import keyboard
import pyperclip
import configparser
import threading


@eel.expose
def py_get_settings():
    global firstFlag
    firstFlag = True
    return target_lang, command, api_key


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


@eel.expose
def py_close():
    # sys.exit()
    pass


def send_clipboard(target_lang, api_key):
    print("key detect")
    global now, beforekeycc
    if(not keyboard.is_pressed("ctrl+C") and not beforekeycc):
        pass
    elif(time.time()-now < 1 and pyperclip.paste() != ""):
        eel.start("main.html", block=False, clsose_callback=onCloseWindow)
        eel.sleep(1)  # 読み込まれるまで待機(雑)
        eel.js_translate(pyperclip.paste(), target_lang, api_key)
    now = time.time()
    beforekeycc = keyboard.is_pressed("ctrl+C")


def onCloseWindow(page, sockets):
    pass


def work1():
    eel.js_close_first()


if __name__ == '__main__':
    now = time.time()
    config = configparser.ConfigParser()
    section = "DeepLopenerPROEXE"
    beforekeycc = True
    optionsFlag = False
    firstFlag = False
    try:
        config.read("config.ini")
        target_lang = config.get(section, "target_lang")
        api_key = config.get(section, "api_key")
        command = config.get(section, "command")
        if(command != "ctrl+C"):
            keyboard.add_hotkey(command, send_clipboard,
                                args=[target_lang, api_key])
    except:
        '''
        target_lang = input("target language : ")
        api_key = input("DeepL Pro API_KEY : ")
        '''
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
    t = threading.Timer(1, work1)
    t.start()
    eel.start("main.html", close_callback=onCloseWindow)
