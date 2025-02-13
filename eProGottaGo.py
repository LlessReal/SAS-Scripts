import time, os
import pyautogui as pya
import keyboard
import pyperclip as pc
import clipboard as cb
import pygetwindow as gw
import threading
running = True

# Before you start line up the columns
# You would get this by hovering over the app in task bar
ExcelSheetName = "BOR_POAP" # Doesn't have to be the full thing, but enough to distinguish it from other windows
eProDocName = "Manage Requisitions" # Same thing, but put the window in the middle monitor or it wont work
ReqIDHeaderLetter = "JayWorkE"
NAHeaderLetter = "JayWorkF"
FontImageName = "JayWorkFont"
ShiftToInfo = 80 # Test things out
CurrentPath = os.path.dirname(__file__) # Gonna need this
# Must be on 200% on excel 
def GrabBoxInfo(cordx,cordy,ReqID=False):
    cb.copy("")
    if ReqID == True:
        pya.click(cordx, cordy) # Click the column info double below it (3 times) (Can't do right below cuz problems)
        time.sleep(0.5)
        pya.hotkey('ctrl', 'c') # Copies it
        time.sleep(0.25)
        keyboard.write("\n")
    else:
        for i in range(3):
            pya.click(cordx, cordy) # Click the column info double below it (3 times) (Can't do right below cuz problems)
        time.sleep(0.5) # Take time so it can copy it right
        pya.hotkey('ctrl', 'c') # Copies it
        if pc.paste() == "N/A":
            GoToSameBox()
            return pc.paste()
        else:
            keyboard.write("Testing")
            time.sleep(0.25)
            for i in range(3):
                pya.click(cordx, cordy) # Click the column info double below it (3 times) (Can't do right below cuz problems)
            time.sleep(0.5)
            pya.hotkey('ctrl', 'c') # Copies it
    return pc.paste()

def GrabReqID(cordx,cordy):
    ReqIDColumnText = GrabBoxInfo(cordx,cordy,True) # Does same function above
    ParsedReqID = ReqIDColumnText[ReqIDColumnText.find("5") - 4:] # Gets only the last few numbers (Finds 5, goes back to get 0s). Stops where a dash is located cuz irrelevant info
    if "-" in ParsedReqID:
        ParsedReqID = ParsedReqID[0:ReqIDColumnText.find("-")] # Reparse but without that other shit
    print(f"The Parsed Req ID is {ParsedReqID}")
    return ParsedReqID # and returns it

def GrabNAStatus(cordx,cordy):
    NAColumnText = GrabBoxInfo(cordx,cordy) # Does same function above
    return NAColumnText # and returns it

def GoToSameBox():
    keyboard.write("\n")
    pya.press('up') # Copies it

# Scroll to next row, (put continue after this)
def NextRow(Status="Success",Swipes=1,NextBox=1):
    if Status == "Fail": # If Fail is in paremeter, this gets printed
        print("Process failed, doing next line")
    ScrollDownSign = pya.locateOnScreen(rf"{CurrentPath}\eProImages\ScrollDownSign.png",confidence=0.9)
    keyboard.write("\n")
    for i in range(Swipes + 1):
        pya.click(ScrollDownSign)
        time.sleep(0.25)
    pya.press('up') # Go back to same box
    time.sleep(0.25)
    for i in range(NextBox - 1):
        pya.click(ScrollDownSign)
        time.sleep(0.25)

def MarkNA(cordx,cordy,BoostExistent=False): # Put in coordinates of where the N/A should be written
    for i in range(3):
        pya.click(cordx, cordy) # Click the column info double below it (3 times) (Can't do right below cuz problems)
    time.sleep(0.25)
    keyboard.write("N/A\n") # Puts in Req ID and paste it (with enter)
    pya.press('up') # Goes back to OG box
    time.sleep(0.5) # Wait for buckets to ungray out
    FontText = pya.locateOnScreen(fr"{CurrentPath}\eProImages\{FontImageName}.png",confidence=0.9) # So it can find font but not the bucket.... INTERESTINGGGG
    x, y = pya.center(FontText) # Get the center of the button
    pya.click(x + 70, y - 40)

    # Python won't look at the top bar for Excel for some reason, so a simple image wont work :(
    # Make sure bucket is on red

def OpenWindow(WindowName):
    Window = gw.getWindowsWithTitle(WindowName)[0] # Goes back to Excel Sheet
    if Window.isMinimized: # If the window is minimized
        Window.restore() # Unminimizes it
    Window.activate()  # Activates the window

