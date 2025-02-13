import speech_recognition as sr
import os
import pygetwindow as gw
from time import sleep
#Gui 
import tkinter as tk
from tkinter import messagebox
import pyautogui as pya
CurrentPath = os.path.dirname(__file__) # Gonna need this
HearRecording = False
ImportantTermDictionary = {
    "human resources": (7065078920,""),
    "admissions": (6001,""),
    "financial aid": (6002,""),
    "bursar": (6002,""),
    "registrar": (6004,""),
    "orientation": (7065078593,""),
    "advisor": (7065078780,""),
    "admissions": (6001,""),
    "admissions": (6001,""),
}
TestStereo = False
RegularInputDeviceName = "Internal Microphone (Synaptics HD Audio)" # Replace with the exact name 
StereoInputDeviceName = "Stereo Mix (Synaptics HD Audio)" # Same Thing
if TestStereo:
    os.system(fr'powershell -Command "& {{(Get-AudioDevice -List | Where-Object {{ $_.Name -like \"{StereoInputDeviceName}\" }}) | Set-AudioDevice }}"')
else:
    os.system(fr'powershell -Command "& {{(Get-AudioDevice -List | Where-Object {{ $_.Name -like \"{RegularInputDeviceName}\" }}) | Set-AudioDevice }}"')
    
def OpenWindow(WindowName):
    Window = gw.getWindowsWithTitle(WindowName)[0] # Goes back to Excel Sheet
    if Window.isMinimized: # If the window is minimized
        Window.restore() # Unminimizes it
    Window.activate()  # Activates the window

def AutoTransferSubmitVersion(TransferNumber):
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

while True:
    recognizer = sr.Recognizer() # Initiate Recognizer
    microphone = sr.Microphone() # Initiate Mic
    
    with microphone as source:
        print("Now Listening to Caller.....")
        audio = recognizer.listen(source,phrase_time_limit=20) # Wait for customer to stop yapping
        print("Stopped recording")
    if HearRecording:
        try:
            with open("recorded_audio.wav", "wb") as file:
                file.write(audio.get_wav_data())
            print("Audio saved as recorded_audio.wav")
        except Exception as e:
            print(f"Could not request results; {e}")
    try:
        CallersWords = recognizer.recognize_google(audio,language='en-US')
        print(CallersWords)
    except Exception as e:
        print("Failed to recognize audio", e)
        CallersWords = ""
        
    NextInLine = 0
    # Make the gui
    root = tk.Tk() # Creates main window
    root.wait_visibility() # Wait until the label becomes visible
    root.geometry("640x360") # Sets the window size

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
    os.system(fr'powershell -Command "& {{(Get-AudioDevice -List | Where-Object {{ $_.Name -like \"{RegularInputDeviceName}\" }}) | Set-AudioDevice }}"')
    print("The deed is done. You can retest in 5 seconds")
    sleep(5) # You may retest i