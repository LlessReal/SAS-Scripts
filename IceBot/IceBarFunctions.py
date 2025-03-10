import pyautogui as pya
from time import sleep
import time
from OtherFunctions import CloseWindow
# Selenium
import speech_recognition as sr
from config import model, CurrentPath
import SoundFunctions, SchizoRadio

# Function to press a button on IceBar (other than the drop down)
from pywinauto import Application
app = Application(backend='uia').connect(title_re=".*Settings.*")

def TransferToNumber(TransferNumber=0):
    try:
        app = Application(backend='uia').connect(title_re=".*iceBar.*"); print("Successfully connected to iceBar")
        main_window = app.window(title_re=".*iceBar.*")
    except: print("Icebar is off"); return
    DropDown = main_window.child_window(title="More Contact Buttons", auto_id="ContactOverflowPopupToggleButton", control_type="Button")
    DropDown.click_input()
    TransferButton = main_window.child_window(title="Transfer", auto_id="TransferCallButton_1", control_type="Button")
    TransferButton.click_input()
    sleep(5); pya.write(f"{TransferNumber} \n")

# Function that transfers the users
def AutoTransferSubmitVersion(TransferNumber,SayVoiceLine,WaitBeforeGo,StartingProgram=False):
    if StartingProgram: print("Program hasn't started yet"); return
    if SayVoiceLine: # If Say Voice Line Check Box is Checked
        SoundFunctions.playVoiceLine("TransferingNow") # Plays line
        # If Wait for reaction is checked
        if WaitBeforeGo: print("Waiting for reaction"); sleep(5) # Wait for reacton
    print(f"{TransferNumber} is attempting to be sent")
    # Save OG Position
    InitialPosition = pya.position()
    # Tries to press the dropdown
    TransferToNumber(TransferNumber) 
    CloseWindow("(External)")
    print(" Transfer Successful! Returning to initial location"); pya.moveTo(InitialPosition) # # Go to OG position


def wait_for_silence(recognizer, source, silence_duration=5, silence_threshold=1000):
    """
    Waits until there is silence for a specified duration.
    
    :param recognizer: The recognizer instance.
    :param source: The audio source.
    :param silence_duration: The duration of silence to wait for (in seconds).
    :param silence_threshold: The energy threshold to consider as silence.
    :return: True if silence is detected, False if timeout occurs.
    """
    start_time = time.time()
    while True:
        print("Listening...")
        audio = recognizer.listen(source, timeout=1)  # Listen for 1 second
        energy = sum(abs(audio.get_raw_data())) / len(audio.get_raw_data())
        
        if energy < silence_threshold:
            print("Silence detected.")
            if time.time() - start_time >= silence_duration: return True
        else: start_time = time.time()  # Reset the timer if sound is detected
        
        # Overall timeout to prevent infinite loop
        if time.time() - start_time > 30: print("Timeout occurred."); return False

# Gets caller's message
def getCallerMessage():   
    recognizer = sr.Recognizer() # Initiate Recognizer
    microphone = sr.Microphone() # Initiate Mic
    AskedtoSpeakAlready = False
    with microphone as source: # Gets mic to listen to
        while True:
            recognizer.adjust_for_ambient_noise(source)
            print("Now Listening to Caller.....")
            #print("Waiting for silence...")
            #if wait_for_silence(recognizer, source, silence_duration=5): print("Silence detected for 5 seconds.")
            #else: print("Silence not detected within the timeout period.")
            try: audio = recognizer.listen(source, timeout=30) # Listens to customer's yap
            except sr.WaitTimeoutError:
                print("No message detected.")
                LeaveCallNotice = PleaseRepeat(AskedtoSpeakAlready)
                AskedtoSpeakAlready = True
                if LeaveCallNotice == "Left the Call": return
                else: continue
            
            print("Stopped recording"); SchizoRadio.RadioControl("On")
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
        SoundFunctions.playVoiceLine("Goodbye"); CloseWindow("(External)"); return "Left the Call"
    else: SoundFunctions.playVoiceLine("NoResponse") # Asks them to speak louder
# Make AskedtoSpeakAlready = True and add a continue after this function