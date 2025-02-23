import pyautogui as pya
import clipboard as cb 
import OtherFunctions, config, keyboard, time

def CheckForSr(ReqID):
    OtherFunctions.OpenWindow(config.eProDocName) # Open PDF Doc (Must be at 100%)
    pya.hotkey('ctrl', 'f') # Find
    keyboard.write(ReqID + "\n") # Puts in Req ID and paste it (with enter)
    time.sleep(1)
    NoMatches = pya.locateOnScreen(fr'{config.CurrentPath}\NoMatches.png',confidence=0.9) # Tries to look for the No Matches box
    try:
        print(f"No SR for {ReqID}") # If error didn't occur above, no SR was found
        pya.press('enter') # enters outta box
        return "No SR"
    except:
        print("SR Found") # If no box was found, SR is there
        cb.copy(f"{ReqID} SR Found") # In order to prevent it from doing N/A in the next spots  
        return "SR Found"