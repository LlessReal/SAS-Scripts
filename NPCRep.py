import pyautogui as pya
import os
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
from tkinter import messagebox

# Before you use this program, run Install-Module -Name AudioDeviceCmdlets -Scope CurrentUser on Powershell
# This is for python to run the commands that change the input devices via commandline
ViewAllDeviceNames = False # Btw , if this is on the program won't go
HearRecording = False
RegularInputDeviceName = "Internal Microphone (Synaptics HD Audio)" # Replace with the exact name 
StereoInputDeviceName = "Stereo Mix (Synaptics HD Audio)" # Same Thing
ChatGPTLoginLink = r"https://auth.openai.com/authorize?audience=https%3A%2F%2Fapi.openai.com%2Fv1&client_id=TdJIcbe16WoTHtN95nyywh5E4yOo6ItG&device_id=6e9f462f-7a80-448f-b6ac-692abbf6ba78&ext-login-allow-phone=true&ext-oai-did=6e9f462f-7a80-448f-b6ac-692abbf6ba78&prompt=login&redirect_uri=https%3A%2F%2Fchatgpt.com%2Fapi%2Fauth%2Fcallback%2Fopenai&response_type=code&scope=openid+email+profile+offline_access+model.request+model.read+organization.read+organization.write&screen_hint=login&state=5jLqBHJPB5acvCeqdRyL54mMCz6yE6Xyvj0baiMQodQ&flow=treatment"
Email = "marshall3001.mm@gmail.com"
Password = "Miguel1@3$5^"
# CONFIGURATION OVER

ImportantTermDictionary = {
    "human resources": (7065078920,""),
    "admissions": (6001,"")
}

CurrentPath = os.path.dirname(__file__) # Gonna need this

def OpenWindow(WindowName):
    Window = gw.getWindowsWithTitle(WindowName)[0] # Goes back to Excel Sheet
    if Window.isMinimized: # If the window is minimized
        Window.restore() # Unminimizes it
    Window.activate()  # Activates the window

def AutoTransferSubmitVersion(TransferNumber):
    IcebarDropDownArrow = pya.locateOnScreen(fr"{CurrentPath}\IceBarImages\Icebardropdownarrow.png") # Can do directories as well btw
    InitialPosition = pya.position()
    pya.click(IcebarDropDownArrow) # Click the button        

    try:
        transferbutton = pya.locateOnScreen(fr"{CurrentPath}\IceBarImages\TransferButton.png") # Finds transfer button, if it's not on screen, goes to except
        pya.click(transferbutton) # Click the button
    except:
        print("You're not in a call.") 
        pya.click(IcebarDropDownArrow) # Clicks again to close
        tkExOut = pya.locateOnScreen(fr"{CurrentPath}\IceBarImages\tkExOut.png")
        pya.click(tkExOut)
        pya.moveTo(InitialPosition) # Go to OG position
        return # Ends function
    # Tries to find initiate transfer button to see if we should type info or not
    for i in range(10):
        try:
            InitiateTransferButton = pya.locateOnScreen(fr"{CurrentPath}\IceBarImages\InitiateTransferButton.png") # Checks if the 2nd window after you press transfer is up
            pya.write(f"{TransferNumber} \n") # Types number and then press enter
            break
        except:
            print("Couldn't find the initiate transfer button, retrying")
            sleep(1)
            if i == 9: # If 10 seconds passed and transfer still not complete
                print("Failed operation. PC too laggy") 
                pya.moveTo(InitialPosition) 
                return
        
    print("Transfer Successful!")
    tkExOut = pya.locateOnScreen(fr"{CurrentPath}\IceBarImages\tkExOut.png")
    pya.click(tkExOut)
    pya.moveTo(InitialPosition) # End

