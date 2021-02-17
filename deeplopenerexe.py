import eel
import os
import subprocess
import time
import shutil
import keyboard
import pyperclip
import configparser


@eel.expose
def py_first_target():
    print(command)
    print(target_lang, command, api_key)
    return target_lang, command, api_key


@ eel.expose
def py_save_settings(targetlang, cmd, apikey):
    global target_lang, command, api_key
    command = cmd
    target_lang = targetlang
    print(targetlang, command, apikey)

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
    # write settings
    with open("config.ini", "w")as f:
        config.write(f)
    return "saved"+command


def send_clipboard(target_lang, api_key):
    global now, beforekeycc
    print("sendclipboard:"+target_lang+" : "+api_key)
    print(keyboard.is_pressed("ctrl+C"))
    if(not keyboard.is_pressed("ctrl+C") and not beforekeycc):
        print("VV")
        pass
    elif(time.time()-now < 1 and pyperclip.paste() != ""):
        eel.js_translate(pyperclip.paste(), target_lang, api_key)
    now = time.time()
    beforekeycc = keyboard.is_pressed("ctrl+C")


if __name__ == '__main__':
    now = time.time()
    config = configparser.ConfigParser()
    section = "DeepLopenerPROEXE"
    beforekeycc = True
    try:
        config.read("config.ini")
        target_lang = config.get(section, "target_lang")
        api_key = config.get(section, "api_key")
        command = config.get(section, "command")
        keyboard.add_hotkey(command, send_clipboard,
                            args=[target_lang, api_key])
    except:
        target_lang = input("target language : ")
        api_key = input("DeepL Pro API_KEY : ")
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
    eel.start("main.html")
