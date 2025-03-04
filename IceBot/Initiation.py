import pyautogui as pya
from time import sleep

import IceBarFunctions
from OtherFunctions import OpenWindow
from config import CurrentPath, ModelName
import GuiMaker, SoundFunctions, ollama, pyttsx3
engine = pyttsx3.init() # Initialize the engine
#Adjust speaking rate
rate = engine.getProperty('rate')
engine.setProperty('rate', 150) # Slowwww

#Adjust volume
engine.setProperty('volume', 1.0)

#Change voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Selecting a female voice

from huggingface_hub import InferenceClient

client = InferenceClient(
	provider="novita",
	#api_key=""
)

def StartFunction(TestingBot,StartingProgram):
    GuiMaker.makeTransferGui()
    if not StartingProgram:
        ###### PHASE 1 - Greeting
        if TestingBot: # If testing, will use regular mic, then go straight to general greeting
            print("Testing Mode On. Program starts in 5 seconds")
            sleep(5)
            ResetState = GuiMaker.BackToStageOne()
            if ResetState == "ResetGuiNow": return
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
                    if CallInactive == False:  print("Waiting for Answer Button to be active....") # This is so it won't be spammed.
                    CallInactive = True # needed to not make above message spam
                    sleep(0.1)
                    ResetState = GuiMaker.BackToStageOne()
                    if ResetState == "ResetGuiNow": return
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
                        except: continue
                    if NoCallStarted: continue
                    print("Call has started !!")
                    SoundFunctions.GeneralGreeting() # After it loads, Good Morning/Afternoon and then the greeting
                    break # Break out subloop
                except:
                    if CallInactive == False: print("Waiting for call to load...") # This is so it won't be spammed.
                    CallInactive = True # needed to not make above message spam
                    sleep(0.1)
                    ResetState = GuiMaker.BackToStageOne()
                    if ResetState == "ResetGuiNow": return
        
        ##### PHASE 2 - Grab Info From Caller
        GetCallersMessage()


### Message Context
PhoneNumDetails = open(fr"{CurrentPath}\Details.txt","r", encoding='utf-8', errors='ignore').read()
SystemMessage = f"""You are a bot at Columbus State University meant to transfer people to the right number depending on what they ask for
You'll be transfering them from the numbers below. 
if you're going to transfer them to a number, say, '[INITIATE TRANSFER - (The Number)]' AT THE VERY END of your response, and replace (The Number) with the actual number you're transfering them to of course.
{PhoneNumDetails}"""
def GetCallersMessage():
    CallersWords = IceBarFunctions.getCallerMessage() 
    DetailsExplained = f"A caller has said the following message: {CallersWords}\nRespond to the caller's message"
    SoundFunctions.playVoiceLine("PleaseWait")
    # Generate bot's response
    try:
        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct", 
            messages=[
                {'role': 'system', 'content': SystemMessage},
                {'role': 'user', 'content': "A caller has said the following message: Can you give me admissions?\nRespond to the caller's message"},
                {'role': 'assistant', 'content': "Alright, you will be transferred to admissions shortly. [INITIATE TRANSFER - 6001]"},
                {'role': 'user', 'content': "A caller has said the following message: Hey, I was wondering where I would go for orientation?\nRespond to the caller's message"},
                {'role': 'assistant', 'content': "I can have the orientation department help you with that. Please hold while I transfer you. [INITIATE TRANSFER - 7065078593]"},
                {'role': 'user', 'content': DetailsExplained},
                ], 
            max_tokens=500,
        )
        BotsResponse = completion.choices[0].message.content 
    except Exception as e:
        print(f"Error running Ollama: {e}")
        return
    
    print(f"Bot's Response: {BotsResponse}")
    engine.say(BotsResponse) # Says the bot's response
    engine.runAndWait()
    engine.stop() # Stop the engine
    # FINAL PHASE: Transfering
    if CallersWords != "Left the Call": GuiMaker.makeTransferGui(TheCallersWords=CallersWords,BotsResponse=BotsResponse) 

# Repeat
def RepeatPlease(StartingProgram=False,SayMessage=0):
    if StartingProgram:
        print("Program hasn't started yet")
        return # Do nothing
    if SayMessage == 1: SoundFunctions.playVoiceLine("Repeat")
    GetCallersMessage()

# Change the Input Device on Microsoft Teams Call
def MTeamsChangeInputDevice(Input):
    try: OpenWindow("(External)") # Open the call window
    except: return
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
        if Input == "Headset": DeviceToTurnOn = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\HDAudio.png')
        elif Input == "Speakers": DeviceToTurnOn = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\Speakers.png')
        elif Input == "StereoMix": DeviceToTurnOn = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\StereoMix.png')
        pya.click(DeviceToTurnOn)
    except:
        print("Couldn't find headset or speakers : (")
        return