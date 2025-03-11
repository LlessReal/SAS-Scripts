import pyautogui as pya
import keyboard, threading
import pyperclip as pc
import config, BoxManipulation, time, os
running = True

CurrentPath = os.path.dirname(__file__) 
def main():
    print("Program starts in a sec (to get rid of shortcut bullshit)")
    time.sleep(1)
    EmptyCounter = 0
    global running
    FormerReqID = ""
    while running:
        # Check Former Req ID
        if FormerReqID != "": print(f"Former ID was {FormerReqID}")  

        # You better have clicked a box at this point
        # Grab Req ID
        ReqID = BoxManipulation.GrabReqID() # Gets Req ID from box, and stores it (and copies it as well)
        
        if ReqID == "Empty":
            print("Empty Box")
            pya.press("down") # Next, no coloring
            EmptyCounter += 1
            if EmptyCounter == 10:
                print("10 Empty Boxes detected, stopping program")
                running = False # If we got 10 empty boxes, exit program, we done
            else: continue # Go back to program
        else: EmptyCounter = 0 # If it wasn't empty, there's more info

        # If the box was Unknown
        if ReqID == "Unknown": BoxManipulation.MarkUnknown(); continue

        if ReqID == "Cool Down": print("Cooling down...."); time.sleep(30); continue

        # Checking for Duplicates
        if ReqID in FormerReqID: # If we got the same ID from before
            if "(SR Found)" in FormerReqID: # If SR was found
                print("A duplicate was found (SR Was Found in it)")
                #BoxManipulation.AddSRNum(ReqID) # Mark as N/A and copies status as No SR Found
            elif "(No SR Found)" in FormerReqID: # If no SR was found
                print("A duplicate was found (No SR Found in it)")
                #BoxManipulation.MarkNA() # Mark as N/A and copies status as No SR Found
            BoxManipulation.MoveBoxes("N/A") # Goes to N/A Box
            BoxManipulation.CopyAbove()
            BoxManipulation.MoveBoxes("Req ID") # Returns to ReqID box, and goes to next row
            continue 
        
        # Moving to N/A Box (If previous stage went good)
        BoxManipulation.MoveBoxes("N/A")
        pya.hotkey("ctrl","c") # Copies box from N/A Column
        time.sleep(0.5) # Same reason as b4
        # If already marked as N/A or if a SR number is in it already
        if pc.paste() == "N/A" or "SR" in pc.paste(): BoxManipulation.MoveBoxes("Req ID"); continue # Next Req ID
        else: # If empty
            SRSearch = BoxManipulation.CheckForSRNum(ReqID) # Checks if there's a SR Number     
            if SRSearch == "No SR": BoxManipulation.MarkNA() # # If no SR was deemed to be found Mark as N/A
            elif SRSearch == "SR Found": # If SR was found
                # Get current color fro mfile
                with open(f"{CurrentPath}\\NextColor.txt","r") as f: CurrentColor = f.read()
                # Write next color name
                with open(f"{CurrentPath}\\NextColor.txt","w") as f2:
                    try: f2.write(config.AllColors[config.AllColors.index(CurrentColor) + 1]) # Tries to write down the next color
                    except: f2.write(config.AllColors[0]) # Resets if at max
            
                BoxManipulation.AddSRNum(ReqID) # Add the SR Number (need to the Req ID to do so)
            FormerReqID = f"{ReqID} (SR Found)" if SRSearch == "SR Found" else f"{ReqID} (No SR Found)"
            # Next Req ID
            BoxManipulation.MoveBoxes("Req ID")
        # LOOP

    # If code ended due to hotkey, this goes.
    print("The code has halted.")

def start_function():
    global running; running = True
    thread = threading.Thread(target=main); thread.start()

def stop_function(): global running; running = False

while True:
    try:
        print("Click the first box, then Press ctrl+shift+f to commense and press ctrl+shift+v to stop.")
        keyboard.add_hotkey("ctrl+shift+f", start_function)
        keyboard.add_hotkey("ctrl+shift+v", stop_function)
        keyboard.wait()
    except: print("it stopped")