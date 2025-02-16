import pyautogui as pya
import os, pygame
from time import sleep

import OtherFunctions
from SoundFunctions import playVoiceLine, GeneralGreeting
from config import ViewAllDeviceNames, RegularInputDeviceName, StereoInputDeviceName, TestingBot, TestingStereoInput, CurrentPath
import GuiMaker 
pygame.mixer.init() # Initialization

def StartFunction():
    while True:
        ###### PHASE 1 - Greeting
        if TestingBot == True: # If testing, will use regular mic, then go straight to general greeting
            print("Testing Mode On. Program starts in 5 seconds")
            sleep(5)
            if not TestingStereoInput:
                os.system(fr'powershell -Command "& {{(Get-AudioDevice -List | Where-Object {{ $_.Name -like \"{RegularInputDeviceName}\" }}) | Set-AudioDevice }}"')
            else:
                os.system(fr'powershell -Command "& {{(Get-AudioDevice -List | Where-Object {{ $_.Name -like \"{StereoInputDeviceName}\" }}) | Set-AudioDevice }}"')
            GeneralGreeting() # Good Morning/Afternoon and then the greeting
        else: # If not testing
            # Wait for person to call
            CallInactive = False # Apart of message showing functionality to not have wait message spammedCallInactive = False # Apart of message showing functionality to not have wait message spammed
            while True:
                try: 
                    # Tries to detect blue calling button that appears when someone calls
                    SomeoneCalling = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\SomeoneCalling.png') 
                    # If we passed this stage
                    print("Someone is calling!") 
                    CallInactive = False # Reset CallInactive if it's True and we're past the other stae
                    pya.click(SomeoneCalling) # Clicks the button
                    # Swap to stereo (May take a while) for bot to listen to caller
                    os.system(fr'powershell -Command "& {{(Get-AudioDevice -List | Where-Object {{ $_.Name -like \"{StereoInputDeviceName}\" }}) | Set-AudioDevice }}"') 
                    break # Onto next stage
                except Exception as e:
                    if CallInactive == False: # This is so it won't be spammed.
                        print("Waiting for Answer Button to be active....")
                    CallInactive = True # needed to not make above message spam
                    sleep(0.1)
            # Sub-Loop: Wait for release button to load (Signifies that the call has loaded)
            while True: 
                try:
                    ReleaseAvailable = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\ReleaseAvailable.png')
                    # Once it loads
                    GeneralGreeting() # Good Morning/Afternoon and then the greeting
                    # Mute myself to hear caller
                    MuteAvailable = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\MuteAvailable.png') # Checks to see if mute option is available
                    print("Found Mute Button!")
                    pya.click(MuteAvailable) # Clicks mute button
                    break # Break out subloop
                except:
                    if CallInactive == False: # This is so it won't be spammed.
                        print("Waiting for call to load...")
                    CallInactive = True # needed to not make above message spam
                    sleep(0.1)
        
        ##### PHASE 2 - Grab Info From Caller
        GetCallersMessage()

def GetCallersMessage():
    CallersWords = OtherFunctions.getCallerMessage()    
    playVoiceLine("PleaseWait")
    GuiMaker.makeTransferGui(CallersWords,True) 

def RepeatPlease():
    playVoiceLine("Repeat")
    GetCallersMessage()