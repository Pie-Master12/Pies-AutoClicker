import time
import os
import sys
import json
import pyautogui
from pynput import keyboard
from pynput.keyboard import Key, Controller

# File directories
import UI.UIStart as UIStart

# Random Variables
MouseClicking = False
KeyboardSimulation = False
SettingKeybind = False
LockEnabled = False # Used to prevent the functions from being toggled

# Main class for the autoclicker
class AutoClicker():
    def __init__(Self, UIInstance):
        Self.Settings = {}

        Self.load_settings()
        Self.save_settings()

        Self.UIInstance = UIInstance
        OtherStuff = UIInstance.GetMenuInputs()

        Self.ClickSpeed = OtherStuff["ClickSpeed"]
        Self.ClickType = OtherStuff["ClickType"]
        Self.ClickStyle = OtherStuff["ClickStyle"]
        Self.MousePositionX = OtherStuff["MousePositionX"]
        Self.MousePositionY = OtherStuff["MousePositionY"]
        Self.PositionStyle = OtherStuff["PositionStyle"]
        Self.RepeatMode = OtherStuff["RepeatMode"]
        Self.RepeatAmount = OtherStuff["RepeatAmount"]

    def UpdateSettings(Self, UIInstance):
        MainUI.UpdateUI()  # Update the UI to reflect changes

        OtherStuff = UIInstance.GetMenuInputs()
        Self.ClickSpeed = OtherStuff["ClickSpeed"]
        Self.ClickType = OtherStuff["ClickType"]
        Self.ClickStyle = OtherStuff["ClickStyle"]
        Self.MousePositionX = OtherStuff["MousePositionX"]
        Self.MousePositionY = OtherStuff["MousePositionY"]
        Self.PositionStyle = OtherStuff["PositionStyle"]
        Self.RepeatMode = OtherStuff["RepeatMode"]
        Self.RepeatAmount = OtherStuff["RepeatAmount"] 

    def load_settings(Self):
        if os.path.exists("Settings.json"):
            with open("Settings.json", 'r') as file:
                Self.Settings = json.load(file)
        else:
            Self.Settings = {"ToggleClicker": "p", "Lock": "l", "ToggleKey": "o"}

    def save_settings(Self):
        with open("Settings.json", 'w') as file:
            json.dump(Self.Settings, file)

    def on_press(Self, key):
        global MouseClicking
        global KeyboardSimulation
        global SettingKeybind
        global LockEnabled

        try:
            # print("Key pressed:", key.char if hasattr(key, 'char') else key.name)
            if SettingKeybind:
                Self.Settings["ToggleKey"] = key.char if hasattr(key, 'char') else key.name
                Self.save_settings()

            elif key.char == Self.Settings["ToggleClicker"] and not LockEnabled and not KeyboardSimulation:  # Toggles AutoClicker
                MouseClicking = not MouseClicking
                print("Clicking:", MouseClicking)

            elif key.char == Self.Settings["ToggleKey"] and not LockEnabled and not MouseClicking:  # Toggles Key Simulation
                KeyboardSimulation = not KeyboardSimulation
                print("Keyboard Simulation:", KeyboardSimulation)

            elif key.char == Self.Settings["Lock"]:  # Locking Function
                LockEnabled = not LockEnabled
                print("Lock Enabled:", LockEnabled)

            else:
                # print("Key pressed was not a valid keybind.")
                pass
        except:
            pass

    def Click(Self, ClickType, ClickStyle, PositionX, PositionY, PositionStyle):
        if ClickStyle == "Double":
            pyautogui.click(button=str(ClickType), x=PositionX if PositionStyle == "Custom" else None, y=PositionY if PositionStyle == "Custom" else None)
            time.sleep(0.015)  # Small delay for double click
            pyautogui.click(button=str(ClickType), x=PositionX if PositionStyle == "Custom" else None, y=PositionY if PositionStyle == "Custom" else None)
        else:
            pyautogui.click(button=str(ClickType), x=PositionX if PositionStyle == "Custom" else None, y=PositionY if PositionStyle == "Custom" else None)

    def Record(Self):
        Self.UIInstance.CreateRecordUI()

    def Playback(Self, KeyBoard):
        with open("TempKeyList.json", "r") as KeyList:
            KeyListData = json.load(KeyList)

        for Keys in KeyListData:
            KeyData = KeyListData[Keys]
            SpecialKeys = {
                "space": Key.space,
                "enter": Key.enter,
                "lshift": Key.shift_l,
                "rshift": Key.shift_r,
                "lctrl": Key.ctrl_l,
                "rctrl": Key.ctrl_r,
                "lalt": Key.alt_l,
                "ralt": Key.alt_r,
                "esc": Key.esc,
                "tab": Key.tab,
                "backspace": Key.backspace,
                "delete": Key.delete,
                "up": Key.up,
                "down": Key.down,
                "left": Key.left,
                "right": Key.right,
                "home": Key.home,
                "end": Key.end,
                "pageup": Key.page_up,
                "pagedown": Key.page_down,
                "f1": Key.f1,
                "f2": Key.f2,
                "f3": Key.f3,
                "f4": Key.f4,
                "f5": Key.f5,
                "f6": Key.f6,
                "f7": Key.f7,
                "f8": Key.f8,
                "f9": Key.f9,
                "f10": Key.f10,
                "f11": Key.f11,
                "f12": Key.f12,
                "f13": Key.f13,
                "f14": Key.f14,
                "f15": Key.f15,
                "f16": Key.f16,
                "f17": Key.f17,
                "f18": Key.f18,
                "f19": Key.f19,
                "f20": Key.f20,
                "f21": Key.f21,
                "f22": Key.f22,
                "f23": Key.f23,
                "f24": Key.f24,
                "capslock": Key.caps_lock,
                "numlock": Key.num_lock,
                "scrolllock": Key.scroll_lock,
                "printscreen": Key.print_screen,
                "pause": Key.pause,
                "insert": Key.insert,
                "win": Key.cmd,  # Windows key
                "apps": Key.menu,  # Context menu key
                "volumeup": Key.media_volume_up,
                "volumedown": Key.media_volume_down,
                "volumemute": Key.media_volume_mute,
                "playpause": Key.media_play_pause,
                "nexttrack": Key.media_next,
                "prevtrack": Key.media_previous,
                "stop": Key.media_stop,
            }

            if KeyData["Type"] != "MouseClick":
                KeyObject = SpecialKeys.get(KeyData["Object"], KeyData["Object"])

            if KeyData["Type"] == "KeyDown":
                try:
                    KeyBoard.press(KeyObject)
                except Exception as e:
                    print(f"Error pressing key \"{KeyData['Object']}\": {e}")
            elif KeyData["Type"] == "KeyUp":
                try:
                    KeyBoard.release(KeyObject)
                except Exception as e:
                    print(f"Error releasing key \"{KeyData['Object']}\": {e}")

            elif KeyData["Type"] == "Sleep":
                time.sleep(float(KeyData["Object"]))
            elif KeyData["Type"] == "MouseClick":
                MouseData = KeyData["Object"]
                MousePositionX = MouseData["X"]
                MousePositionY = MouseData["Y"]
                try:
                    pyautogui.click(button=KeyData["Object"]["Style"], x=MousePositionX, y=MousePositionY)
                except Exception as e:
                    print(f"Error clicking mouse: {e}")

            # Reference for each type: {"PartOne": {"Type": "KeyDown", "Object": "space"}, "PartTwo": {"Type": "KeyDown", "Object": "s"}, "PartThree": {"Type": "Sleep", "Object": "0.507"}, "PartFour": {"Type": "KeyUp", "Object": "space"}, "PartFive": {"Type": "KeyUp", "Object": "s"}, "PartSix": {"Type": "KeyDown", "Object": "w"}, "PartSeven": {"Type": "Sleep", "Object": "0.5"}, "PartEight": {"Type": "KeyUp", "Object": "w"}, "PartNine": {"Type": "MouseClick", "Object": {"Style": "Left", "X": 1000, "Y": 600}}}




