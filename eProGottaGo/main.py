import pyautogui as pya
import keyboard, threading
import pyperclip as pc
import clipboard as cb
import BoxManipulation, Acrobat, OtherFunctions, config, time
running = True

def main():
    print("Program starts in a sec (to get rid of shortcut bullshit)")
    time.sleep(1)
    global running
    while running:
        # Check Former Req ID
        FormerReqID = pc.paste() # Gets the former grabbed Req ID
        print(f"Former ID was {FormerReqID}")
        cb.copy("") # Reset clip board     

        # You better have clicked a box at this point
        # Grab Req ID
        ReqID = BoxManipulation.GrabReqID() # Copies info from Req Box and only gets Req ID
        # Check for Dupes
        if pc.paste() in FormerReqID: # If we got the same ID from before
            if "SR Found" not in FormerReqID:
                print("A duplicate was found (No SR Found in it)")
                BoxManipulation.MoveToNABox()
                BoxManipulation.MarkNA()
                BoxManipulation.MoveToReqIDBox("Next Row")
                cb.copy(ReqID) # Fail proof smh
            else:
                print("A duplicate was found (SR Was Found in it)")
                pya.press('down') # Next box, no point in going to N/A box
                cb.copy(f"{ReqID} SR Found") # In order to prevent it from doing N/A in the next spots
            continue
        else:
            pass   
        
        BoxManipulation.MoveToNABox()
        # Check for already filled spots
        pya.hotkey("ctrl","c") # Grabs box from N/A Column
        time.sleep(0.5) # Same reason as b4
        if pc.paste() == "N/A" or "SR" in pc.paste():
            BoxManipulation.MoveToReqIDBox("Next Row")
            continue
        
        # If spot wasn't filled, searches for SR in pdf doc.
        SRSearch = Acrobat.CheckForSr(ReqID) # PHASE 2 - CHECK FOR INFO         
        OtherFunctions.OpenWindow(config.ExcelSheetName) # PHASE 3 - RETURN TO EXCEL SHEET
        time.sleep(1)
        if SRSearch == "No SR":
            BoxManipulation.MarkNA() # Mark as N/A
        elif SRSearch == "SR Found":
            pass
        BoxManipulation.MoveToReqIDBox("Next Row")
        cb.copy(ReqID) # Save ReqID for checking former Req IDs

        # LOOP
    # If code ended due to hotkey, this goes.
    print("The code has halted.")

def screenshotmoment():
    global running
    if running:
        screenshot = pya.screenshot()
        screenshot.save("Testshot.png")

def start_function():
    global running
    running = True
    thread = threading.Thread(target=main)
    thread.start()

def stop_function():
    global running
    running = False


if __name__ == "__main__":
    cb.copy("") # Reset clipboard for no problems
    print("Press ctrl+shift+fto commense,ctrl+shift+v to stop.")
    keyboard.add_hotkey("ctrl+shift+f", start_function)
    keyboard.add_hotkey("ctrl+shift+v", stop_function)
    keyboard.wait()