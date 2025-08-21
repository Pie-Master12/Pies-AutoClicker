import time
import os
import json
import pyautogui
from pynput import keyboard

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
            elif key.char == Self.Settings["ToggleClicker"] and not LockEnabled:  # Toggles AutoClicker
                MouseClicking = not MouseClicking
                print("Clicking:", MouseClicking)
            elif key.char == Self.Settings["Lock"]:  # Locking Function
                LockEnabled = not LockEnabled
                print("Lock Enabled:", LockEnabled)
            else:
                # print("Key pressed was not a valid keybind.")
                pass
        except:
            pass


MainUI = UIStart.StartUILoop()
AutoClickerInstance = AutoClicker(MainUI)

Listener = keyboard.Listener(on_press = AutoClickerInstance.on_press)
Listener.start()

def Click(ClickType, ClickStyle, PositionX, PositionY, PositionStyle):
    if ClickStyle == "Double":
        pyautogui.click(button=str(ClickType) if PositionStyle == "Current" else (PositionX, PositionY), )
        time.sleep(0.015)  # Small delay for double click
        pyautogui.click(button=str(ClickType))
    else:
        pyautogui.click(button=str(ClickType), x=PositionX if PositionStyle == "Custom" else None, y=PositionY if PositionStyle == "Custom" else None)


while AutoClickerInstance.RepeatAmount > 0 or AutoClickerInstance.RepeatMode == "Until Stopped":
    # Clicking and Keyboard cannot run at the same time, they will slow each other down causing undesired results.

    if AutoClickerInstance.RepeatMode == "Fixed":
        AutoClickerInstance.RepeatAmount -= 1
        if AutoClickerInstance.RepeatAmount <= 0:
            MouseClicking = False

    AutoClickerInstance.UpdateSettings(MainUI)

    if MouseClicking:
        Click(AutoClickerInstance.ClickType, AutoClickerInstance.ClickStyle, AutoClickerInstance.MousePositionX, AutoClickerInstance.MousePositionY, AutoClickerInstance.PositionStyle)
        time.sleep(AutoClickerInstance.ClickSpeed) # Changes the speed of the mouse clicking
    elif KeyboardSimulation:
        pass  # Placeholder for keyboard logic
