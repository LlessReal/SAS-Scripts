import pyautogui as pya
from time import sleep
import pygetwindow as gw
# Selenium
import speech_recognition as sr
from config import model, CurrentPath, RegularInputDeviceName, StereoInputDeviceName
import GuiMaker, os
from SoundFunctions import playVoiceLine
from Initiation import StartFunction
# Opens Window
def OpenWindow(WindowName):
    Window = gw.getWindowsWithTitle(WindowName)[0] # Goes back to Excel Sheet
    if Window.isMinimized: # If the window is minimized
        Window.restore() # Unminimizes it
    Window.activate()  # Activates the window
# Closes Window
def CloseWindow(WindowName):
    Window = gw.getWindowsWithTitle(WindowName)[0] # Goes back to Excel Sheet
    Window.close()  # Activates the window

# Gets caller's message
def getCallerMessage():   
    recognizer = sr.Recognizer() # Initiate Recognizer
    microphone = sr.Microphone() # Initiate Mic
    AskedtoSpeakAlready = False
    with microphone as source: # Gets mic to listen to
        while True:
            print("Now Listening to Caller.....")
            try:
                audio = recognizer.listen(source, timeout=5) # Listens to customer's yap
                AskedtoSpeakAlready = False # Reset if it was True
                break
            except sr.WaitTimeoutError:
                print("No message detected.")
                if AskedtoSpeakAlready:
                    playVoiceLine("Goodbye") # Says good bye and closes call window
                    CloseWindow("(External)") # Closes the call window
                    return "Left the Call"
                else:
                    playVoiceLine("NoResponse")
                    AskedtoSpeak = True
            
        print("Stopped recording")
    try: # Try to save their message
        with open(fr"{CurrentPath}\Caller's Message\CallersMessage.wav", "wb") as file:
            file.write(audio.get_wav_data())
        print("Audio saved as CallersMessage.wav")
    except Exception as e:
        print(f"Unable to save audio somehow {e}")
    try: # Tries to transcribe audio
        result = model.transcribe(fr"{CurrentPath}\Caller's Message\CallersMessage.wav",fp16=False, language='English')
        with open(fr"{CurrentPath}\Caller's Message\CallersMessageTranscription.txt","w") as f:
            f.write(result["text"]) # Put it in a transcript.txt file
        print(f"Message said was: {result["text"]}")
        return result["text"] # Returns the transcript for the user
    except Exception as e:
        print("Failed to recognize audio", e)
        return ""
# Auto Transfer
def AutoTransferSubmitVersion(TransferNumber,SayVoiceLine,WaitBeforeGo):
    if SayVoiceLine == 1: # If Say Voice Line Check Box is Checked
        playVoiceLine("TransferingNow") # Plays line
        if WaitBeforeGo == 1: # If Wait for reaction is checked
            print("Waiting for reaction")
            sleep(5) # Wait for reacton
    print(f"{TransferNumber} Will be sent")
    try:
        IcebarDropDownArrow = pya.locateOnScreen(fr"{CurrentPath}\..\IceBarImages\Icebardropdownarrow.png") # Can do directories as well btw
        InitialPosition = pya.position()
        pya.click(IcebarDropDownArrow) # Click the button        
    except:
        print("Ice bar is closed/missing")
        StartFunction()
        return

    try:
        transferbutton = pya.locateOnScreen(fr"{CurrentPath}\..\IceBarImages\TransferButton.png") # Finds transfer button, if it's not on screen, goes to except
        pya.click(transferbutton) # Click the button
    except:
        print("You're not in a call.") 
        pya.click(IcebarDropDownArrow) # Clicks again to close
        pya.moveTo(InitialPosition) # Go to OG position
        return # Ends function
    # Tries to find initiate transfer button to see if we should type info or not
    for i in range(10):
        try:
            InitiateTransferButton = pya.locateOnScreen(fr"{CurrentPath}\..\IceBarImages\InitiateTransferButton.png") # Checks if the 2nd window after you press transfer is up
            pya.write(f"{TransferNumber} \n") # Types number and then press enter
            sleep(2)
            break
        except:
            print("Couldn't find the initiate transfer button, retrying")
            sleep(1)
            if i == 9: # If 10 seconds passed and transfer still not complete
                print("Failed operation. PC too laggy") 
                pya.moveTo(InitialPosition) 
                return
    CloseWindow("(External)") # Close the calling window   
    print("Transfer Successful!")
    pya.moveTo(InitialPosition) # End
    # FINAL PHASE - Return to Normal
    ChangeToRegularMic()
    print("The deed is done")

def ChangeToRegularMic():
    os.system(fr'powershell -Command "& {{(Get-AudioDevice -List | Where-Object {{ $_.Name -like \"{RegularInputDeviceName}\" }}) | Set-AudioDevice }}"')

def ChangeToStereoMix():
    os.system(fr'powershell -Command "& {{(Get-AudioDevice -List | Where-Object {{ $_.Name -like \"{StereoInputDeviceName}\" }}) | Set-AudioDevice }}"')
