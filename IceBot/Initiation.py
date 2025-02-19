import pyautogui as pya
import ollama, pyttsx3
from time import sleep

import OtherFunctions
from OtherFunctions import OpenWindow
from SoundFunctions import playVoiceLine, GeneralGreeting
from config import CurrentPath
import GuiMaker 
engine = pyttsx3.init() # Initialize the engine

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
                    GeneralGreeting() # After it loads, Good Morning/Afternoon and then the greeting
                    MTeamsChangeInputDevice("Headset")
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
        MTeamsChangeInputDevice("Speakers")
    except:
        pass
    playVoiceLine("PleaseWait")
    #model_name = "sblight"  # Replace with your desired Ollama model
    #TranscriptionText = fr"{CurrentPath}\Caller's Message\CallersMessageTranscription.txt"
    #EntireConversation = fr"{CurrentPath}\Caller's Message\WholeConvo.txt"
    #try:
    #    response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': CallersWords}])
    #    BotsResponse = response['message']['content'] # Use this for whatever
    #except Exception as e:
    #    print(f"Error running Ollama: {e}")
    #    return

    # Adjust speaking rate
    #rate = engine.getProperty('rate')
    #engine.setProperty('rate', 100) # Slowwww

    # Adjust volume
    #volume = engine.getProperty('volume')
    #engine.setProperty('volume', 1.0)

    # Change voice
    #voices = engine.getProperty('voices')
    #engine.setProperty('voice', voices[0].id)  # Selecting a female voice

    #engine.say(BotsResponse) # Says the bot's response
    #engine.runAndWait()

    #engine.stop() # Stop the engine
    # FINAL PHASE: Transfering
    if CallersWords != "Left the Call":
        GuiMaker.makeTransferGui(TheCallersWords=CallersWords) 
     

# Repeat
def RepeatPlease(StartingProgram=False):
    if StartingProgram:
        print("Program hasn't started yet")
        return # Do nothing
    playVoiceLine("Repeat")
    GetCallersMessage()

def MTeamsChangeInputDevice(Input):
    try:
        OpenWindow("(External)")
    except:
        print("Not in a call")
        return
    sleep(0.5)
    try:
        MicrosoftDropDown = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\MicrosoftDropDown.png')
        pya.click(MicrosoftDropDown)
    except:
        print("Couldn't find Microsoft Dropdown :(")
        return
    sleep(0.5)
    try:
        if Input == "Headset":
            HDAudio = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\HDAudio.png')
            pya.click(HDAudio)
        elif Input == "Speakers":
            Speakers = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\Speakers.png')
            pya.click(Speakers)
    except:
        print("Couldn't find headset or speakers : (")
        return