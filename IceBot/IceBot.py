import pyautogui as pya
import os, pygame
from time import sleep
import sounddevice as sd 
import datetime

import OtherFunctions
from SoundFunctions import playVoiceLine
from config import ViewAllDeviceNames, RegularInputDeviceName, StereoInputDeviceName, TestingBot, CurrentPath 
import GuiMaker 
pygame.mixer.init() # Initialization

def main():
    # Check all devices and dip
    if ViewAllDeviceNames == True:
        print(sd.query_devices() + "\n Performed Input Device Listing")
        return
    # Main loop
    while True:
        ###### PHASE 1 - Answer Za Call
        CallInactive = False # Apart of message showing functionality to not have wait message spammed
        if TestingBot == True:
            os.system(fr'powershell -Command "& {{(Get-AudioDevice -List | Where-Object {{ $_.Name -like \"{RegularInputDeviceName}\" }}) | Set-AudioDevice }}"')
            CurrentDateandTime = datetime.datetime.now()
            playVoiceLine("GoodMorning" if CurrentDateandTime.strftime("%p") == "AM" else "GoodAfternoon")
            playVoiceLine("Greeting")
        else:
            while True:
                try: 
                    # If we found that Answer is available and can be pressed
                    SomeoneCalling = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\SomeoneCalling.png') # If error, it couldn't find it :(
                    print("Someone is calling!") # Let us know
                    pya.click(SomeoneCalling) # Clicks it
                    os.system(fr'powershell -Command "& {{(Get-AudioDevice -List | Where-Object {{ $_.Name -like \"{StereoInputDeviceName}\" }}) | Set-AudioDevice }}"') 
                    # Swap to stereo (May take a while) for bot to listen to caller
                    CallInactive = False # Reset CallInactive if it's True
                    while True: # Wait for thing to load (waits for Release Button to be available)
                        try:
                            ReleaseAvailable = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\ReleaseAvailable.png') # If error, it couldn't find it :(
                            break
                        except:
                            if CallInactive == False: # This is so it won't be spammed.
                                print(e)
                                print("Waiting for call to load...")
                            CallInactive = True # needed to not make above message spam
                            sleep(0.25)
                    CallInactive = False
                    CurrentDateandTime = datetime.datetime.now()
                    playVoiceLine("GoodMorning" if CurrentDateandTime.strftime("%p") == "AM" else "GoodAfternoon")
                    playVoiceLine("Greeting")
                    break # Break out to next stage
                except Exception as e:
                    if CallInactive == False: # This is so it won't be spammed.
                        print(e)
                        print("Waiting for Answer Button to be active....")
                    CallInactive = True # needed to not make above message spam
                    sleep(0.25)

        ##### PHASE 2 - Muting Myself to Hear Caller
        if TestingBot == False:
            MuteAvailable = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\MuteAvailable.png') # Checks to see if mute option is available
            print("Found Mute Button!")
            pya.click(MuteAvailable) # Clicks mute button

        ##### FINAL PHASE (PART 1) - Grab Info From Caller
        Status = ""
        while True:
            CallersWords = OtherFunctions.getCallerMessage(Status)    
            playVoiceLine("PleaseWait")

            ##### FINAL PHASE (PART 2) - TRANSFER GUI
            Status = GuiMaker.makeTransferGui(CallersWords) 
            if Status == "Repeat":
                continue
            else:
                break
            
        # End (Change audio input back to microphone)
        os.system(fr'powershell -Command "& {{(Get-AudioDevice -List | Where-Object {{ $_.Name -like \"{RegularInputDeviceName}\" }}) | Set-AudioDevice }}"')
        print("The deed is done")
        if TestingBot == True:
            print("Rerunning in 5 seconds")
            sleep(5)
        # Loop happens here

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("The program broke L", e)
        # Set input device back to regular mic
        os.system(fr'powershell -Command "& {{(Get-AudioDevice -List | Where-Object {{ $_.Name -like \"{RegularInputDeviceName}\" }}) | Set-AudioDevice }}"')