MainUI = UIStart.StartUILoop()
AutoClickerInstance = AutoClicker(MainUI)

KeyBoard = Controller()

Listener = keyboard.Listener(on_press = AutoClickerInstance.on_press)
Listener.start()


while AutoClickerInstance.RepeatAmount > 0 or AutoClickerInstance.RepeatMode == "Until Stopped":
    # Clicking and Keyboard cannot run at the same time, they will slow each other down causing undesired results.

    if AutoClickerInstance.RepeatMode == "Fixed":
        AutoClickerInstance.RepeatAmount -= 1
        if AutoClickerInstance.RepeatAmount <= 0:
            MouseClicking = False
            KeyboardSimulation = False
    elif MainUI.Ended:
        MouseClicking = False
        KeyboardSimulation = False
        SystemExit(0)
        sys.exit(0)

    AutoClickerInstance.UpdateSettings(MainUI)

    if MouseClicking:
        AutoClickerInstance.Click(AutoClickerInstance.ClickType, AutoClickerInstance.ClickStyle, AutoClickerInstance.MousePositionX, AutoClickerInstance.MousePositionY, AutoClickerInstance.PositionStyle)
        time.sleep(AutoClickerInstance.ClickSpeed) # Changes the speed of the mouse clicking
    elif KeyboardSimulation:
        AutoClickerInstance.Playback(KeyBoard)
