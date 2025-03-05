import pyautogui as pya
from time import sleep
from config import CurrentPath, api_key
import GuiMaker, SoundFunctions, pyttsx3, IceBarFunctions, SchizoRadio
engine = pyttsx3.init() # Initialize the engine
# Adjust speaking rate and volume
engine.setProperty('rate', 150); engine.setProperty('volume', 1.0)
# Change to male voice
voices = engine.getProperty('voices'); engine.setProperty('voice', voices[0].id)

from huggingface_hub import InferenceClient

client = InferenceClient(
	provider="novita",
	api_key=api_key
)

def StartFunction(TestingBot,StartingProgram):
    GuiMaker.makeTransferGui()
    if not StartingProgram:
        ###### PHASE 1 - Greeting
        if TestingBot: # If testing, will use regular mic, then go straight to general greeting
            print("Testing Mode On. Program starts in 5 seconds"); sleep(5)
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
                    if CallInactive == False: print("Waiting for Answer Button to be active....") # This is so it won't be spammed.
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
        CallersMessage = IceBarFunctions.getCallerMessage() 
        DetailsExplained = f"A caller has said the following message: {CallersMessage}\nRespond to the caller's message"
        GenerateBotResponse(DetailsExplained)

### Message Context
PhoneNumDetails = open(fr"{CurrentPath}\Details.txt","r", encoding='utf-8', errors='ignore').read()
SystemMessage = f"""You are a bot at Columbus State University meant to transfer people to the right number depending on what they ask for
You'll be transfering them from the numbers below. 
if you're going to transfer them to a number, say, '[INITIATE TRANSFER - (The Number)]' AT THE VERY END of your response, and replace (The Number) with the actual number you're transfering them to of course.
{PhoneNumDetails}"""

def GenerateBotResponse(DetailsExplained):
    SoundFunctions.playVoiceLine("PleaseWait")
    SchizoRadio.RadioControl("On")
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
    except Exception as e: print(f"Error running bot {e}"); return
    SchizoRadio.RadioControl("Off")
    print(f"Bot's Response: {BotsResponse}")
    # Says the bot's response (Without the initiate part lol) and stop the engine after
    engine.say(BotsResponse.replace(BotsResponse[BotsResponse.find("[INITIATE"):],"")); engine.runAndWait(); engine.stop() 
    # FINAL PHASE: Transfering
    if "INITIATE TRANSFER" in BotsResponse: 
        IceBarFunctions.AutoTransferSubmitVersion(TransferNumber=BotsResponse[BotsResponse.find("- ") + 2:BotsResponse.find("]")],SayVoiceLine=GuiMaker.TransferLineToggle.get(),WaitBeforeGo=GuiMaker.WaitToggle.get())

# Repeat
def RepeatPlease(SayRepeatVoiceLine=0):
    # Asks caller to repeat what they said if this is on
    if SayRepeatVoiceLine == 1: SoundFunctions.playVoiceLine("Repeat")
    CallersMessage = IceBarFunctions.getCallerMessage() 
    DetailsExplained = f"A caller has said the following message: {CallersMessage}\nRespond to the caller's message"
    GenerateBotResponse(DetailsExplained)