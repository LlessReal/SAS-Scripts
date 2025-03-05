import OtherFunctions, time
import pyautogui as pya
from config import CurrentPath,HeadPhoneArea,SpeakerArea,StereoMixArea, MicArea,SpeakerOptions,MicOptions

# https://teams.microsoft.com/ - Microsoft teams website
# Change the Input Device on Microsoft Teams Call
def MicrosoftTeamsChangeDevice(Action=""):
    # Open Call Window
    try: OtherFunctions.OpenWindow("(External)"); time.sleep(0.5) # Open the call window
    except: return # Usually if this occurs, you're in testing mode
    # Click the dropdown
    try:
        MicrosoftDropDown = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\MicrosoftDropDown.png')
        pya.click(MicrosoftDropDown); time.sleep(0.5)
    except: print("Couldn't find Microsoft Dropdown :("); return
    if Action == "Speaking to Client":  ChangeInputandOutput(StereoMixArea,SpeakerArea); 
    elif Action == "Listening to Client": ChangeInputandOutput(MicArea,HeadPhoneArea); 

def ChangeInputandOutput(Input,Output):
    OtherFunctions.OpenWindow("Settings")
    for i in range(2): pya.press("tab") 
    # Change Speaker
    pya.press("enter")
    for i in range(SpeakerOptions): pya.press("up") # Attempt to go to the stop
    for i in range(Output - 1): pya.press("down")
    pya.press("enter"); pya.press("tab")
    # Change Mic
    pya.press("enter")
    for i in range(MicOptions): pya.press("up") # Attempt to go to the stop
    for i in range(Input - 1): pya.press("down")
    pya.press("enter")
    # Return
    for i in range(2): pya.hotkey("shift","tab")