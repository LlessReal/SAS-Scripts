def NextRow(Status="Success",Swipes=1,NextBox=1):
    if Status == "Fail": # If Fail is in paremeter, this gets printed
        print("Process failed, doing next line")
    ScrollDownSign = pya.locateOnScreen(rf"{config.CurrentPath}\eProImages\ScrollDownSign.png",confidence=0.9)
    keyboard.write("\n")
    for i in range(Swipes + 1):
        pya.click(ScrollDownSign)
        time.sleep(0.25)
    pya.press('up') # Go back to same box
    time.sleep(0.25)
    for i in range(NextBox - 1):
        pya.click(ScrollDownSign)
        time.sleep(0.25)

ExcelSheetName = "BOR_POAP" # Doesn't have to be the full thing, but enough to distinguish it from other windows
eProDocName = "Manage Requisitions" # Same thing, but put the window in the middle monitor or it wont work
eProDocs = ["Basically a list of ePro docs lmfao"]
# Formerly I would make the program open the document and actually run Ctrl + F to see if there's a Req ID
# Thanks to PyPDF, this is no longer needed
def CheckForSRNum(ReqID):
    OtherFunctions.OpenWindow(config.eProDocName) # Open PDF Doc (Must be at 100%)
    pya.hotkey('ctrl', 'f') # Find
    keyboard.write(ReqID + "\n") # Puts in Req ID and paste it (with enter)
    time.sleep(1)
    try:
        NoMatches = pya.locateOnScreen(fr'{config.CurrentPath}\NoMatches.png',confidence=0.9) # Tries to look for the No Matches box
        print(f"No SR for {ReqID}") # If error didn't occur above, no SR was found
        pya.press('enter') # enters outta box
        return "No SR"
    except:
        print(f"SR Found for {ReqID}") # If no box was found, SR is there
        cb.copy(f"{ReqID} SR Found") # In order to prevent it from doing N/A in the next spots  
        return "SR Found"