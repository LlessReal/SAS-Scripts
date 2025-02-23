import pyautogui as pya
import pyperclip as pc
import clipboard as cb
import config, keyboard, time

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
        ParsedReqID = ParsedReqID[0:ReqIDColumnText.find("-")] # Reparse but without that other shit
    print(f"The Parsed Req ID is {ParsedReqID}")
    print("Req ID Grabbed and Copied!")
    cb.copy(ParsedReqID) # Copy it
    print(f"Copied ID was {pc.paste()}") # Debug
    return ParsedReqID # and returns it

# Marks box as N/A
def MarkNA(): # Put in coordinates of where the N/A should be written
    keyboard.write("N/A\n") # Puts in Req ID and paste it (with enter)
    pya.press('up') # Goes back to OG box
    FillColor(6,1) # Marks red

# Move to N/A Box depending on ReqID Column location
def MoveToNABox():
    for Box in range(config.ColumnDistance):
        if config.ReqIDColumnOnTheLeft:
            pya.press('right')
        else:
            pya.press('left')

# Move to Req ID Box
def MoveToReqIDBox(RowShift = ""):
    if RowShift == "Next Row":
        pya.press('down')
    for Box in range(config.ColumnDistance):
        if config.ReqIDColumnOnTheLeft:
            pya.press('left')
        else:
            pya.press('right')   