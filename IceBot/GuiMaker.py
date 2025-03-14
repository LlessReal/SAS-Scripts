from config import VoicelineFolderName, ImportantTermDictionary, CurrentPath
from SoundFunctions import playSound, StopSounds
from OtherFunctions import OpenWindow
from Initiation import StartFunction, GatherCallersInfo
from IceBarFunctions import AutoTransferSubmitVersion
from tkinter import *
import os, threading, SchizoRadio, pygame, sys
from MicrosoftTeamsControl import MicrosoftTeamsChangeDevice

root = Tk(); root.title("IceBot Gui"); root.wait_visibility() 
root.geometry("700x480")
root.config(background="Gray")
StopSetting = IntVar(); TestingBotToggle = IntVar()

def RestartProgram(): root.destroy(); raise TypeError("Restarting Program") 
def makeTransferGui(TheCallersWords="",ResettingGui=True,StartingProgram=False,BotsResponse=""):
    if ResettingGui == True: ResetGui(); OpenWindow("IceBot Gui")
    
    # Phone Number Label and Entry
    PhoneNumLabel = Label(root, text = 'Phone Number: ', font=('calibre',10, 'bold')) # Makes label with text Username and certain font
    PhoneNumLabel.grid(row=0,column=0)
    PhoneNum = StringVar() # Declares variable for storing name
    PhoneNumEntry = Entry(root, textvariable = PhoneNum, font=('calibre',10, 'bold')) # Makes entry where you can type things and stores it in TheName
    PhoneNumEntry.grid(row=0,column=1)    
    PhoneNumEntry.bind("<Return>", lambda event: AutoTransferSubmitVersion(PhoneNumEntry.get(),TransferLineToggle.get(),WaitToggle.get(),StartingProgram=StartingProgram))
    
    # Transfer Number, Department Name, and Transfer Button
    NextInLine = 0
    for ImportantTerm in ImportantTermDictionary:
        # Transfer and allat
        if ImportantTerm in TheCallersWords.lower():
            OfficeInMention = f"({ImportantTermDictionary[ImportantTerm][1]})" if ImportantTermDictionary[ImportantTerm][1] != "" else f"({ImportantTerm})"
            print(f"{ImportantTerm} was found in the Caller's Message. Relevant Numbers: {ImportantTermDictionary[ImportantTerm][0]} {OfficeInMention}")
            SpecificPhoneNum = Label(root, text = ImportantTermDictionary[ImportantTerm][0], font=('calibre',10, 'bold'))
            SpecificPhoneNum.grid(row=1 + NextInLine,column=0)
            DepartmentName = Label(root, text = OfficeInMention, font=('calibre',10, 'bold'))
            DepartmentName.grid(row=1 + NextInLine,column=1)
            TransferButton = Button(root, text = "Transfer", bg="green", fg="white", command = lambda: AutoTransferSubmitVersion(SpecificPhoneNum.cget("text"),TransferLineToggle.get(),WaitToggle.get()))
            TransferButton.grid(row=1 + NextInLine,column=2)
            NextInLine += 1  

    SoundChannels = []
    # Custom Sound Buttons
    CustomSounds = os.listdir(fr"{CurrentPath}\Custom Sounds")
    CustomSoundLabel = Label(root, text = "Custom Sounds", font=('calibre',10, 'bold'))
    CustomSoundLabel.grid(row=1 + NextInLine,column=1)
    for CustomSound in CustomSounds:
        SoundChannels.append(pygame.mixer.Channel(len(SoundChannels)))
        if (CustomSounds.index(CustomSound) % 3) == 0 and CustomSounds.index(CustomSound) != 0: NextInLine += 1 
        CustomButton = Button(root, text = CustomSound[:CustomSound.find(".mp3")], bg="purple", fg="white", command = lambda IndividualSound=CustomSound, SoundChannel=SoundChannels[len(SoundChannels) - 1]: playSound(IndividualSound,SpeedScaleVariable.get(),BrainrotModeToggle.get(),CharacterLine=False,ChannelPicked=SoundChannel)) # Seperates the numbers
        CustomButton.grid(row=2 + NextInLine,column=(CustomSounds.index(CustomSound) % 3))
    
    # Character Voice Lines
    # Building the character voice lines list
    CharacterVoiceLines = [CharacterVoiceLine for CharacterVoiceLine in os.listdir(fr"{CurrentPath}\{VoicelineFolderName}") if "mp3" in CharacterVoiceLine]
    
    # Makes a new list with only files that have "mp3" in it
    CharacterVoiceLinesLabel = Label(root, text = "Custom Character Voice Lines", font=('calibre',10, 'bold'))
    CharacterVoiceLinesLabel.grid(row=3 + NextInLine,column=1)
    for CharacterVoiceLine in CharacterVoiceLines:
        SoundChannels.append(pygame.mixer.Channel(len(SoundChannels)))
        if (CharacterVoiceLines.index(CharacterVoiceLine) % 3) == 0 and CharacterVoiceLines.index(CharacterVoiceLine) != 0:
            NextInLine += 1 
        CharacterVoiceLineButton = Button(root, text = CharacterVoiceLine, bg="pink", fg="white", command = lambda t=CharacterVoiceLine: playSound(t,SpeedScaleVariable.get(),BrainrotModeToggle.get(),CharacterLine=True,ChannelPicked=SoundChannels[len(SoundChannels) - 1])) # Seperates the numbers
        CharacterVoiceLineButton.grid(row=4 + NextInLine,column=(CharacterVoiceLines.index(CharacterVoiceLine) % 3))
    
    # Transfer Toggle
    global TransferLineToggle; TransferLineToggle = IntVar(); TransferLineToggle.set(1)
    TransferVoiceLineOn = Checkbutton(root, text="Play transfer line", variable=TransferLineToggle)
    TransferVoiceLineOn.grid(row=5 + NextInLine,column=0)
    
    # Repeat/Ask For Clarification
    RepeatButton = Button(root, text = "Repeat/Ask For Clarification", bg="red", fg="white", state="disabled" if StartingProgram == True else "normal", command = lambda: GatherCallersInfo(SayMessage=RepeatVoiceLineToggle.get()))
    RepeatButton.grid(row=5 + NextInLine,column=1) # One bit over all the others

    # Wait Toggle
    global WaitToggle; WaitToggle = IntVar(); WaitToggle.set(1)
    WaitToggleOn = Checkbutton(root,text="Wait for Reaction",variable=WaitToggle)
    WaitToggleOn.grid(row=6 + NextInLine,column=0)
        
    # Start Main Function
    #if StartingProgram:
    if not StartingProgram:
        StartProgramButton = Button(root, text="Stop Program",bg="orange", command=RestartProgram)
    else:
        StartProgramButton = Button(root, text = "Commence Za Program", bg="yellow", fg="white", command = lambda: [StopSetting.set(0),InitiationThread.start(),StartProgramButton.config(text="Stop Program",bg="orange", command = lambda: exit("Restarting Program"))]) 
    StartProgramButton.grid(row=6 + NextInLine,column=1) # One bit over all the other
    #else:
    #    StopProgramButton = Button(root, text = "Stop Program", bg="orange", fg="white", command = lambda: [StopSetting.set(1),StopProgramButton.config(text="Stopping Program...",bg="red",state="disabled")])
    #    StopProgramButton.grid(row=6 + NextInLine,column=1) # One bit over all the others    
    
    # Stop all Sounds from playing 
    StopAllSoundsButton = Button(root, text = "Stop all Sounds", bg="black", fg="white", command = StopSounds)
    StopAllSoundsButton.grid(row=6 + NextInLine,column=2) # One bit over all the others
    
    # Repeat Toggle
    RepeatVoiceLineToggle = IntVar(); RepeatVoiceLineToggle.set(0)
    RepeatToggleBox = Checkbutton(root, text="Repeat Toggle",variable=RepeatVoiceLineToggle) 
    RepeatToggleBox.grid(row=7 + NextInLine,column=0)

    # Speed Scale
    SpeedScaleVariable = DoubleVar(); SpeedScaleVariable.set(1.0)
    SpeedScale = Scale( root, variable = SpeedScaleVariable,  
           from_ = 0.5, to = 2, resolution=0.01,
           orient = HORIZONTAL) 
    SpeedScale.grid(row=7 + NextInLine,column=1)
    # Normalize Speed Button
    NormalizeSpeedButton = Button( root, text="Normalize Speed", bg="purple",fg="white",command= lambda: SpeedScaleVariable.set(1.0)) 
    NormalizeSpeedButton.grid(row=8 + NextInLine,column=1)

    # Brainrot Mode
    BrainrotModeToggle = IntVar(); BrainrotModeToggle.set(0)
    BrainrotModeToggleBox = Checkbutton(root, text="Brainrot Mode",variable=BrainrotModeToggle) 
    BrainrotModeToggleBox.grid(row=8 + NextInLine,column=2)

    # Testing Bot Mode
    
    if StartingProgram: TestingBotToggle.set(0)
    TestingBotToggleBox = Checkbutton(root, text="Testing Bot",variable=TestingBotToggle,state= "disabled" if not StartingProgram else "normal") 
    TestingBotToggleBox.grid(row=9 + NextInLine,column=2)
    global InitiationThread
    InitiationThread = threading.Thread(target=lambda: StartFunction(TestingBotToggle.get(),StartingProgram=False))

    # Regular Mic Toggle Button
    HeadsetandMicToggle = Button( root, text="Get real mic", bg="purple",fg="white",command= lambda: MicrosoftTeamsChangeDevice("Switch to Human")) 
    HeadsetandMicToggle.grid(row=10 + NextInLine,column=0)
    # Stereo Mix Toggle Button
    StereoandSpeakerToggle = Button( root, text="Get stereo", bg="purple",fg="white",command= lambda:  MicrosoftTeamsChangeDevice("Change to Stereo")) 
    StereoandSpeakerToggle.grid(row=10 + NextInLine,column=1)

    PrivateConvo = Button( root, text="Private Convo", bg="purple",fg="white",command= lambda:  MicrosoftTeamsChangeDevice("Listening to Client")) 
    PrivateConvo.grid(row=10 + NextInLine,column=1)

    # Radio Toggle
    ToggleRadioButton = Button(root, text="Toggle Radio", bg="black",fg="white",command= lambda: SchizoRadio.RadioControl("On" if SchizoRadio.channel21.get_volume() == 0 else "Off")) 
    ToggleRadioButton.grid(row=11 + NextInLine,column=0)

    # Change Song
    ChangeSongButton = Button(root, text="Change Song", bg="white",fg="black",command= lambda: SchizoRadio.RadioControl("Change Song")) 
    ChangeSongButton.grid(row=11 + NextInLine,column=1)

    # Auto-Change Song
    global AutoChangeSongToggle; AutoChangeSongToggle = IntVar(); AutoChangeSongToggle.set(0)
    AutoChangeSongButton = Checkbutton(root, text="Auto-Change Song",variable=AutoChangeSongToggle) 
    AutoChangeSongButton.grid(row=11 + NextInLine,column=2)

    # Auto-Change Song
    global WaitBeforeContinuing; WaitBeforeContinuing = IntVar(); WaitBeforeContinuing.set(0)
    WaitBeforeContinuingButton = Checkbutton(root, text="Wait Before Continuing",variable=WaitBeforeContinuing) 
    WaitBeforeContinuingButton.grid(row=12 + NextInLine,column=0)

    # Refresh Button
    RefreshGuiButton = Button(root, text="Refresh Gui", bg="red",fg="white",command= lambda: makeTransferGui(TheCallersWords="",StartingProgram=StartingProgram)) 
    RefreshGuiButton.grid(row=13 + NextInLine,column=1)

    # Lastly...
    root.update()
    if StartingProgram and StopSetting.get() != 1: root.mainloop() 

# Function to clear/delete out all widgets inside a frame
def ResetGui(): 
    for widget in root.winfo_children(): widget.destroy() 

# Function that returns to the start
def BackToStageOne(AfterTransfer=False):
    if StopSetting.get() == 0:
        if AfterTransfer: InitiationThread.start(); return
    else: print("Time ta head out"); makeTransferGui(StartingProgram=True); return "ResetGuiNow"
