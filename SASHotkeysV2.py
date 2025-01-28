import pyautogui
import time
import keyboard

def on_hotkey():
    IcebarDropDownArrow = pyautogui.locateOnScreen("Icebardropdownarrow.png") # Can do directories as well btw
    if IcebarDropDownArrow is not None:
        x, y = pyautogui.center(IcebarDropDownArrow) # Get the center of the button
        pyautogui.click(x, y) # Click the button
    else:
        print("Button not found on the screen.")

keyboard.add_hotkey("ctrl+shift+a", on_hotkey)

print("Press CTRL+SHIFT+A to activate the hotkey.")
keyboard.wait()
