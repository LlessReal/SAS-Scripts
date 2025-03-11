import pyautogui as pya
from time import sleep
import time
from OtherFunctions import CloseWindow
# Selenium
import speech_recognition as sr
from config import model, CurrentPath
import SoundFunctions, SchizoRadio
import numpy as np
from MicrosoftTeamsControl import ChangeInputandOutput
# Function to press a button on IceBar (other than the drop down)
from pywinauto import Application
app = Application(backend='uia').connect(title_re=".*Teams and Channels \\| Settings.*")

def TransferToNumber(TransferNumber=0):
    try:
        app = Application(backend='uia').connect(title_re=".*iceBar.*"); print("Successfully connected to iceBar")
        main_window = app.window(title_re=".*iceBar.*")
    except: print("Icebar is off"); return
    DropDown = main_window.child_window(title="More Contact Buttons", auto_id="ContactOverflowPopupToggleButton", control_type="Button")
    DropDown.click_input()
    TransferButton = main_window.child_window(title="Transfer", auto_id="TransferCallButton_1", control_type="Button")
    TransferButton.click_input()
    sleep(5); pya.write(f"{TransferNumber} \n"); sleep(1)

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
    print("Transfer Successful! Returning to initial location"); pya.moveTo(InitialPosition) # # Go to OG position


recognizer,microphone = sr.Recognizer(), sr.Microphone() # Initiate Recognizer and Mic
# Gets caller's message
def getCallerMessage():   
    AskedtoSpeakAlready = False
    with microphone as source: # Gets mic to listen to
        while True:
            print("Now Listening to Caller.....")
            #recognizer.adjust_for_ambient_noise(source)
            #print("Waiting for silence...")
            #if wait_for_silence(recognizer, source, silence_duration=3): print("Silence detected for 5 seconds.")
            #else: print("Silence not detected within the timeout period.")
            fullaudio = b''
            audio = b''
            # Listen to customer's yap
            FirstWords = True
            while True:
                try: 
                    recognizer.adjust_for_ambient_noise(source)
                    # Waits for em to talk (waits 5 seconds if first message, 1 if they said something already)
                    audio = recognizer.listen(source,timeout=5 if FirstWords else 1)
                    # If they said nothing, the code below won't go
                    audiodata = audio.get_raw_data()
                    # Calculate energy
                    samples = np.frombuffer(audiodata, dtype=np.int16)  # Use correct dtype
                    energy = np.mean(np.abs(samples))
                    print(f"Energy: {energy}")
                    # If nothing was meant to be said, break out
                    if energy < 200: break 
                    # Otherwise, we'll add to the full audio
                    fullaudio += audiodata # Add to full data 
                    combined_audio = sr.AudioData(fullaudio, audio.sample_rate, audio.sample_width)
                    FirstWords = False # No longer their first words
                # If they don't talk, we break, thus nothing is added to the audio
                except sr.WaitTimeoutError: break 
            
            print("No more audio detected, stopped recording."); ChangeInputandOutput("Speaking to Client"); SchizoRadio.RadioControl("On")
            if audio == b'': # If we didn't get any new audio data, they said nothing
                print("No message detected.")
                LeaveCallNotice = PleaseRepeat(AskedtoSpeakAlready)
                AskedtoSpeakAlready = True
                if LeaveCallNotice == "Left the Call": return LeaveCallNotice
                else: continue

            # Next stage
            try: # Try to save their message
                # Boost audio
                raw_data = np.frombuffer(combined_audio.get_raw_data(), dtype=np.int16) # Convert raw audio data to a NumPy array
                boosted_data = (raw_data * 1.5).astype(np.int16) # Boost the audio by multiplying with the gain factor
                boosted_data = np.clip(boosted_data, -32768, 32767) # Clip the data to ensure it stays within the valid range for int16
                boosted_bytes = boosted_data.tobytes() # Convert the boosted data back to bytes
                boosted_audio = sr.AudioData(boosted_bytes, audio.sample_rate, audio.sample_width) # Create a new AudioData object with the boosted audio
                with open(fr"{CurrentPath}\Caller's Message\CallersMessage.wav", "wb") as soundfile: soundfile.write(boosted_audio.get_wav_data())
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
                    else: continue
                return result["text"] # Returns the transcript for the user
            except Exception as e:
                print("Failed to recognize audio", e)
                LeaveCallNotice = PleaseRepeat(AskedtoSpeakAlready)
                AskedtoSpeakAlready = True
                if LeaveCallNotice == "Left the Call": return LeaveCallNotice
                else: continue

# Function that asks caller to repeat what they said
def PleaseRepeat(AskedtoSpeakAlready):
    if AskedtoSpeakAlready: # If we tried this already
        print("Caller is absent, leaving call..."); SoundFunctions.playVoiceLine("Goodbye"); CloseWindow("(External)"); return "Left the Call"
    else: SoundFunctions.playVoiceLine("NoResponse") # Asks them to speak louder
    ChangeInputandOutput("Listening to Client")
# Make AskedtoSpeakAlready = True and add a continue after this function