import pyautogui as pya
from time import sleep
from config import CurrentPath
import GuiMaker, SoundFunctions, IceBarFunctions, BotMessaging
import pygetwindow as gw
def StartFunction(TestingBot,StartingProgram):
    GuiMaker.makeTransferGui()
    if not StartingProgram:
        ###### PHASE 1 - Greeting
        while True: # May delete later
            if TestingBot: print("Testing Mode On. Program starts in 5 seconds"); sleep(5)
            else: # If not testing
                # Wait for person to call
                CallInactive = False # Apart of message showing functionality to not have wait message spammedCallInactive = False # Apart of message showing functionality to not have wait message spammed
                while True:
                    try: 
                        # Tries to detect blue calling button that appears when someone calls
                        SomeoneCalling = pya.locateOnScreen(fr'{CurrentPath}\SomeoneCalling.png') 
                        print("Someone is calling!"); pya.click(SomeoneCalling); break  # If we passed this stage
                    except Exception as e:
                        if CallInactive == False: print("Waiting for Answer Button to be active...."); print(e) # This is so it won't be spammed.
                        CallInactive = True # needed to not make above message spam
                        sleep(0.1)
                CallInactive = False
                # Sub-Loop: Wait for release button to load (Signifies that the call has loaded)
                while True:
                    try: gw.getWindowsWithTitle("(External)")[0]; break
                    except: 
                        if CallInactive == False: print("Waiting for call to load..."); CallInactive = True
            print("Call has started !!"); SoundFunctions.GeneralGreeting() # Greets and break out     
            GatherCallersInfo() # Grab Info From Caller

# Repeat
def GatherCallersInfo(SayRepeatVoiceLine=0,NeedMoreInfo=False):
    # Asks caller to repeat what they said if this is on
    if SayRepeatVoiceLine == 1: SoundFunctions.playVoiceLine("Repeat")
    CallersMessage = IceBarFunctions.getCallerMessage() 
    if CallersMessage == "Left the Call": return
    if NeedMoreInfo == False: DetailsExplained = f"A caller has said the following message: {CallersMessage}\nRespond to the caller's message"
    else: DetailsExplained = f"The caller has responded with the following message: {CallersMessage}\nRespond to the caller's message"
    BotMessaging.GenerateBotResponse(DetailsExplained)