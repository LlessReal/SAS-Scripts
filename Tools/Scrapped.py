import pyautogui as pya
import os, threading
from time import sleep
import keyboard as kb
import pygetwindow as gw
# Function that makes a text-readable PDF document
def PrepareAdobePDFFile(PDFPath,CurrentPath):
    # Function that checks if the Req ID is in the document
    def OpenInvoice(): os.system(f'"{PDFPath}"') # Doing it alone will cause issues
    PDFOpeningThread = threading.Thread(target=OpenInvoice)
    PDFOpeningThread.start() # Opens file as a thread so that entire code won't be halted
    FileName = PDFPath[PDFPath.rfind("\\") + 1:]
    while True:
        try:
            window = gw.getWindowsWithTitle(FileName)[0] # Gets the 1st window of the window name
            sleep(2) # Wait a bit, activate wont work for some retarded reason
            break
        except IndexError: continue
    pya.hotkey("ctrl","f")
    sleep(0.5) # Wait for find box to load
    kb.write("Recognize Text")
    sleep(2) # Wait for popup box thing to glitch out for zero fucking reason
    pya.hotkey("ctrl","f") # Reopen that shit
    sleep(0.5) # Wait a bit
    pya.press("down")
    pya.press("enter") # Select the Recognize Text
    sleep(2) # Wait for engine to load
    for i in range(5):  
        pya.press("tab")
        sleep(0.1) # Tab down to Recognize Text
    pya.press("enter") # Select it
    pya.hotkey("ctrl","s") # Saves
    pya.hotkey("alt","f4") # and leave (bot will both process after scan finishes so kickass)
# simply inefficient