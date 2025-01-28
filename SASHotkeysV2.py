import pyautogui
import time
import keyboard
def on_hotkey():
    PhoneNumber = pyautogui.prompt("What's the phone number.")
    if PhoneNumber == None:
        print("Cancelled operation")
        return 
    IcebarDropDownArrow = pyautogui.locateOnScreen("Icebardropdownarrow.png") # Can do directories as well btw
    InitialPosition = pyautogui.position()
    x, y = pyautogui.center(IcebarDropDownArrow) # Get the center of the button
    pyautogui.click(x, y) # Click the button        

    try:
        transferbutton = pyautogui.locateOnScreen("transfer.png") # Finds transfer button, if it's not on screen, goes to except
        x, y = pyautogui.center(transferbutton) # Get the center of the button
        pyautogui.click(x, y) # Click the button
    except:
        print("You're not in a call.") 
        pyautogui.click(x, y) # Clicks again to close
        pyautogui.moveTo(InitialPosition) # Go to OG position
        return # Ends function

    for i in range(10):
        try:
            InputArea = pyautogui.locateOnScreen("transfer2.png") # Checks if the 2nd window after you press transfer is up
            keyboard.write(f"{PhoneNumber}") # Types number and then press enter
            break
        except:
            if i == 9: # If 10 seconds passed and transfer still not complete
                print("Failed operation. PC too laggy") 
                pyautogui.moveTo(InitialPosition) 
                return
        time.sleep(1)

    print("Transfer Successful!")
    pyautogui.moveTo(InitialPosition) # End
    

keyboard.add_hotkey("ctrl+3", on_hotkey)

print("Press CTRL+3 to activate the hotkey.")
keyboard.wait()
