import pyautogui as pya
import pyperclip as pc
import config, keyboard, time, PDFReader

# Function to fill color
def FillColor(Down,Right):
    pya.press('alt')
    keyboard.write("hh") # Alt + H + H
    time.sleep(0.5) # Wait a bit for box to load
    pya.press('down') # Initialize selection
    for Downs in range(Down):
        pya.press('down') # Goes down depending on how much called
    for Rights in range(Right):
        pya.press('right') # Goes right depending on how much called
    time.sleep(0.5)
    pya.press('enter') # Confirms color selection

# Parses out ReqID and copies it
def GrabReqID():
    pya.hotkey("ctrl","c") # Copies Req ID Column text
    time.sleep(0.5) # Wait a sec to process, or else it stores "gain" for some goddamn reason
    ReqIDColumnText = pc.paste()
    if ReqIDColumnText.replace(" ","") == "":
        return "Empty"
    elif ReqIDColumnText == "Retrieving data. Wait a few seconds and try to cut or copy again.":
        return "Cool Down"
    elif "00005" not in ReqIDColumnText:
        return "Unknown"
    
    ParsedReqID = ReqIDColumnText[ReqIDColumnText.find("5") - 4:] # Gets only the last few numbers (Finds 5, goes back to get 0s). Stops where a dash is located cuz irrelevant info
    if "-" in ParsedReqID:
        ParsedReqID = ParsedReqID[0:ReqIDColumnText.find("-")] # Reparse but without that other shit after
    print(f"The Parsed Req ID is {ParsedReqID}")
    return ParsedReqID # and returns it

# Marks box as N/A
def MarkNA(): # Put in coordinates of where the N/A should be written
    keyboard.write("N/A\n") # Puts in Req ID and paste it (with enter)
    pya.press('up') # Goes back to OG box
    FillColor(6,1) # Marks red

def MarkUnknown():
    keyboard.write("Unknown\n")
    pya.press('up')
    FillColor(6,0) # Marks dark red

# Function that adds SR Number to box
def AddSRNum(ReqID):
    AllTextAfterReqID = PDFReader.AllTextFromeProDoc[PDFReader.AllTextFromeProDoc.find(ReqID):] # Gets Req ID and text in front of it
    AllTextAfterSR = AllTextAfterReqID[AllTextAfterReqID.find("SR"):] # Get SR Number (that's after req id) and text in front of it
    while True:
        if AllTextAfterSR[2:8].isdigit():
            SRNumber = AllTextAfterSR[0:8]
            break
        else:
            print("SR Mismatch Detected, searching next SR")
            TheNextSRIndex = AllTextAfterSR.find("SR",AllTextAfterSR.find("SR") + 1) 
            AllTextAfterSR = AllTextAfterSR[TheNextSRIndex:] # Gets all text after and including the next SR Number
            continue

    keyboard.write(SRNumber + "\n")
    pya.press('up') 
    with open(f"{config.CurrentPath}\\NextColor.txt","r") as f:
        CurrentColor = f.read()
    ColorDict = {
        "Orange": [6,2],
        "Yellow": [6,3],
        "Green": [6,4],
        "Blue": [6,6],
        "Purple": [6,9]
    }
    FillColor(ColorDict[CurrentColor][0],ColorDict[CurrentColor][1]) # Marks gray
    
# Move to N/A Box depending on ReqID Column location
def MoveBoxes(BoxTarget=""):
    if BoxTarget == "N/A": # if we're moving to the N/A box
        for Box in range(config.ColumnDistance): # Gets distance to travel
            pya.press('right' if config.ReqIDColumnOnTheLeft else 'left')
            # Go right to the N/A box if Req ID is on the left
    elif BoxTarget == "Req ID": # If we're moving to the Req ID box
        pya.press("down")
        for Box in range(config.ColumnDistance): 
            pya.press('left' if config.ReqIDColumnOnTheLeft else 'right')
            # Go left to the Req ID Box if N/A Box is to the right of the Req ID