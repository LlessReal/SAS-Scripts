import pyautogui as pya
import os, whisper, random
from time import sleep
import pygetwindow as gw
# Selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import sounddevice as sd 
import speech_recognition as sr
import tkinter as tk
import wave, pyaudio, pygame
import datetime
# Before you use this program, run Install-Module -Name AudioDeviceCmdlets -Scope CurrentUser on Powershell
# This is for python to run the commands that change the input devices via commandline
ViewAllDeviceNames = False # Btw , if this is on the program won't go
HearRecording = False
TestStereo = False
VoicelineFolderName = "Mickey" # Add GoodAfternoon.wav, GoodMorning.wav, Greeting.wav (With numbers after), PleaseWait.wav, and Repeat.wav
CharacterVoiceLines = ["Laugh"]
CustomSounds = ["Get out","I missed the part where that's my problem","Packgod Meme","Thwomp","Packgod Mickey","Never"]
RegularInputDeviceName = "Internal Microphone (Synaptics HD Audio)" # Replace with the exact name 
StereoInputDeviceName = "Stereo Mix (Synaptics HD Audio)" # Same Thing
ImportantTermDictionary = {
    "human resources": (7065078920,""),
    "admissions": (6001,""),
    "financial aid": (6002,""),
    "bursar": (6002,""),
    "registrar": (6004,""),
    "orientation": (7065078593,""),
    "advisor": (7065078780,""),
    "military": (7065078866,""),
    "housing": (7065078710,""),
}

CurrentPath = os.path.dirname(__file__) # Gonna need this
model = whisper.load_model("base") # Download the model
pygame.mixer.init() # Initialization

def playCustomSound(SoundName):
    (pygame.mixer.Sound(fr"{CurrentPath}\Custom Sounds\{SoundName}.mp3")).play()

def playCharacterLine(SoundName):
    (pygame.mixer.Sound(fr"{CurrentPath}\{VoicelineFolderName}\{SoundName}.mp3")).play()
    
