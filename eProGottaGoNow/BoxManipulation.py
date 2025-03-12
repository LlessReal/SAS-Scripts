import pyautogui as pya
import pyperclip as pc
import keyboard, time, re, config, Tools.PDFReader

AllTextFromeProDoc = "" # Extract text from each page
for eProDoc in config.eProDocs: # Goes through each document in the list of documents you placed
    AllTextFromeProDoc += Tools.PDFReader.GetPDFText(eProDoc,"Adobe",ShowText=True)
# we're reading all the pages from each doc ya 

# Check if text grabbed is still empty
if AllTextFromeProDoc == "":
    exit("Why is the documents folder empty.")

# Function to fill color
def FillColor(Down,Right):
    pya.press('alt'); keyboard.write("hh"); time.sleep(0.5) 
    pya.press('down') # Initialize selection
    for Downs in range(Down): pya.press('down') # Goes down depending on how much called
    for Rights in range(Right): pya.press('right') # Goes right depending on how much called
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
    print("Unknown Box.")
    MoveBoxes("N/A") # Goes to N/A Box
    keyboard.write("Unknown\n")
    pya.press('up')
    MoveBoxes("Req ID") # Goes to N/A Box
    FillColor(6,0) # Marks dark red

# Function that adds SR Number to box
def AddSRNum(ReqID):
    AllTextAfterReqID = AllTextFromeProDoc[AllTextFromeProDoc.find(ReqID):] # Gets Req ID and text in front of it
    SRNumberGotten = re.findall(r"SR\d{6}",AllTextAfterReqID)
    SRNumber = SRNumberGotten[0] 
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

def CopyAbove():
    pya.press("up")
    pya.hotkey("ctrl","c")
    pya.press("down")
    pya.hotkey("ctrl","v")

# Function that checks if the Req ID is in the document
def CheckForSRNum(ReqID):
    if AllTextFromeProDoc.find(ReqID) == -1: # If the ID wasn't found in the text
        print(f"No SR for {ReqID}") # If error didn't occur above, no SR was found
        return "No SR"
    else:
        print(f"SR Found for {ReqID}") # If no box was found, SR is there
        return "SR Found"