def main():
    # Check all devices and dip
    if ViewAllDeviceNames == True:
        print(sd.query_devices())
        return "Performed Input Device Listing"
    while True:
        ###### PHASE 1 - Answer Za Call
        while True:
            try: 
                # If we found that Answer is available and can be pressed
                AnswerAvailable = pya.locateOnScreen(fr'{CurrentPath}\IceBarImages\AnswerAvailable.png') # If error, it couldn't find it :(
                print("Answer Button is Active") # Let us know
                pya.click(AnswerAvailable) # Clicks it
                CallInactive = False # Reset CallInactive if it's True
                break # Break out to next stage
            except:
                if CallInactive == False: # This is so it won't be spammed.
                    print("Waiting for Answer Button to be active....")
                CallInactive = True
                sleep(1)

        ##### PHASE 2 - Muting and Preparing Bot to Listen to Caller
        while True:
            try:
                # Checks to see if mute option is available
                MuteAvailable = pya.locateOnScreen(fr'{CurrentPath}\IceBarImages\MuteAvailable.png') 
                print("Found Mute Button!")
                pya.click(MuteAvailable) # Clicks mute button
                os.system(fr'powershell -Command "& {{(Get-AudioDevice -List | Where-Object {{ $_.Name -like \"{StereoInputDeviceName}\" }}) | Set-AudioDevice }}"')
                # Input changed to Stereo, for bot to listen to caller
                break
            except:
                print("Didn't find Mute Button On")
                sleep(1)
        
        ##### PHASE 3 - Grab Info From Caller
        recognizer = sr.Recognizer() # Initiate Recognizer
        microphone = sr.Microphone() # Initiate Mic
        try:
            with microphone as source:
                print("Now Listening to Caller.....")
                audio = recognizer.listen(source) # Wait for customer to stop yapping
                print("Stopped recording")
            if HearRecording:
                try: 
                    with open("recorded_audio.wav", "wb") as file:
                        file.write(audio.get_wav_data())
                    print("Audio saved as recorded_audio.wav")
                except Exception as e:
                    print(f"Could not request results; {e}")
            CallersWords = recognizer.recognize_google(audio)
            print(CallersWords)
            NextInLine = 0
            # Make the gui
            root = tk.Tk() # Creates main window
            root.wait_visibility() # Wait until the label becomes visible
            root.geometry("1280x720") # Sets the window size

            PhoneNumLabel = tk.Label(root, text = 'Phone Number: ', font=('calibre',10, 'bold')) # Makes label with text Username and certain font
            PhoneNumLabel.grid(row=0,column=0)
            PhoneNum = tk.StringVar() # Declares variable for storing name
            PhoneNumEntry = tk.Entry(root, textvariable = PhoneNum, font=('calibre',10, 'bold')) # Makes entry where you can type things and stores it in TheName
            PhoneNumEntry.grid(row=0,column=1)
            PhoneNumEntry.bind("<Return>", lambda event: AutoTransferSubmitVersion(PhoneNumEntry.get()))
            for ImportantTerm in ImportantTermDictionary:
                if ImportantTerm in CallersWords.lower():
                    NextInLine += 1
                    OfficeInMention = f"({ImportantTermDictionary[ImportantTerm][1]})" if ImportantTermDictionary[ImportantTerm][1] != "" else f"({ImportantTerm})"
                    print(f"{ImportantTerm} was found in the Caller's Message. Relevant Numbers: {ImportantTermDictionary[ImportantTerm][0]} {OfficeInMention}")
                    SpecificPhoneNum = tk.Label(root, text = ImportantTermDictionary[ImportantTerm][0], font=('calibre',10, 'bold'))
                    SpecificPhoneNum.grid(row=0 + NextInLine,column=0)
                    DepartmentName = tk.Label(root, text = OfficeInMention, font=('calibre',10, 'bold'))
                    DepartmentName.grid(row=0 + NextInLine,column=1)
                    TransferButton = tk.Button(root, text = "Transfer", command = lambda: AutoTransferSubmitVersion(SpecificPhoneNum.cget("text")))
                    TransferButton.grid(row=0 + NextInLine,column=2)
            root.mainloop()
            print("The deed is done")
                
        except Exception as e:
            print("Failure", e)
            CallersWords = ""

        # End (Change audio input back to microphone)
        os.system(fr'powershell -Command "& {{(Get-AudioDevice -List | Where-Object {{ $_.Name -like \"{RegularInputDeviceName}\" }}) | Set-AudioDevice }}"')
        # Loop happens here

if __name__ == '__main__':
    try:
        main()
    except:
        print("The program broke L")
        # Set input device back to regular mic
        os.system(fr'powershell -Command "& {{(Get-AudioDevice -List | Where-Object {{ $_.Name -like \"{RegularInputDeviceName}\" }}) | Set-AudioDevice }}"')