def PlayWaveFile(WavFile):
    chunk = 1024  
    wf = wave.open(WavFile, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(chunk)
    while data:
        stream.write(data)
        data = wf.readframes(chunk)
    stream.stop_stream()
    stream.close()
    p.terminate()

def PlayVoiceLine(VoicelineType):
    try:
        UnmuteSign = pya.locateOnScreen(fr"{CurrentPath}\IceBarImages\Unmute.png")
        pya.click(UnmuteSign)
    except:
        pass
    AllVoicelines = [] # List Initialization
    for Voiceline in os.listdir(fr"{CurrentPath}\{VoicelineFolderName}"): # Gets all files in the Voiceliens folder
        if VoicelineType in os.path.join(fr"{CurrentPath}\{VoicelineFolderName}", Voiceline): # If the type of voiceline is in the file name
            AllVoicelines.append(os.path.join(fr"{CurrentPath}\{VoicelineFolderName}", Voiceline)) # Add it to the list
    PlayWaveFile(random.choice(AllVoicelines)) # Play a random sound from the type

def OpenWindow(WindowName):
    Window = gw.getWindowsWithTitle(WindowName)[0] # Goes back to Excel Sheet
    if Window.isMinimized: # If the window is minimized
        Window.restore() # Unminimizes it
    Window.activate()  # Activates the window

def CloseWindow(WindowName):
    Window = gw.getWindowsWithTitle(WindowName)[0] # Goes back to Excel Sheet
    Window.close()  # Activates the window

def AutoTransferSubmitVersion(TransferNumber):
    root.destroy()
    PlayVoiceLine("TransferingNow")
    print(f"{TransferNumber} Will be sent")
    IcebarDropDownArrow = pya.locateOnScreen(fr"{CurrentPath}\IceBarImages\Icebardropdownarrow.png") # Can do directories as well btw
    InitialPosition = pya.position()
    pya.click(IcebarDropDownArrow) # Click the button        

    try:
        transferbutton = pya.locateOnScreen(fr"{CurrentPath}\IceBarImages\TransferButton.png") # Finds transfer button, if it's not on screen, goes to except
        pya.click(transferbutton) # Click the button
    except:
        print("You're not in a call.") 
        pya.click(IcebarDropDownArrow) # Clicks again to close
        pya.moveTo(InitialPosition) # Go to OG position
        return # Ends function
    # Tries to find initiate transfer button to see if we should type info or not
    for i in range(10):
        try:
            InitiateTransferButton = pya.locateOnScreen(fr"{CurrentPath}\IceBarImages\InitiateTransferButton.png") # Checks if the 2nd window after you press transfer is up
            pya.write(f"{TransferNumber} \n") # Types number and then press enter
            sleep(2)
            CloseWindow("(External)")
            break
        except:
            print("Couldn't find the initiate transfer button, retrying")
            sleep(1)
            if i == 9: # If 10 seconds passed and transfer still not complete
                print("Failed operation. PC too laggy") 
                pya.moveTo(InitialPosition) 
                return
        
    print("Transfer Successful!")
    pya.moveTo(InitialPosition) # End

def getCallerMessage(Status=""):
    if Status == "Repeat":
        PlayVoiceLine("Repeat")
        
    recognizer = sr.Recognizer() # Initiate Recognizer
    microphone = sr.Microphone() # Initiate Mic
    with microphone as source:
        print("Now Listening to Caller.....")
        audio = recognizer.listen(source) # Wait for customer to stop yapping
        print("Stopped recording")
    if HearRecording:
        try:
            with open(fr"{CurrentPath}\CallerMessage.wav", "wb") as file:
                file.write(audio.get_wav_data())
            print("Audio saved as CallerMessage.wav")
        except Exception as e:
            print(f"Could not request results; {e}")
    try:
        result = model.transcribe(fr"{CurrentPath}\CallerMessage.wav",fp16=False, language='English')
        with open(fr"{CurrentPath}\CallerMessageTranscription.txt","w") as f:
            f.write(result["text"])
        print(f"Message said was: {result["text"]}")
        return result["text"]
    except Exception as e:
        print("Failed to recognize audio", e)
        return ""

def main():
    # Check all devices and dip
    if ViewAllDeviceNames == True:
        print(sd.query_devices())
        return "Performed Input Device Listing"
    while True:

###### PHASE 1 - Answer Za Call
        CallInactive = False
        while True:
            try: 
                # If we found that Answer is available and can be pressed
                SomeoneCalling = pya.locateOnScreen(fr'{CurrentPath}\IceBarImages\SomeoneCalling.png') # If error, it couldn't find it :(
                print("Someone is calling!") # Let us know
                pya.click(SomeoneCalling) # Clicks it
                CallInactive = False # Reset CallInactive if it's True
                os.system(fr'powershell -Command "& {{(Get-AudioDevice -List | Where-Object {{ $_.Name -like \"{StereoInputDeviceName}\" }}) | Set-AudioDevice }}"') 
                # Swap to stereo (May take a while)
                # Wait for thing to load
                while True:
                    try:
                        ReleaseAvailable = pya.locateOnScreen(fr'{CurrentPath}\IceBarImages\ReleaseAvailable.png') # If error, it couldn't find it :(
                        break
                    except:
                        print("Waiting for call to load...")
                        sleep(1)
                CurrentDateandTime = datetime.datetime.now()
                PlayVoiceLine("GoodMorning" if CurrentDateandTime.strftime("%p") == "AM" else "GoodAfternoon")
                PlayVoiceLine("Greeting")
                break # Break out to next stage
            except Exception as e:
                if CallInactive == False: # This is so it won't be spammed.
                    print(e)
                    print("Waiting for Answer Button to be active....")
                CallInactive = True
                sleep(1)

        ##### PHASE 2 - Muting Myself to Hear Caller
        # Checks to see if mute option is available
        MuteAvailable = pya.locateOnScreen(fr'{CurrentPath}\IceBarImages\MuteAvailable.png') 
        print("Found Mute Button!")
        pya.click(MuteAvailable) # Clicks mute button
        # Input changed to Stereo, for bot to listen to caller

        ##### FINAL PHASE (PART 1) - Grab Info From Caller
        Status = ""
        def repeatMessage():
            PhoneNum.set("Repeat")
            root.destroy()
        while True:
            CallersWords = getCallerMessage(Status)    
            PlayVoiceLine("PleaseWait")
            ##### FINAL PHASE (PART 2) - TRANSFER GUI
            global root
            root = tk.Tk() # Creates main window
            root.wait_visibility() # Wait until the label becomes visible
            root.geometry("400x360") # Sets the window size

            PhoneNumLabel = tk.Label(root, text = 'Phone Number: ', font=('calibre',10, 'bold')) # Makes label with text Username and certain font
            PhoneNumLabel.grid(row=0,column=0)
            PhoneNum = tk.StringVar() # Declares variable for storing name
            PhoneNumEntry = tk.Entry(root, textvariable = PhoneNum, font=('calibre',10, 'bold')) # Makes entry where you can type things and stores it in TheName
            PhoneNumEntry.grid(row=0,column=1)
            PhoneNumEntry.bind("<Return>", lambda event: AutoTransferSubmitVersion(PhoneNumEntry.get()))
            NextInLine = 0
            for ImportantTerm in ImportantTermDictionary:
                if ImportantTerm in CallersWords.lower():
                    OfficeInMention = f"({ImportantTermDictionary[ImportantTerm][1]})" if ImportantTermDictionary[ImportantTerm][1] != "" else f"({ImportantTerm})"
                    print(f"{ImportantTerm} was found in the Caller's Message. Relevant Numbers: {ImportantTermDictionary[ImportantTerm][0]} {OfficeInMention}")
                    SpecificPhoneNum = tk.Label(root, text = ImportantTermDictionary[ImportantTerm][0], font=('calibre',10, 'bold'))
                    SpecificPhoneNum.grid(row=1 + NextInLine,column=0)
                    DepartmentName = tk.Label(root, text = OfficeInMention, font=('calibre',10, 'bold'))
                    DepartmentName.grid(row=1 + NextInLine,column=1)
                    TransferButton = tk.Button(root, text = "Transfer", command = lambda: AutoTransferSubmitVersion(SpecificPhoneNum.cget("text")))
                    TransferButton.grid(row=1 + NextInLine,column=2)
                    NextInLine += 1  

            CustomSoundLabel = tk.Label(root, text = "Custom Sounds", font=('calibre',10, 'bold'))
            CustomSoundLabel.grid(row=1 + NextInLine,column=1)
            for CustomSound in CustomSounds:
                if (CustomSounds.index(CustomSound) % 3) == 0 and CustomSounds.index(CustomSound) != 0:
                    NextInLine += 1 
                CustomButton = tk.Button(root, text = CustomSound, command = lambda t=CustomSound: playCustomSound(t)) # Seperates the numbers
                CustomButton.grid(row=2 + NextInLine,column=(CustomSounds.index(CustomSound) % 3))
            CharacterVoiceLinesLabel = tk.Label(root, text = "Custom Character Voice Lines", font=('calibre',10, 'bold'))
            CharacterVoiceLinesLabel.grid(row=3 + NextInLine,column=1)
            for CharacterVoiceLine in CharacterVoiceLines:
                if (CharacterVoiceLines.index(CharacterVoiceLine) % 3) == 0 and CharacterVoiceLines.index(CharacterVoiceLine) != 0:
                    NextInLine += 1 
                CharacterVoiceLineButton = tk.Button(root, text = CharacterVoiceLine, command = lambda t=CharacterVoiceLine: playCharacterLine(t)) # Seperates the numbers
                CharacterVoiceLineButton.grid(row=4 + NextInLine,column=(CharacterVoiceLines.index(CharacterVoiceLine) % 3))
            WhatsYourNameButton = tk.Button(root, text = "What's your name?", command = lambda: PlayVoiceLine("Name"))
            WhatsYourNameButton.grid(row=5 + NextInLine,column=1) # One bit over all the others    
            def repeatMessage():
                PhoneNum.set("Repeat")
                root.destroy()
            TransferLineToggle = tk.IntVar()
            TransferLineToggle.set(1)
            TransferVoiceLineOn = tk.Checkbutton(root, text="Play transfer line", variable=TransferLineToggle)
            TransferVoiceLineOn.grid(row=6 + NextInLine,column=0)
            RepeatButton = tk.Button(root, text = "Repeat/Ask For Clarification", command = repeatMessage)
            RepeatButton.grid(row=6 + NextInLine,column=1) # One bit over all the others
            root.mainloop()
            Status = PhoneNum.get()
            if Status == "Repeat":
                continue
            else:
                break
            
        # End (Change audio input back to microphone)
        os.system(fr'powershell -Command "& {{(Get-AudioDevice -List | Where-Object {{ $_.Name -like \"{RegularInputDeviceName}\" }}) | Set-AudioDevice }}"')
        print("The deed is done")
        # Loop happens here

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("The program broke L", e)
        # Set input device back to regular mic
        os.system(fr'powershell -Command "& {{(Get-AudioDevice -List | Where-Object {{ $_.Name -like \"{RegularInputDeviceName}\" }}) | Set-AudioDevice }}"')