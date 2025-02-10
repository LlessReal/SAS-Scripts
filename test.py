import pygetwindow as gw
import time
import pyautogui as pya
import keyboard
import pyperclip as pc
import os

time.sleep(2)
reqid = "0000538390"
CurrentPath = os.path.dirname(__file__) # Gonna need this
pya.hotkey('ctrl', 'f') # Find
keyboard.write(reqid + "\n") # Puts in Req ID and paste it (with enter)
time.sleep(1) # Wait for box to load
try:
    NoMatches = pya.locateOnScreen(f'{CurrentPath}\\NoMatches.png') # Tries to look for the No Matches box
    print(f"No SR for {reqid}")
    time.sleep(0.5)
    keyboard.write("\n") # Enters
except:
    print("SR Found") # If no box was found, SR is there