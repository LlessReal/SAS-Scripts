import OtherFunctions, time
import pyautogui as pya
from config import CurrentPath,HeadPhoneArea,SpeakerArea,StereoMixArea, MicArea

# https://teams.microsoft.com/ - Microsoft teams website
# Change the Input Device on Microsoft Teams Call
def MicrosoftTeamsChangeDevice(Action=""):
    # Open Call Window
    try: OtherFunctions.OpenWindow("(External)"); time.sleep(0.5) # Open the call window
    except: return
    # Click the dropdown
    try:
        MicrosoftDropDown = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\MicrosoftDropDown.png')
        pya.click(MicrosoftDropDown); time.sleep(0.5)
    except: print("Couldn't find Microsoft Dropdown :("); return
    if Action == "Speaking to Client":  ChangeInputandOutput(StereoMixArea,SpeakerArea); 
    elif Action == "Listening to Client": ChangeInputandOutput(MicArea,HeadPhoneArea); 

def ChangeInputandOutput(StereoMixArea,SpeakerArea):
    try:
        MicrosoftDropDown = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\MicrosoftDropDown.png')
        pya.click(MicrosoftDropDown); time.sleep(0.5)
    except: print("Couldn't find Microsoft Dropdown :("); return
    for i in range(3): pya.press("tab")
    time.sleep(1)
    for i in range(StereoMixArea - 1): pya.press("tab") # Tab onto the correct Incoming Audio Choice
    time.sleep(0.5); pya.press('enter') # Wait then press enter
    try:
        MicrosoftDropDown = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\MicrosoftDropDown.png')
        pya.click(MicrosoftDropDown); time.sleep(0.5)
    except: print("Couldn't find Microsoft Dropdown :("); return

    # Now change to speaker
    try:
        MicrosoftDropDown = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\MicrosoftDropDown.png')
        pya.click(MicrosoftDropDown); time.sleep(0.5)
    except: print("Couldn't find Microsoft Dropdown :("); return
    for i in range(7): pya.press("tab")
    time.sleep(1)
    for i in range(SpeakerArea - 1): pya.press("tab") # Tab onto the correct Incoming Audio Choice
    time.sleep(0.5); pya.press('enter') # Wait then press enter
    try:
        MicrosoftDropDown = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\MicrosoftDropDown.png')
        pya.click(MicrosoftDropDown); time.sleep(0.5)
    except: print("Couldn't find Microsoft Dropdown :("); return

