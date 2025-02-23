import pyautogui as pya
import pyperclip as pc
import clipboard as cb 
import OtherFunctions, config, keyboard, time

def CheckForSr(ReqID):
    OtherFunctions.OpenWindow(config.eProDocName) # Open PDF Doc (Must be at 100%)
    time.sleep(0.5)
    pya.hotkey('ctrl', 'f') # Find
    time.sleep(0.5)
    keyboard.write(pc.paste() + "\n") # Puts in Req ID and paste it (with enter)
    time.sleep(2) # Wait for box to load
    try:
        NoMatches = pya.locateOnScreen(fr'{config.CurrentPath}\NoMatches.png',confidence=0.9) # Tries to look for the No Matches box
        print(f"No SR for {ReqID}") # If error didn't occur above, no SR was found
        pya.press('enter') # enters outta box
        time.sleep(0.5)
        return "No SR"
    except:
        print("SR Found") # If no box was found, SR is there
        cb.copy(f"{ReqID} SR Found") # In order to prevent it from doing N/A in the next spots  
        return "SR Found"