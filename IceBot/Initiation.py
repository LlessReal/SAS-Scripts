import pyautogui as pya
import ollama, pyttsx3
from time import sleep

import IceBarFunctions
from OtherFunctions import OpenWindow
from config import CurrentPath, ModelName
import GuiMaker 
import SoundFunctions
engine = pyttsx3.init() # Initialize the engine
#Adjust speaking rate
rate = engine.getProperty('rate')
engine.setProperty('rate', 150) # Slowwww

#Adjust volume
engine.setProperty('volume', 1.0)

#Change voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Selecting a female voice


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
            SoundFunctions.GeneralGreeting() # Good Morning/Afternoon and then the greeting
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
                    CallStartedImages = [fr'{CurrentPath}\..\IceBarImages\MuteAvailable.png',fr'{CurrentPath}\..\IceBarImages\PersonIcon.png']
                    NoCallStarted = True
                    for CallStartedImage in CallStartedImages:
                        try:
                            MuteAvailable = pya.locateOnScreen(CallStartedImage) # Checks to see if mute option is available
                            NoCallStarted = False
                            break
                        except:
                            continue
                    if NoCallStarted:
                        continue
                    print("Call has started !!")
                    SoundFunctions.GeneralGreeting() # After it loads, Good Morning/Afternoon and then the greeting
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
    CallersWords = IceBarFunctions.getCallerMessage() 
    DetailsExplained = f"""An unknown caller has sent this message towards you: {CallersWords}
Respond to the caller's message, and if you're going to transfer them to a number, say, '[INITIATE TRANSFER - (The Number )]' AT THE VERY END of your response, and replace (The Number) with the actual number you're transfering them to of course."""
    DetailsLocation = fr"{CurrentPath}\Details.txt"
    with open(DetailsLocation,"r+", encoding='utf-8', errors='ignore') as f:
        DetailsandMessage = f"{DetailsExplained}\n{f.read()}" 

    SoundFunctions.playVoiceLine("PleaseWait")
    # Generate bot's response
    try:
        response = ollama.chat(model=ModelName, messages=[{'role': 'user', 'content': DetailsandMessage}])
        BotsResponse = response['message']['content'] # Use this for whatever
    except Exception as e:
        print(f"Error running Ollama: {e}")
        return
    
    print(f"Bot's Response: {BotsResponse}")
    engine.say(BotsResponse) # Says the bot's response
    engine.runAndWait()
    engine.stop() # Stop the engine
    # FINAL PHASE: Transfering
    if CallersWords != "Left the Call":
        GuiMaker.makeTransferGui(TheCallersWords=CallersWords,BotsResponse=BotsResponse) 

# Repeat
def RepeatPlease(StartingProgram=False,SayMessage=0):
    if StartingProgram:
        print("Program hasn't started yet")
        return # Do nothing
    if SayMessage == 1: SoundFunctions.playVoiceLine("Repeat")
    GetCallersMessage()

# Change the Input Device on Microsoft Teams Call
def MTeamsChangeInputDevice(Input):
    # Open the call window
    try:
        OpenWindow("(External)")
    except:
        return
    sleep(0.5)
    # Click the dropdown
    try:
        MicrosoftDropDown = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\MicrosoftDropDown.png')
        pya.click(MicrosoftDropDown)
    except:
        print("Couldn't find Microsoft Dropdown :(")
        return
    sleep(0.5)
    # Click Headset, or Speakers, or Stereo Yk Yk
    try:
        if Input == "Headset":
            DeviceToTurnOn = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\HDAudio.png')
        elif Input == "Speakers":
            DeviceToTurnOn = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\Speakers.png')
        elif Input == "StereoMix":
            DeviceToTurnOn = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\StereoMix.png')
        pya.click(DeviceToTurnOn)
    except:
        print("Couldn't find headset or speakers : (")
        return