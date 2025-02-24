import clipboard as cb 
import config
from PyPDF2 import PdfReader
import os
import pyautogui as pya
import keyboard as kb
import threading
from time import sleep
import re


# Function that checks if the Req ID is in the document
def CheckForSRNum():
    if AramarkInvoice.find("SR") == -1: # If the ID wasn't found in the text
        print(f"No SR Number detected") # If error didn't occur above, no SR was found
        return "No SR"
    else:
        return "SR Found"
    
AllTextFromInvoice = "" # Extract text from each page

# Function that makes a text-readable PDF document
def PreparePDFFile(AramarkInvoice):
    def OpenInvoice():
        os.system(f'"{config.CurrentPath}\\Aramark Invoices\\{AramarkInvoice}"') # Doing it alone will cause issues
    PDFOpeningThread = threading.Thread(target=OpenInvoice)
    PDFOpeningThread.start() # Opens file as a thread so that entire code won't be halted
    sleep(2) # Wait for doc to load
    pya.hotkey("ctrl","f")
    sleep(0.5) # Wait for find box to load
    kb.write("Recognize Text")
    sleep(2) # Wait for popup box thing to glitch out for zero fucking reason
    pya.hotkey("ctrl","f") # Reopen that shit
    sleep(0.5) # Wait a bit
    pya.press("down")
    pya.press("enter") # Select the Recognize Text
    sleep(1) # Wait for engine to load
    for i in range(5):  
        pya.press("tab")
        sleep(0.1) # Tab down to Recognize Text
    pya.press("enter") # Select it
    pya.hotkey("ctrl","s") # Saves
    pya.hotkey("alt","f4") # and leave (bot will both process after scan finishes so kickass)
    while True: # Wait for scan to be done
        try:
            pya.locateOnScreen(f"{config.CurrentPath}\\Acrobat Images\\in this fear.png") # signified by In This File
            sleep(0.1) # If it's still on screen, we wait
        except:
            break # else the scan is finished

# Make the PDF File
for AramarkInvoice in config.AramarkInvoices: # Goes through each document in the list of documents you placed
    Reader = PdfReader(f"{config.CurrentPath}\\Aramark Invoices\\{AramarkInvoice}") # Gets pdf file
    for page in Reader.pages: # Goes through each page of document
        AllTextFromInvoice += page.extract_text() # Stores all text from the page intos AllTextFromDoc
    if AllTextFromInvoice == "":
        PreparePDFFile(AramarkInvoice)
        # Redo
        Reader = PdfReader(f"{config.CurrentPath}\\Aramark Invoices\\{AramarkInvoice}") # Gets pdf file
        for page in Reader.pages: # Goes through each page of document
            AllTextFromInvoice += page.extract_text() # Stores all text from the page intos AllTextFromDoc      
        print("PDF is now text-readable by PyPDF!" if AllTextFromInvoice != "" else "Mission Failed.")

    # Find all 6 digit numbers in the document
    All6DigitNums = re.findall(r'\d{6}', AllTextFromInvoice)
    SRNum = ""
    if "SR" in AllTextFromInvoice:
        SRNum = AllTextFromInvoice[AllTextFromInvoice.find("SR"):AllTextFromInvoice.find("SR") + 8]
    else:
        for DigitNum in All6DigitNums: 
            if DigitNum.startswith("3"):
                SRNum = DigitNum
                print(f"{SRNum} is the SR Number so far")
    if SRNum == "":
        print("We got nothin")
    else:
        print(f"{SRNum} is the SR Number")
        AllAfter = AllTextFromInvoice[AllTextFromInvoice.find(SRNum):]
        FullSRNameIG = AllAfter[:AllAfter.find("\n")]
        print(f"{FullSRNameIG} is the almost full SR name, file will be renamed to that.")
        os.rename(f"{config.CurrentPath}\\Aramark Invoices\\{AramarkInvoice}",f"{config.CurrentPath}\\Aramark Invoices\\{FullSRNameIG}.pdf")


    #input("")
    #os.rename(f"{config.CurrentPath}\\Aramark Invoices\\{AramarkInvoiceDoc}",f"{config.CurrentPath}\\Aramark Invoices\\Successfully Sent\\{FullSRName}.pdf")
    #CheckForSRNum()