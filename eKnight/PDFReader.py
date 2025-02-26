from PyPDF2 import PdfReader
import pyautogui as pya
import keyboard as kb
from time import sleep
import os, threading, re, eQuestBrowsing, config

# Function that makes a text-readable PDF document
def PreparePDFFile(AramarkInvoice):
    # Function that checks if the Req ID is in the document
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
def ReadFiles():
    AllTextFromInvoice = "" # Extract text from each page
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
        for DigitNum in All6DigitNums: 
            if DigitNum.startswith("3"):
                SRNum = AllTextFromInvoice[AllTextFromInvoice.find(DigitNum) - 2:AllTextFromInvoice.find(DigitNum) + 8]
                print(f"{SRNum} is the SR Number so far")
        if SRNum == "":
            print("We got nothin")
            os.rename(f"{config.CurrentPath}\\Aramark Invoices\\{AramarkInvoice}",f"{config.CurrentPath}\\Aramark Invoices\\Failure\\{FullSRNameIG}.pdf")
            continue
        else: # If we got an SR Number
            print(f"{SRNum} is the SR Number")
            AllAfter = AllTextFromInvoice[AllTextFromInvoice.find(SRNum):]
            FullSRNameIG = AllAfter[:AllAfter.find("\n")]
            print(f"{FullSRNameIG} is the almost full SR name, file will be renamed to that.")
            os.rename(f"{config.CurrentPath}\\Aramark Invoices\\{AramarkInvoice}",f"{config.CurrentPath}\\Aramark Invoices\\{FullSRNameIG}.pdf")
            eQuestBrowsing.SearchSRNum(SRNum)
            eQuestBrowsing.AttachPDF(f"{config.CurrentPath}\\Aramark Invoices\\{FullSRNameIG}.pdf",SRNum,f"{FullSRNameIG}.pdf")
            print("We did it !! - Dora")
            os.rename(f"{config.CurrentPath}\\Aramark Invoices\\{AramarkInvoice}",f"{config.CurrentPath}\\Aramark Invoices\\Successfully Sent\\{FullSRNameIG}.pdf")