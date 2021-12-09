import eel
import time
import keyboard
import pyperclip
import configparser
import os
import re
from PIL import ImageGrab, Image
# for bat
import getpass
import pyocr
import time


def ocr(im, target, apikey):
    global win_opening
    pyocr.tesseract.TESSERACT_CMD = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    engines = pyocr.get_available_tools()
    if len(engines) == 0:
        print("Tesseract is not found")
    else:
        engine = engines[0]
        txt = engine.image_to_string(im, lang="eng")
        txt = re.sub(r"(\w)\n+?([\w])", r"\1 \2", txt)
        print(txt)
        if(len(txt.replace("\n", "").replace(" ", "")) > 0):
            if(not win_opening):
                win_opening = True
                eel.show("main.html")
                eel.sleep(1)  # 読み込まれるまで待機(雑)
            eel.js_translate(txt, target, apikey)


def capture():
    global target_lang, api_key
    image = ImageGrab.grabclipboard()
    while True:
        im = ImageGrab.grabclipboard()
        if isinstance(im, Image.Image) and im != image:
            ocr(im, target_lang, api_key)
        else:
            pass
        image = ImageGrab.grabclipboard()
        eel.sleep(1)


def add_to_startup_bat():
    folder_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r"C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup" % getpass.getuser()
    with open(bat_path + "\\" + "DeepLopenerOCR.bat", "w+") as bat_file:
        bat_file.write("cd "+folder_path+'\nstart "" ' +
                       folder_path+"\dist\DeepLopenerOCR\DeepLopenerOCR.exe")
    return folder_path


@eel.expose
def py_get_settings():
    global firstFlag
    if(firstFlag):
        firstFlag = False
        return target_lang, command, api_key, freeflag, True
    else:
        firstFlag = False
        return target_lang, command, api_key, freeflag, False


@ eel.expose
def py_save_settings(targetlang, cmd, apikey, freeflg):
    global target_lang, command, api_key, freeflag
    command = cmd
    target_lang = targetlang
    freeflag = freeflg

    config.set(section, "target_lang", target_lang)
    if(apikey != ""):
        api_key = apikey
        config.set(section, "api_key", api_key)
    keyboard.unhook_all_hotkeys()
    keyboard.add_hotkey('ctrl+C', send_clipboard,
                        args=[target_lang, api_key])
    config.set(section, "command", command)
    config.set(section, "freeflag", freeflag)

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
    global now, beforekeycc, beforetxt, win_opening
    print("key detect")
    if(not keyboard.is_pressed("ctrl+C") and not beforekeycc):
        pass
    elif(time.time()-now < 1 and pyperclip.paste() != "" and pyperclip.paste() != beforetxt):
        if(not win_opening):
            win_opening = True
            eel.show("main.html")
            eel.sleep(1)  # 読み込まれるまで待機(雑)
        eel.js_translate(pyperclip.paste(), target_lang, api_key)
        beforetxt = pyperclip.paste()
    now = time.time()
    beforekeycc = keyboard.is_pressed("ctrl+C")


def onCloseWindow(page, sockets):
    global win_opening
    win_opening = False
    pass


if __name__ == '__main__':
    now = time.time()
    config = configparser.ConfigParser()
    section = "DeepLopenerOCR"
    beforekeycc = True
    optionsFlag = False
    firstFlag = True
    beforetxt = ""
    win_opening = False
    # 自動起動.bat存在確認
    if not os.path.exists(r"C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\DeepLopenerOCR.bat" % getpass.getuser()):
        try:
            add_to_startup_bat()
        except:
            pass
    try:
        config.read("config.ini")
        target_lang = config.get(section, "target_lang")
        api_key = config.get(section, "api_key")
        command = config.get(section, "command")
        if(command != "ctrl+C"):
            keyboard.add_hotkey(command, send_clipboard,
                                args=[target_lang, api_key])
        freeflag = config.get(section, "freeflag")

    except:
        target_lang = "JA"
        api_key = ""
        command = "ctrl+C"
        freeflag = "Free"
        config.add_section(section)
        config.set(section, "target_lang", target_lang)
        config.set(section, "api_key", api_key)
        config.set(section, "command", command)
        config.set(section, "freeflag", freeflag)
        with open("config.ini", "w")as f:
            config.write(f)

    keyboard.add_hotkey('ctrl+C', send_clipboard,
                        args=[target_lang, api_key])
    eel.init("assets")
    eel.spawn(capture)
    print("start")
    while True:
        win_opening = True
        eel.start("main.html", close_callback=onCloseWindow)