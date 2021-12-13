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
    global win_opening, optionsFlag
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


@eel.expose
def py_get_settings():
    global firstFlag
    if(firstFlag):
        firstFlag = False
        return target_lang, command, api_key, freeFlag, ocrFlag, True
    else:
        firstFlag = False
        return target_lang, command, api_key, freeFlag, ocrFlag, False


@ eel.expose
def py_save_settings(targetlang, cmd, apikey, freeflg, ocrflg):
    global target_lang, command, api_key, freeFlag, ocrFlag
    command = cmd
    target_lang = targetlang
    freeFlag = freeflg
    ocrFlag = ocrflg

    config.set(section, "target_lang", target_lang)
    if(apikey != ""):
        api_key = apikey
        config.set(section, "api_key", api_key)
    keyboard.unhook_all_hotkeys()
    keyboard.add_hotkey('ctrl+C', send_clipboard,
                        args=[target_lang, api_key])
    config.set(section, "command", command)
    config.set(section, "freeFlag", freeFlag)
    config.set(section, "ocrFlag", ocrFlag)

    if(command != "ctrl+C"):
        keyboard.add_hotkey(command, send_clipboard,
                            args=[target_lang, api_key])
    with open("config.ini", "w")as f:
        config.write(f)
    return "saved "+command


@ eel.expose
def py_save_ocr_settings(ocrflg):
    global ocrFlag, spawn
    ocrFlag = ocrflg
    spawn.kill()
    if(ocrFlag == "True"):
        spawn = eel.spawn(capture)
    config.set(section, "target_lang", target_lang)
    config.set(section, "api_key", api_key)
    config.set(section, "command", command)
    config.set(section, "freeFlag", freeFlag)
    config.set(section, "ocrFlag", ocrFlag)
    with open("config.ini", "w")as f:
        config.write(f)
    return "saved "+command


@eel.expose
def py_open_options():
    global optionsFlag
    optionsFlag = True
    print("py_open_options", optionsFlag, win_opening)


def send_clipboard(target_lang, api_key):
    global now, beforekeycc, beforetxt, win_opening, optionsFlag
    print("key detect")
    if(not keyboard.is_pressed("ctrl+C") and not beforekeycc):
        pass
    elif(time.time()-now < 0.5 and pyperclip.paste() != "" and pyperclip.paste() != beforetxt):
        print(optionsFlag, win_opening)
        if(not win_opening):
            win_opening = True
            eel.show("main.html")
            eel.sleep(1)  # 読み込まれるまで待機(雑)
        eel.js_translate(pyperclip.paste(), target_lang, api_key)
        beforetxt = pyperclip.paste()
    now = time.time()
    beforekeycc = keyboard.is_pressed("ctrl+C")


def onCloseWindow(page, sockets):
    global win_opening, optionsFlag
    if not optionsFlag:
        win_opening = False
    optionsFlag = False
    pass


def add_to_startup_bat():
    folder_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r"C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup" % getpass.getuser()
    with open(bat_path + "\\" + "DeepLopenerOCR.bat", "w+") as bat_file:
        bat_file.write("cd "+folder_path+'\nstart "" ' +
                       folder_path+"\dist\DeepLopenerOCR\DeepLopenerOCR.exe")
    return folder_path


if __name__ == '__main__':
    now = time.time()
    config = configparser.ConfigParser()
    section = "DeepLopenerOCR"
    beforekeycc = True
    optionsFlag = False
    firstFlag = True
    ocrFlag = False
    beforetxt = ""
    win_opening = False
    # 自動起動.bat存在確認
    if not os.path.exists(r"C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\DeepLopenerOCR.bat" % getpass.getuser()) and os.path.exists("dist\DeepLopenerOCR\DeepLopenerOCR.exe"):
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
        freeFlag = config.get(section, "freeFlag")
        ocrFlag = config.get(section, "ocrFlag")

    except:
        target_lang = "JA"
        api_key = ""
        command = "ctrl+C"
        freeFlag = "Free"
        ocrFlag = "False"
        config.add_section(section)
        config.set(section, "target_lang", target_lang)
        config.set(section, "api_key", api_key)
        config.set(section, "command", command)
        config.set(section, "freeFlag", freeFlag)
        config.set(section, "ocrFlag", ocrFlag)
        with open("config.ini", "w")as f:
            config.write(f)

    keyboard.add_hotkey('ctrl+C', send_clipboard,
                        args=[target_lang, api_key])
    eel.init("assets")
    spawn = eel.spawn(capture)
    if(ocrFlag == "False"):
        spawn.kill()
    print("start")
    win_opening = True
    eel.start("main.html", close_callback=onCloseWindow)
