import pyautogui as pya
import os, pygame
from time import sleep

import OtherFunctions
from SoundFunctions import playVoiceLine, GeneralGreeting
from config import CurrentPath
import GuiMaker 

pygame.mixer.init() # Initialization

def StartFunction(TestingBot,StartingProgram):
    GuiMaker.makeTransferGui()
    if not StartingProgram:
        ###### PHASE 1 - Greeting
        if TestingBot: # If testing, will use regular mic, then go straight to general greeting
            print("Testing Mode On. Program starts in 5 seconds")
            sleep(5)
            ResetState = GuiMaker.BackToStageOne()
            if ResetState == "ResetGuiNow":
                return
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
                    OtherFunctions.ChangeToStereoMix() # Swap to stereo (May take a while) for bot to listen to caller
                    break # Onto next stage
                except Exception as e:
                    if CallInactive == False: # This is so it won't be spammed.
                        print("Waiting for Answer Button to be active....")
                    CallInactive = True # needed to not make above message spam
                    sleep(0.1)
                    ResetState = GuiMaker.BackToStageOne()
                    if ResetState == "ResetGuiNow":
                        return
            # Sub-Loop: Wait for release button to load (Signifies that the call has loaded)
            while True: 
                try:
                    
                    MuteAvailable = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\MuteAvailable.png') # Checks to see if mute option is available
                    print("Found Mute Button! Call has started")
                    GeneralGreeting() # After it loads, Good Morning/Afternoon and then the greeting
                    pya.click(MuteAvailable) # Mute myself to hear caller
                    break # Break out subloop
                except:
                    if CallInactive == False: # This is so it won't be spammed.
                        print("Waiting for call to load...")
                    CallInactive = True # needed to not make above message spam
                    sleep(0.1)
                    ResetState = GuiMaker.BackToStageOne()
                    if ResetState == "ResetGuiNow":
                        return
        
        ##### PHASE 2 - Grab Info From Caller
        GetCallersMessage()

def GetCallersMessage():
    CallersWords = OtherFunctions.getCallerMessage()  
    try:
        UnMuteAvailable = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\UnMuteAvailable.png') # Checks to see if mute option is available
        pya.click(UnMuteAvailable) # Mute myself to hear caller  
    except:
        pass
    playVoiceLine("PleaseWait")
    # FINAL PHASE: Transfering
    if CallersWords != "Left the Call":
        GuiMaker.makeTransferGui(TheCallersWords=CallersWords) 
        sleep(50)

# Repeat
def RepeatPlease(StartingProgram=False):
    if StartingProgram:
        print("Program hasn't started yet")
        return # Do nothing
    playVoiceLine("Repeat")
    GetCallersMessage()