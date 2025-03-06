import pyautogui as pya
from time import sleep
from config import CurrentPath, api_key
import GuiMaker, SoundFunctions, IceBarFunctions, BotMessaging

def StartFunction(TestingBot,StartingProgram):
    GuiMaker.makeTransferGui()
    if not StartingProgram:
        ###### PHASE 1 - Greeting
        if TestingBot: # If testing, will use regular mic, then go straight to general greeting
            print("Testing Mode On. Program starts in 5 seconds"); sleep(5)
            SoundFunctions.GeneralGreeting() # Good Morning/Afternoon and then the greeting
        else: # If not testing
            # Wait for person to call
            CallInactive = False # Apart of message showing functionality to not have wait message spammedCallInactive = False # Apart of message showing functionality to not have wait message spammed
            while True:
                try: 
                    # Tries to detect blue calling button that appears when someone calls
                    SomeoneCalling = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\SomeoneCalling.png') 
                    print("Someone is calling!")  # If we passed this stage
                    CallInactive = False # Reset CallInactive if it's True and we're past the other stae
                    pya.click(SomeoneCalling) # Clicks the button
                    break # Onto next stage
                except Exception as e:
                    if CallInactive == False: print("Waiting for Answer Button to be active....") # This is so it won't be spammed.
                    CallInactive = True # needed to not make above message spam
                    sleep(0.1)
            # Sub-Loop: Wait for release button to load (Signifies that the call has loaded)
            while True: 
                try: # Uses mute button to determine if call started
                    pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\MuteAvailable.png') # Checks to see if mute option is available 
                    print("Call has started !!")
                    SoundFunctions.GeneralGreeting(); break # Greets and break out
                except:
                    if CallInactive == False: print("Waiting for call to load..."); CallInactive = True # This is so it won't be spammed.
        
        GatherCallersInfo() # Grab Info From Caller

# Repeat
def GatherCallersInfo(SayRepeatVoiceLine=0,NeedMoreInfo=False):
    # Asks caller to repeat what they said if this is on
    if SayRepeatVoiceLine == 1: SoundFunctions.playVoiceLine("Repeat")
    CallersMessage = IceBarFunctions.getCallerMessage() 
    if NeedMoreInfo == False: DetailsExplained = f"A caller has said the following message: {CallersMessage}\nRespond to the caller's message"
    else: DetailsExplained = f"The caller has responded with the following message: {CallersMessage}\nRespond to the caller's message"
    BotMessaging.GenerateBotResponse(DetailsExplained)