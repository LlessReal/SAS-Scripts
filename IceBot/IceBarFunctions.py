import pyautogui as pya
import GuiMaker
from time import sleep
from OtherFunctions import CloseWindow
# Selenium
import speech_recognition as sr
from config import model, CurrentPath
import SoundFunctions

# Function to press a button on IceBar (other than the drop down)
def PressIceButton(ImagePath,WaitMessage="",FailMessage="",TypeTransfer=False,TransferNumber=0,Wait=False):
    AlreadyTried = False 
    Timeout = 0   
    while True:
        try:
            ButtonToBePressed = pya.locateOnScreen(ImagePath) # Finds transfer button, if it's not on screen, goes to except
            if TypeTransfer == False:
                pya.click(ButtonToBePressed) # Click the button
            else: pya.write(f"{TransferNumber} \n") # Types number and then press enter
            sleep(1)
            return
        except:
            if Wait == True:
                if AlreadyTried == False:
                    print(WaitMessage)
                    AlreadyTried = True
                sleep(0.1)
                Timeout += 1
            if Timeout == 100 or Wait == False:
                print(FailMessage) 
                return "Fail"
            continue 


# Function that transfers the users
def AutoTransferSubmitVersion(TransferNumber,SayVoiceLine,WaitBeforeGo,StartingProgram=False):
    if StartingProgram:
        print("Program hasn't started yet")
        return
    if SayVoiceLine: # If Say Voice Line Check Box is Checked
        SoundFunctions.playVoiceLine("TransferingNow") # Plays line
        if WaitBeforeGo: # If Wait for reaction is checked
            print("Waiting for reaction")
            sleep(5) # Wait for reacton
    print(f"{TransferNumber} is attempting to be sent")
    # Save OG Position
    InitialPosition = pya.position()
    # Tries to press the dropdown
    MoveOnStatus = PressIceButton(fr"{CurrentPath}\..\IceBarImages\Icebardropdownarrow.png",FailMessage="Ice bar is closed/missing") 
    if MoveOnStatus != "Fail":
        # Pressing Transfer Button Next
        MoveOnStatus = PressIceButton(fr"{CurrentPath}\..\IceBarImages\TransferButton.png",FailMessage="You're not in a call.")   
        if MoveOnStatus != "Fail":
            # If we should type transfer next
            MoveOnStatus = PressIceButton(fr"{CurrentPath}\..\IceBarImages\InitiateTransferButton.png",WaitMessage="Waiting for Transfer Initiation to load..",FailMessage="Failed operation. PC too laggy",TypeTransfer=True,TransferNumber=TransferNumber) 
    
    if MoveOnStatus != "Fail": 
        CloseWindow("(External)") # Close the calling window   
        print("Transfer Successful!")
    print("Returning to initial stage")
    pya.moveTo(InitialPosition) # # Go to OG position
    ResetState = GuiMaker.BackToStageOne(True)

# Gets caller's message
def getCallerMessage():   
    recognizer = sr.Recognizer() # Initiate Recognizer
    microphone = sr.Microphone() # Initiate Mic
    AskedtoSpeakAlready = False
    with microphone as source: # Gets mic to listen to
        while True:
            print("Now Listening to Caller.....")
            try: audio = recognizer.listen(source, timeout=30) # Listens to customer's yap
            except sr.WaitTimeoutError:
                print("No message detected.")
                LeaveCallNotice = PleaseRepeat(AskedtoSpeakAlready)
                AskedtoSpeakAlready = True
                if LeaveCallNotice == "Left the Call": return
                else: continue
            
            print("Stopped recording")
            try: # Try to save their message
                with open(fr"{CurrentPath}\Caller's Message\CallersMessage.wav", "wb") as file: file.write(audio.get_wav_data())
                print("Audio saved as CallersMessage.wav")
            except Exception as e: print(f"Unable to save audio somehow {e}")
            try: # Tries to transcribe audio
                result = model.transcribe(fr"{CurrentPath}\Caller's Message\CallersMessage.wav",fp16=False, language='English')
                with open(fr"{CurrentPath}\Caller's Message\CallersMessageTranscription.txt","w") as f:
                    f.write(result["text"]) # Put it in a transcript.txt file
                print(f"Message said was: {result['text']}")
                if result["text"].replace(" ","") == "":
                    print("No message detected.")
                    LeaveCallNotice = PleaseRepeat(AskedtoSpeakAlready)
                    AskedtoSpeakAlready = True
                    if LeaveCallNotice == "Left the Call": return LeaveCallNotice
                return result["text"] # Returns the transcript for the user
            except Exception as e:
                print("Failed to recognize audio", e)
                LeaveCallNotice = PleaseRepeat(AskedtoSpeakAlready)
                AskedtoSpeakAlready = True
                if LeaveCallNotice == "Left the Call": return LeaveCallNotice
            

# Function that asks caller to repeat what they said
def PleaseRepeat(AskedtoSpeakAlready):
    if AskedtoSpeakAlready: # If we tried this already
        SoundFunctions.playVoiceLine("Goodbye") # Says good bye
        CloseWindow("(External)") # and closes the call window
        return "Left the Call"
    else: SoundFunctions.playVoiceLine("NoResponse") # Asks them to speak louder
# Make AskedtoSpeakAlready = True and add a continue after this function