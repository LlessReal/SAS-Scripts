import pyautogui as pya
import os
def screenshot():
    screenshot = pya.screenshot()
    screenshot.save("Testshot.png")
# Post Config
CurrentPath = os.path.dirname(__file__) # Gonna need this