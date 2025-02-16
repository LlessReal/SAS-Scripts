import pyautogui as pya
from time import sleep
import pygetwindow as gw
# Selenium
import speech_recognition as sr
from config import model, CurrentPath 
import GuiMaker
from SoundFunctions import playVoiceLine

def OpenWindow(WindowName):
    Window = gw.getWindowsWithTitle(WindowName)[0] # Goes back to Excel Sheet
    if Window.isMinimized: # If the window is minimized
        Window.restore() # Unminimizes it
    Window.activate()  # Activates the window

def CloseWindow(WindowName):
    Window = gw.getWindowsWithTitle(WindowName)[0] # Goes back to Excel Sheet
    Window.close()  # Activates the window


def getCallerMessage(Status=""):
    if Status == "Repeat":
        playVoiceLine("Repeat")
        
    recognizer = sr.Recognizer() # Initiate Recognizer
    microphone = sr.Microphone() # Initiate Mic
    with microphone as source:
        print("Now Listening to Caller.....")
        audio = recognizer.listen(source) # Wait for customer to stop yapping
        print("Stopped recording")
    try:
        with open(fr"{CurrentPath}\Caller's Message\CallersMessage.wav", "wb") as file:
            file.write(audio.get_wav_data())
        print("Audio saved as CallersMessage.wav")
    except Exception as e:
        print(f"Could not request results; {e}")
    try:
        result = model.transcribe(fr"{CurrentPath}\Caller's Message\CallersMessage.wav",fp16=False, language='English')
        with open(fr"{CurrentPath}\Caller's Message\CallersMessageTranscription.txt","w") as f:
            f.write(result["text"])
        print(f"Message said was: {result["text"]}")
        return result["text"]
    except Exception as e:
        print("Failed to recognize audio", e)
        return ""

def AutoTransferSubmitVersion(TransferNumber):
    GuiMaker.root.destroy()
    playVoiceLine("TransferingNow")
    print(f"{TransferNumber} Will be sent")
    try:
        IcebarDropDownArrow = pya.locateOnScreen(fr"{CurrentPath}\..\IceBarImages\Icebardropdownarrow.png") # Can do directories as well btw
        InitialPosition = pya.position()
        pya.click(IcebarDropDownArrow) # Click the button        
    except:
        print("Ice bar is closed/missing")
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