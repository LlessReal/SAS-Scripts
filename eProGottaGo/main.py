import pyautogui as pya
import keyboard, threading
import pyperclip as pc
import clipboard as cb
import BoxManipulation, PDFReader, time
import config
running = True

def main():
    cb.copy("") # Reset clipboard for no problems
    print("Program starts in a sec (to get rid of shortcut bullshit)")
    time.sleep(1)

    global running
    while running:
        # Check Former Req ID
        FormerReqID = pc.paste() 
        print(f"Former ID was {FormerReqID}")
        cb.copy("") # Reset clip board     

        # You better have clicked a box at this point
        # Grab Req ID
        ReqID = BoxManipulation.GrabReqID() # Gets Req ID from box, and stores it (and copies it as well)
        
        # Checking for Duplicates
        if ReqID in FormerReqID: # If we got the same ID from before
            if "(SR Found)" in FormerReqID: # If SR was found
                print("A duplicate was found (SR Was Found in it)")
                #BoxManipulation.AddSRNum(ReqID) # Mark as N/A and copies status as No SR Found
            elif "(No SR Found)" in FormerReqID: # If no SR was found
                print("A duplicate was found (No SR Found in it)")
                #BoxManipulation.MarkNA() # Mark as N/A and copies status as No SR Found
            BoxManipulation.MoveBoxes("N/A") # Goes to N/A Box
            pya.press("up")
            pya.hotkey("ctrl","c")
            time.sleep(0.5)
            pya.press("down")
            pya.hotkey("ctrl","v")
            BoxManipulation.MoveBoxes("Req ID") # Returns to ReqID box, and goes to next row
            cb.copy(FormerReqID) # Copies same former req ID and status
            continue 
        
        # Moving to N/A Box (If previous stage went good)
        BoxManipulation.MoveBoxes("N/A")
        pya.hotkey("ctrl","c") # Copies box from N/A Column
        time.sleep(0.5) # Same reason as b4
        if pc.paste() == "N/A" or "SR" in pc.paste(): # If already marked as N/A or if a SR number is in it already
            BoxManipulation.MoveBoxes("Req ID") # Next Req ID
            continue
        else: # If empty
            SRSearch = PDFReader.CheckForSRNum(ReqID) # Checks if there's a SR Number     
            time.sleep(0.5) # Wait a bit
            if SRSearch == "No SR": # If no SR was deemed to be found
                BoxManipulation.MarkNA() # Mark as N/A
            elif SRSearch == "SR Found": # If SR was found
                # Get current color fro mfile
                with open(f"{config.CurrentPath}\\NextColor.txt","r") as f:
                    CurrentColor = f.read()
                # Write next color name
                with open(f"{config.CurrentPath}\\NextColor.txt","w") as f2:
                    try: # Tries to write down the next color
                        f2.write(config.AllColors[config.AllColors.index(CurrentColor) + 1])
                    except: # Resets if at max
                        f2.write(config.AllColors[0])
                
                BoxManipulation.AddSRNum(ReqID) # Add the SR Number (need to the Req ID to do so)
            # Next Req ID
            BoxManipulation.MoveBoxes("Req ID")
        # LOOP

    # If code ended due to hotkey, this goes.
    print("The code has halted.")

def start_function():
    global running
    running = True
    thread = threading.Thread(target=main)
    thread.start()

def stop_function():
    global running
    running = False

if __name__ == "__main__":
    while True:
        try:
            print("Press ctrl+shift+f to commense and press ctrl+shift+v to stop.")
            keyboard.add_hotkey("ctrl+shift+f", start_function)
            keyboard.add_hotkey("ctrl+shift+v", stop_function)
            keyboard.wait()
        except:
            print("it stopped")
            pass