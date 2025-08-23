import tkinter as TKinter
from tkinter import ttk as TTK
import webbrowser

import time
import sys
import json
import os

class AutoClickerUI():
    def __init__(Self):
        Self.Root = TKinter.Tk()
        Self.Root.title("Pie's AutoClicker")
        Self.ScreenWidth = Self.Root.winfo_screenwidth()
        Self.ScreenHeight = Self.Root.winfo_screenheight()
        Self.Root.resizable(False, False)
        Self.Root.geometry(f"550x450+{(Self.ScreenWidth // 2) - (550 // 2)}+{(Self.ScreenHeight // 2) - (450 // 2)}")  # Centers the window on the screen

        Self.Ended = False

        MenuBar = TKinter.Menu(Self.Root)

        SettingsMenu = TKinter.Menu(MenuBar, tearoff=0)
        SettingsMenu.add_command(label="General", command=lambda: None)
        SettingsMenu.add_command(label="Keybinds", command=lambda: Self.CreateKeybindUI())
        SettingsMenu.add_command(label="Theme", command=lambda: Self.CreateUISettingsUI())
        MenuBar.add_cascade(label="Settings", menu=SettingsMenu)

        AboutMenu = TKinter.Menu(MenuBar, tearoff=0)
        AboutMenu.add_command(label="Discord", command=lambda: webbrowser.open("https://discord.gg/pNPJFkqWBW"))
        AboutMenu.add_command(label="GitHub", command=lambda: webbrowser.open("https://github.com/Pie-Master12/Pies-AutoClicker"))
        AboutMenu.add_command(label="WebPage", command=lambda: webbrowser.open_new_tab("src\WebPages\About.html")) # Opens the about us webpage
        MenuBar.add_cascade(label="About", menu=AboutMenu)

        MenuBar.add_cascade(label="Help", command=lambda: webbrowser.open_new_tab("src\WebPages\Documentation.html")) # Opens Documentation

        Self.Root.config(menu=MenuBar)


        # Gets the position/position type
        Self.MousePositionX, Self.MousePositionY, Self.PositionStyle = TKinter.StringVar(value="0"), TKinter.StringVar(value="0"), TKinter.StringVar(value="Current")
        # Gets the click type (eg. left, right, middle), click style (eg. single, double), and speed in seconds
        Self.ClickType, Self.ClickStyle = TKinter.StringVar(value="Left"), TKinter.StringVar(value="Single")
        # Gets the Values for ClickSpeed
        Self.Hours, Self.Minutes, Self.Seconds, Self.Milliseconds = TKinter.StringVar(value="0"), TKinter.StringVar(value="0"), TKinter.StringVar(value="0"), TKinter.StringVar(value="100")
        # Gets the Repeat mode, Gets the repeat amount
        Self.RepeatMode, Self.RepeatAmount = TKinter.StringVar(value="Until Stopped"), TKinter.StringVar(value="1")
        # UI Theme, saves
        Self.UITheme = TKinter.StringVar(value="Default")
        Self.UIColors = {}

        # Frames
        Self.CurrentFrame = "FrameOne"  # Keeps track of the current frame
        Self.FrameOne = Self.Root

        
        Self.CreateMainUI()

        Self.Root.protocol("WM_DELETE_WINDOW", Self.Quit)  # Ensures the window closes properly

        # Starts the main loop
        Self.UpdateUI()

    def UpdateUI(Self):
        Self.Root.update_idletasks()
        Self.Root.update()

    def Quit(Self):
        print("Frame: " + Self.CurrentFrame)

        if Self.CurrentFrame == "FrameOne":
            Self.Root.destroy()
            Self.Root.quit()
            Self.Ended = True
        else:
            Self.FrameOne.pack_forget()
            Self.CreateMainUI()


    def GetMenuInputs(Self):
        def CheckValue(Value, Default):
            try:
                return int(Value) if Value else Default
            except ValueError:
                return Default

        Inputs = {
            "MousePositionX": CheckValue(Self.MousePositionX.get(), 1),
            "MousePositionY": CheckValue(Self.MousePositionY.get(), 1),
            "PositionStyle": str(Self.PositionStyle.get()),
            "ClickType": str(Self.ClickType.get()),
            "ClickStyle": str(Self.ClickStyle.get()),
            "ClickSpeed": (CheckValue(Self.Hours.get(), 0) * 3600) + (CheckValue(Self.Minutes.get(), 0) * 60) + CheckValue(Self.Seconds.get(), 0) + (CheckValue(Self.Milliseconds.get(), 1) / 1000),
            "RepeatMode": str(Self.RepeatMode.get()),
            "RepeatAmount": CheckValue(Self.RepeatAmount.get(), 1)
        }

        return Inputs

    def CreateMainUI(Self):
        Self.Root.geometry("550x450")

        if Self.CurrentFrame != "FrameOne":
            Self.FrameOne.pack_forget()
            Self.CurrentFrame = "FrameOne"

        # Main UI Frame
        MainFrame = TKinter.Frame(Self.Root)
        MainFrame.pack(fill="both", expand=True)

        Self.FrameOne = MainFrame


        # Click Speed Section
        CSSection = TKinter.LabelFrame(MainFrame, text="Click Interval")
        CSSection.pack(pady=5, fill="x", padx=10)

        CSGrid = TKinter.Frame(CSSection)
        CSGrid.pack(pady=10, fill="x")

        TKinter.Label(CSGrid, text="Hours:").grid(row=0, column=0, sticky="w", padx=2, pady=2)
        ClickSpeedEntryHours = TKinter.Entry(CSGrid, textvariable=Self.Hours, width=6)
        ClickSpeedEntryHours.grid(row=0, column=1, padx=1, pady=2)

        TKinter.Label(CSGrid, text="Minutes:").grid(row=0, column=2, sticky="w", padx=2, pady=2)
        ClickSpeedEntryMinutes = TKinter.Entry(CSGrid, textvariable=Self.Minutes, width=6)
        ClickSpeedEntryMinutes.grid(row=0, column=3, padx=1, pady=2)

        TKinter.Label(CSGrid, text="Seconds:").grid(row=0, column=4, sticky="w", padx=2, pady=2)
        ClickSpeedEntrySeconds = TKinter.Entry(CSGrid, textvariable=Self.Seconds, width=6)
        ClickSpeedEntrySeconds.grid(row=0, column=5, padx=1, pady=2)

        TKinter.Label(CSGrid, text="Miliseconds:").grid(row=0, column=6, sticky="w", padx=2, pady=2)
        ClickSpeedEntryMiliSec = TKinter.Entry(CSGrid, textvariable=Self.Milliseconds, width=6)
        ClickSpeedEntryMiliSec.grid(row=0, column=7, padx=1, pady=2)


        # Container for the side-by-side sections
        TopFrame = TKinter.Frame(MainFrame)
        TopFrame.pack(pady=5, fill="x")

        # Click Options Section
        COSection = TKinter.LabelFrame(TopFrame, text="Click options")
        COSection.grid(row=0, column=2, padx=12, sticky="w")

        TKinter.Label(COSection, text="Click Type:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ClickTypeDropdown = TTK.OptionMenu(COSection, Self.ClickType, Self.ClickType.get(), "Left", "Right", "Middle")
        ClickTypeDropdown.grid(row=0, column=1, padx=5, pady=5)

        TKinter.Label(COSection, text="Click Style:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ClickStyleDropdown = TTK.OptionMenu(COSection, Self.ClickStyle, Self.ClickStyle.get(), "Single", "Double")
        ClickStyleDropdown.grid(row=1, column=1, padx=5, pady=5)    

        # Click Position Section
        CPSection = TKinter.LabelFrame(TopFrame, text="Click Position")
        CPSection.grid(row=0, column=6, padx=35, sticky="e")

        TKinter.Radiobutton(CPSection, text="Current location", variable=Self.PositionStyle, value="Current").grid(row=0, column=0, columnspan=3, sticky="w", padx=5, pady=5)
        TKinter.Radiobutton(CPSection, text="Fixed", variable=Self.PositionStyle, value="Custom").grid(row=1, column=0, sticky="w", padx=5, pady=5)

        TKinter.Label(CPSection, text="X:").grid(row=1, column=1)
        XEntry = TKinter.Entry(CPSection, textvariable=Self.MousePositionX, width=5)
        XEntry.grid(row=1, column=2)

        TKinter.Label(CPSection, text="Y:").grid(row=1, column=3)
        YEntry = TKinter.Entry(CPSection, textvariable=Self.MousePositionY, width=5)
        YEntry.grid(row=1, column=4)


        # Repeat Options Section
        ROSection = TKinter.LabelFrame(MainFrame, text="Repeat Options")
        ROSection.pack(pady=5, fill="x", padx=10)

        TKinter.Radiobutton(ROSection, text="Repeat", variable=Self.RepeatMode, value="Fixed").grid(row=0, column=0, sticky="w", padx=5, pady=5)

        RepeatEntry = TKinter.Entry(ROSection, textvariable=Self.RepeatAmount, width=6)
        RepeatEntry.grid(row=0, column=1, padx=5, pady=5)
        TKinter.Label(ROSection, text="times").grid(row=0, column=2)
        TKinter.Radiobutton(ROSection, text="Repeat until stopped", variable=Self.RepeatMode, value="Until Stopped").grid(row=1, column=0, sticky="w", padx=5, pady=5)

        # Bottom Buttons Section
        BottomButtonSection = TKinter.Frame(MainFrame)
        BottomButtonSection.pack(pady=20, fill="x")

        # Record/Playback Button
        RecordButton = TKinter.Button(BottomButtonSection, text="Record/Playback", command=lambda: Self.CreateRecordUI())
        RecordButton.grid(row=0, column=10, padx=10, pady=10)



    def CreateRecordUI(Self):
        Self.Root.geometry("650x800")
        Self.FrameOne.pack_forget()

        # Main UI Frame
        MainFrame = TKinter.Frame(Self.Root)
        MainFrame.pack(fill="both", expand=True)
        Self.CurrentFrame = "FrameTwo"
        Self.FrameOne = MainFrame

        Changed = True
        Saved = False

        
        def Save_Menu(Number, Name, Description):
            def SaveToFile(Number):
                Changed = False
                Saved = True
                with open(f"Save{Number}.json", "w") as SavedFile:
                    with open("TempKeyList.json", "r") as TempFile:
                        json.dump(json.load(TempFile), SavedFile)

        def Load_Menu():
            def LoadFromFile(Number):
                Changed = False
                Saved = True
                with open(f"Save{Number}.json", "r") as SavedFile:
                    KeyList = json.load(SavedFile)
                with open("TempKeyList.json", "w") as TempFile:
                    json.dump(KeyList, TempFile)

                

        def AddToList(ActionType, Button, PositionX, PositionY):
            Changed = True
            Saved = False

        def RemoveFromList(ListItem):
            Changed = True
            Saved = False

        def ClearList():
            if Changed and not Saved:
                PromptInput = Self.CreateMessagePrompt("Unsaved Changes", "You have unsaved changes. Would you like to continue clearing the list? Doing so without saving may result in a loss of data.")
                if PromptInput == False:
                    pass
                else:
                    with open("TempKeyList.json", "w") as TempFile:
                        json.dump({}, TempFile)
            else:
                with open("TempKeyList.json", "w") as TempFile:
                    json.dump({}, TempFile)

        def ChangeListItem():
            Changed = True
            Saved = False


        # Top Frame, Methods to start/stop the recording and playback
        TopFrame = TKinter.Frame(MainFrame, height=150, bg="Gray")
        TopFrame.pack(fill="x")

        RecordButton = TKinter.Button(TopFrame, text="Record", width=12, height=1, command=lambda: None)
        RecordButton.pack(pady=20, side="left", padx=5)

        PlaybackButton = TKinter.Button(TopFrame, text="Playback", width=12, height=1, command=lambda: None)
        PlaybackButton.pack(pady=20, side="left", padx=5)

        # Save and Load macro files to return to later
        SaveButton = TKinter.Button(TopFrame, text="Save", width=12, height=1, command=lambda: Save_Menu())
        SaveButton.pack(pady=20, side="left", padx=5)

        LoadButton = TKinter.Button(TopFrame, text="Load", width=12, height=1, command=lambda: ClearList())
        LoadButton.pack(pady=20, side="left", padx=5)

        # Right Frame, Contains methods to change/add/remove items from the list
        RightFrame = TKinter.Frame(MainFrame, width=250, bg="gray")
        RightFrame.pack(side="right", fill="y")


        # List Frame, Where all the recorded key/mouse actions are listed
        ListFrame = TKinter.Frame(MainFrame, bg="Black")
        ListFrame.pack(fill="both", expand=True)



    def CreateKeybindUI(Self):
        Self.Root.geometry("550x450")
        Self.FrameOne.pack_forget()

        # Main UI Frame
        MainFrame = TKinter.Frame(Self.Root)
        MainFrame.pack(fill="both", expand=True)
        Self.CurrentFrame = "FrameThree"
        Self.FrameOne = MainFrame


    def CreateMessagePrompt(Self, callback, Title, Message):
        OptionSelected = False

        MessageBox = TKinter.Toplevel(Self.Root)
        MessageBox.title(Title)
        MessageBox.resizable(False, False)
        MessageBox.grab_set()  # Makes the message box modal
        MessageBox.transient(Self.Root)  # Makes sure the message box is always on top of the main window
        MessageBox.focus_set()  # Focuses the message box
        MessageBox.lift()  # Brings the message box to the front
        MessageBox.attributes("-topmost", True)  # Ensures the message box stays on top
        MessageBox.update_idletasks()  # Updates the message box to ensure it is on
        MessageBox.anchor = "center"
        MessageBox.geometry(f"350x175+{(Self.ScreenWidth // 2) - (350 // 2)}+{(Self.ScreenHeight // 2) - (175 // 2)}")  # Centers the message box on the screen

        MessageLabel = TKinter.Label(MessageBox, text=Message, wraplength=250)
        MessageLabel.pack(pady=20)

        CancelButton = TKinter.Button(MessageBox, text="Cancel", command=lambda: callback(False), width=10)
        CancelButton.pack(pady=10, fill="y")

        ContinueButton = TKinter.Button(MessageBox, text="Continue", command=lambda: callback(True), width=10)
        ContinueButton.pack(pady=10, fill="y")

        MessageBox.transient(Self.Root)


    def CreateUISettingsUI(Self):
        Self.Root.geometry("550x450")
        Self.FrameOne.pack_forget()

        # Main UI Frame
        MainFrame = TKinter.Frame(Self.Root)
        MainFrame.pack(fill="both", expand=True)
        Self.CurrentFrame = "FrameFour"
        Self.FrameOne = MainFrame

        # Scrollable Frame with scrollbar and mousewheel
        Canvas = TKinter.Canvas(MainFrame, height=300)
        Scrollbar = TKinter.Scrollbar(MainFrame, orient="vertical", command=Canvas.yview)
        Scrollable_frame = TKinter.Frame(Canvas)

        Scrollable_frame.bind(
            "<Configure>",
            lambda e: Canvas.configure(
                scrollregion=Canvas.bbox("all")
            )
        )

        Canvas.create_window((0, 0), window=Scrollable_frame, anchor="nw")
        Canvas.configure(yscrollcommand=Scrollbar.set)

        Canvas.pack(side="left", fill="both", expand=True)
        Scrollbar.pack(side="right", fill="y")

        # Add labels to scrollable frame



        # Bind mousewheel scrolling
        Self.bind_mousewheel(Canvas)

    def bind_mousewheel(self, widget):
        # Windows and Linux
        widget.bind_all("<MouseWheel>", lambda e: widget.yview_scroll(int(-1*(e.delta/120)), "units"))
        # For Linux with shift key pressed (horizontal scrolling)
        widget.bind_all("<Shift-MouseWheel>", lambda e: widget.xview_scroll(int(-1*(e.delta/120)), "units"))
        # macOS uses different event.delta values
        widget.bind_all("<Button-4>", lambda e: widget.yview_scroll(-1, "units"))
        widget.bind_all("<Button-5>", lambda e: widget.yview_scroll(1, "units"))



def StartUILoop():
    MainUI = AutoClickerUI()
    return MainUI

# Below this line is the testing zone for the UI
# AutoClickerUI()