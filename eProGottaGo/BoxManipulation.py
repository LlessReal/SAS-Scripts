import pyautogui as pya
import pyperclip as pc
import clipboard as cb
import config, keyboard, time, PDFReader

# Function to fill color
def FillColor(Down,Right):
    pya.press('alt')
    keyboard.write("hh") # Alt + H + H
    time.sleep(0.25) # Wait a bit for box to load
    pya.press('down') # Initialize selection
    for Downs in range(Down):
        pya.press('down') # Goes down depending on how much called
    for Rights in range(Right):
        pya.press('right') # Goes right depending on how much called
    pya.press('enter') # Confirms color selection

# Parses out ReqID and copies it
def GrabReqID():
    pya.hotkey("ctrl","c") # Copies Req ID Column text
    time.sleep(0.5) # Wait a sec to process, or else it stores "gain" for some goddamn reason
    ReqIDColumnText = pc.paste()
    ParsedReqID = ReqIDColumnText[ReqIDColumnText.find("5") - 4:] # Gets only the last few numbers (Finds 5, goes back to get 0s). Stops where a dash is located cuz irrelevant info
    if "-" in ParsedReqID:
        ParsedReqID = ParsedReqID[0:ReqIDColumnText.find("-")] # Reparse but without that other shit after
    print(f"The Parsed Req ID is {ParsedReqID}")
    cb.copy(ParsedReqID) # Copy it
    print(f"Req ID Grabbed and Copied! Copied ID: {pc.paste()}") # Debug
    return ParsedReqID # and returns it

# Marks box as N/A
def MarkNA(): # Put in coordinates of where the N/A should be written
    keyboard.write("N/A\n") # Puts in Req ID and paste it (with enter)
    pya.press('up') # Goes back to OG box
    FillColor(6,1) # Marks red

# Function that adds SR Number to box
def AddSRNum(ReqID):
    AllTextAfterReqID = PDFReader.AllTextFromDoc[PDFReader.AllTextFromDoc.find(ReqID):]
    SRNumber = AllTextAfterReqID[AllTextAfterReqID.find("SR"):AllTextAfterReqID.find("SR") + 8]
    keyboard.write(SRNumber + "\n")
    pya.press('up') 
    FillColor(4,0) # Marks gray
    
# Move to N/A Box depending on ReqID Column location
def MoveBoxes(BoxTarget=""):
    if BoxTarget == "N/A": # if we're moving to the N/A box
        for Box in range(config.ColumnDistance): # Gets distance to travel
            pya.press('right' if config.ReqIDColumnOnTheLeft else 'left')
            # Go right to the N/A box if Req ID is on the left
    elif BoxTarget == "Req ID": # If we're moving to the Req ID box
        for Box in range(config.ColumnDistance): 
            pya.press('left' if config.ReqIDColumnOnTheLeft else 'right')
            # Go left to the Req ID Box if N/A Box is to the right of the Req ID