import tkinter as tk
from config import CharacterVoiceLines, CustomSounds, ImportantTermDictionary 
from SoundFunctions import playCustomSound, playCharacterLine, playVoiceLine
import OtherFunctions

def makeTransferGui(TheCallersWords):
    global root

    root = tk.Tk() # Creates main window
    root.wait_visibility() # Wait until the label becomes visible
    root.geometry("500x360") # Sets the window size

    PhoneNumLabel = tk.Label(root, text = 'Phone Number: ', font=('calibre',10, 'bold')) # Makes label with text Username and certain font
    PhoneNumLabel.grid(row=0,column=0)
    PhoneNum = tk.StringVar() # Declares variable for storing name
    PhoneNumEntry = tk.Entry(root, textvariable = PhoneNum, font=('calibre',10, 'bold')) # Makes entry where you can type things and stores it in TheName
    PhoneNumEntry.grid(row=0,column=1)
    PhoneNumEntry.bind("<Return>", lambda event: OtherFunctions.AutoTransferSubmitVersion(PhoneNumEntry.get()))
    NextInLine = 0
    for ImportantTerm in ImportantTermDictionary:
        if ImportantTerm in TheCallersWords.lower():
            OfficeInMention = f"({ImportantTermDictionary[ImportantTerm][1]})" if ImportantTermDictionary[ImportantTerm][1] != "" else f"({ImportantTerm})"
            print(f"{ImportantTerm} was found in the Caller's Message. Relevant Numbers: {ImportantTermDictionary[ImportantTerm][0]} {OfficeInMention}")
            SpecificPhoneNum = tk.Label(root, text = ImportantTermDictionary[ImportantTerm][0], font=('calibre',10, 'bold'))
            SpecificPhoneNum.grid(row=1 + NextInLine,column=0)
            DepartmentName = tk.Label(root, text = OfficeInMention, font=('calibre',10, 'bold'))
            DepartmentName.grid(row=1 + NextInLine,column=1)
            TransferButton = tk.Button(root, text = "Transfer", command = lambda: OtherFunctions.AutoTransferSubmitVersion(SpecificPhoneNum.cget("text")))
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
    WhatsYourNameButton = tk.Button(root, text = "What's your name?", command = lambda: playVoiceLine("Name"))
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
    return PhoneNum.get()