def eProGottaGo():
    ###### PHASE 1 - GET INFO
    # Find B Column or whatever
    global running
    while running:
        while running:
            FormerReqID = pc.paste() # Gets the former grabbed Req ID
            print(f"Former ID was {FormerReqID}")
            cb.copy("") # Reset clip board     
            # Find the header for Req IDs
            try:
                ReqIDHeader = pya.locateOnScreen(fr'{CurrentPath}\eProImages\{ReqIDHeaderLetter}.png',confidence=0.9) # Finds each column   
                print("Req ID Header Found")
                x, y = pya.center(ReqIDHeader) # Get the center of the button
            except:
                return IndexError("Didnt find ReqID Header somehow") 
            ###### PHASE 2 - Get Req ID
            ReqID = GrabReqID(x,y + ShiftToInfo) # Copies info below    
            print("Req ID Grabbed and Copied!")
            cb.copy(ReqID) # Copy it
            print(f"Copied ID was {pc.paste()}") # Debug
            ###### PHASE 3 - Check for Duplicates
            # Find N/A Header
            try:
                NAHeader = pya.locateOnScreen(fr'{CurrentPath}\eProImages\{NAHeaderLetter}.png',confidence=0.9) # Finds each column   
                print("N/A ID Header Found")
                x, y = pya.center(NAHeader) # Get the center of the button
            except:
                return IndexError("Didnt find N/A Header somehow") 
            Boost = 0
            while running:
                NAInfo = GrabNAStatus(x,y + ShiftToInfo + Boost) # Copies info from the F Box first
                if NAInfo.replace(" ","") == "": # If we didn't get a req ID
                    print("Space Detected, Checking next box")
                    Boost += 40
                elif NAInfo == "N/A":
                    NextRow(Swipes=2,NextBox=int(1 + (Boost / 40)))
                    break
                else:
                    print("Onto next stage!!!")
                    GoToSameBox()
                    break
            if NAInfo == "N/A":
                NAInfo = ""
                continue
            
            cb.copy(ReqID) # Copy ReqID again
            time.sleep(0.5)
            if pc.paste() in FormerReqID: # If we got the same ID
                if "SR Found" not in FormerReqID:
                    print("A duplicate was found (No SR Found in it)")
                    MarkNA(x,y + ShiftToInfo + Boost)
                    NextRow("Fail",Swipes=2,NextBox=int(1 + (Boost // 40)))
                else:
                    print("A duplicate was found (SR Was Found in it)")
                    NextRow("Fail",Swipes=2,NextBox=int(1 + (Boost // 40)))
                    cb.copy(f"{ReqID} SR Found") # In order to prevent it from doing N/A in the next spots
                continue
            else:
                break
            
        ###### PHASE 2 - CHECK FOR INFO 
        OpenWindow(eProDocName) # Open PDF Doc (Must be at 100%)
        time.sleep(0.5)
        pya.hotkey('ctrl', 'f') # Find
        time.sleep(0.5)
        keyboard.write(pc.paste() + "\n") # Puts in Req ID and paste it (with enter)
        time.sleep(2) # Wait for box to load
        NoMatches = ""
        try:
            NoMatches = pya.locateOnScreen(fr'{CurrentPath}\eProImages\NoMatches.png',confidence=0.9) # Tries to look for the No Matches box
            print(f"No SR for {ReqID}")
            time.sleep(0.5)
            keyboard.write("\n") # Enters out of the box 
        except:
            print("SR Found") # If no box was found, SR is there
            cb.copy(f"{ReqID} SR Found") # In order to prevent it from doing N/A in the next spots     

        # PHASE 3 - RETURN TO EXCEL SHEET
        OpenWindow(ExcelSheetName)
        if NoMatches != "":
            MarkNA(x,y + ShiftToInfo + Boost,True if Boost != 0 else False) # Mark as N/A
        else:
            keyboard.write("\n") # Enters to next box
        time.sleep(3)
        if "SR Found" not in pc.paste():
            NextRow(Swipes=2,NextBox=int(1 + (Boost // 40)))
        else:
            NextRow(Swipes=2,NextBox=int(0 + (Boost // 40))) 
        time.sleep(3)
        # LOOP
    print("The code has halted.")

def screenshotmoment():
    global running
    if running:
        screenshot = pya.screenshot()
        screenshot.save("Testshot.png")

def start_function():
    global running
    running = True
    thread = threading.Thread(target=eProGottaGo)
    thread.start()

def stop_function():
    global running
    running = False

keyboard.add_hotkey("shift+f2", start_function)
keyboard.add_hotkey("ctrl+f3", stop_function)
keyboard.wait()