import time, os
import pyautogui as pya
import keyboard
import pyperclip as pc
import clipboard as cb
import pygetwindow as gw

# You would get this by hovering over the app in task bar
ExcelSheetName = "BOR_POAP" # Doesn't have to be the full thing, but enough to distinguish it from other windows
eProDocName = "Manage Requisitions" #Same thing
# Must be on 205% on excel
def GrabBoxInfo(cordx,cordy):
    for i in range(3):
        pya.click(cordx, cordy) # Click the column info double below it (3 times) (Can't do right below cuz problems)
    time.sleep(0.5)
    pya.hotkey('ctrl', 'c') # Copies it
    return pc.paste()

def AutoGetZeros():
    InitialPosition = pya.position() # Save OG Position
    ###### PHASE 1 - GET INFO
    # Find B Column or whatever
    CurrentPath = os.path.dirname(__file__) # Gonna need this
    BImages = [f'{CurrentPath}\\B.png',f'{CurrentPath}\\B2.png',f'{CurrentPath}\\B3.png']
    while True:
        ColumnFText = ""
        cb.copy("") # Reset clip board
        BColumn = "" # Initial value
        for BImage in BImages:
            try:
                BColumn = pya.locateOnScreen(BImage) # Finds each column
            except:
                continue
            x, y = pya.center(BColumn) # Get the center of the button
            ColumnFText = GrabBoxInfo(x + 975,y + 80) # Copies info from the F Box first
            if ColumnFText != "N/A":
                print("No N/A Found")
                ColumnBText = GrabBoxInfo(x,y + 80) # Copies info below
                ReqID = ColumnBText[ColumnBText.find("5") - 4:] # Gets only the last few numbers (Finds 5, goes back to get 0s)
                if ReqID.replace(" ","") == "":
                    ColumnBText = GrabBoxInfo(x,y + 120) # Copies info below (but lower since unusual space)
                print(ReqID) # Debug
                cb.copy(ReqID) # Copy it
                time.sleep(1)
            break # Breaks out so it won't do it again (for some reason)
        if BColumn == "":
            return IndexError("Didnt find B column somehow") 
        if ColumnFText == "N/A":
            ScrollDownSign = pya.locateOnScreen(f"{CurrentPath}\\ScrollDownSign.png")
            pya.click(ScrollDownSign)
            print("Will retry in a few seconds")
            time.sleep(5)
            continue
        else:
            time.sleep(20)
            break
    ###### PHASE 2 - CHECK FOR INFO 
    WindowFound = False
    # Open PDF Doc (Must be at 100%)
    window = gw.getWindowsWithTitle("Manage Requisitions")[0] # Grab it
    WindowFound = True # If above worked with no error, shift to true
    if window.isMinimized: # If the window is minimized
        window.restore() # Unminimizes it
    window.activate()  # Activates the window
    time.sleep(0.5)

    if WindowFound == True:
        pya.hotkey('ctrl', 'f') # Find
        keyboard.write(pc.paste() + "\n") # Puts in Req ID and paste it (with enter)
        time.sleep(2) # Wait for box to load
        try:
            NoMatches = pya.locateOnScreen(f'{CurrentPath}\\NoMatches.png') # Tries to look for the No Matches box
            print(f"No SR for {ReqID}")
            time.sleep(0.5)
            keyboard.write("\n") # Enters
        except:
            print("SR Found") # If no box was found, SR is there

    # PHASE 3 - RETURN TP EXCEL SHEET
    ExcelSheet = gw.getWindowsWithTitle("BOR_POAP")[0] # Goes back to Excel Sheet
    if ExcelSheet.isMinimized: # If the window is minimized
        ExcelSheet.restore() # Unminimizes it
    ExcelSheet.activate()  # Activates the window
    time.sleep(0.5)
    ScrollDownSign = pya.locateOnScreen(f"{CurrentPath}\\ScrollDownSign.png")
    pya.click(ScrollDownSign) # Clicks scroll down sign
    time.sleep(0.5)
    pya.moveTo(InitialPosition)
    # LOOP

keyboard.add_hotkey("ctrl+`", AutoGetZeros)
keyboard.wait()



