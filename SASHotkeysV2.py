import pyautogui
import time
import keyboard
import tkinter as tk
from tkinter import messagebox
import pyperclip

root = tk.Tk() # Creates main window
root.wait_visibility() # Wait until the label becomes visible
root.geometry("240x75") # Sets the window size

PhoneNumberLabel = tk.Label(root, text = "Phone Number")
PhoneNumberTyped = tk.StringVar()
PhoneNumberEntry = tk.Entry(root, textvariable = PhoneNumberTyped)
PhoneNumberLabel.grid(row=0,column=0)   
PhoneNumberEntry.grid(row=0,column=1)   
root.withdraw()

def ShowTkinterWindow():
    root.deiconify()
    PhoneNumberTyped.set(pyperclip.paste())
    PhoneNumberEntry.icursor(tk.END)
    PhoneNumberEntry.focus()
    
def AutoTransfer(event):
    root.withdraw()
    theNumber = PhoneNumberEntry.get()
    if theNumber == "":
        print("Put in a number idiot.")
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
            keyboard.write(f"{theNumber} \n") # Types number and then press enter
            break
        except:
            if i == 9: # If 10 seconds passed and transfer still not complete
                print("Failed operation. PC too laggy") 
                pyautogui.moveTo(InitialPosition) 
                return
        time.sleep(1)

    print("Transfer Successful!")
    pyautogui.moveTo(InitialPosition) # End

PhoneNumberEntry.bind("<Return>", AutoTransfer)
keyboard.add_hotkey("ctrl+f1", ShowTkinterWindow)
root.mainloop() # Keeps the Tkinter event loop running to make gui elements work right
keyboard.wait()



