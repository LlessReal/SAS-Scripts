import pyautogui
import time, os
import keyboard
import tkinter as tk
from tkinter import messagebox
import pyperclip
import pygetwindow as gw

root = tk.Tk() # Creates main window
root.wait_visibility() # Wait until the label becomes visible
root.geometry("240x75") # Sets the window size

PhoneNumberLabel = tk.Label(root, text = "Phone Number")
PhoneNumberLabel.grid(row=0,column=0)   
PhoneNumberTyped = tk.StringVar()
PhoneNumberEntry = tk.Entry(root, textvariable = PhoneNumberTyped)
PhoneNumberEntry.grid(row=0,column=1)   
root.withdraw()

CurrentPath = os.path.dirname(__file__) # Gonna need this

def ShowTkinterWindow():
    root.deiconify()
    PhoneNumberTyped.set(pyperclip.paste())
    PhoneNumberEntry.icursor(tk.END)
    PhoneNumberEntry.focus()
    Window = gw.getWindowsWithTitle("tk")[0] # Goes back to Excel Sheet
    if Window.isMinimized: # If the window is minimized
        Window.restore() # Unminimizes it
    Window.activate()  # Activates the window


def AutoTransfer(TransferNumber):
    IcebarDropDownArrow = pyautogui.locateOnScreen(fr"{CurrentPath}\..\IceBarImages\Icebardropdownarrow.png") # Can do directories as well btw
    InitialPosition = pyautogui.position()
    pyautogui.click(IcebarDropDownArrow) # Click the button        

    try:
        transferbutton = pyautogui.locateOnScreen(fr"{CurrentPath}\..\IceBarImages\TransferButton.png") # Finds transfer button, if it's not on screen, goes to except
        pyautogui.click(transferbutton) # Click the button
    except:
        print("You're not in a call.") 
        pyautogui.click(transferbutton) # Clicks again to close
        pyautogui.moveTo(InitialPosition) # Go to OG position
        return # Ends function
    # Tries to find initiate transfer button to see if we should type info or not
    for i in range(10):
        try:
            InitiateTransferButton = pyautogui.locateOnScreen(fr"{CurrentPath}\..\IceBarImages\InitiateTransferButton.png") # Checks if the 2nd window after you press transfer is up
            keyboard.write(f"{TransferNumber} \n") # Types number and then press enter
            break
        except:
            print("Couldn't find the initiate transfer button, retrying")
            time.sleep(1)
            if i == 9: # If 10 seconds passed and transfer still not complete
                print("Failed operation. PC too laggy") 
                pyautogui.moveTo(InitialPosition) 
                return
        
    print("Transfer Successful!")
    pyautogui.moveTo(InitialPosition) # End

def InitiateAutoTransfer(event):
    root.withdraw()
    theNumber = PhoneNumberEntry.get()
    if theNumber == "":
        print("Put in a number idiot.")
        return 
    AutoTransfer(theNumber)
    
PhoneNumberEntry.bind("<Return>", InitiateAutoTransfer)
print("ctrl+f1 to start")
keyboard.add_hotkey("ctrl+f1", ShowTkinterWindow)
root.mainloop() # Keeps the Tkinter event loop running to make gui elements work right
keyboard.wait()



