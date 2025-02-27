from PyPDF2 import PdfReader
import pyautogui as pya
import keyboard as kb
from time import sleep
import os, threading, re, eQuestBrowsing, config, BrowserControl
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# Function that makes a text-readable PDF document
def PrepareAdobePDFFile(AramarkInvoice):
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

def OnlineOCR(AramarkInvoice):
    wait = WebDriverWait(BrowserControl.driver,300)
    BrowserControl.driver.get("https://www.onlineocr.net/")
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='fileupload']")))
    sleep(1)
    FileDrop = BrowserControl.driver.find_element(By.XPATH, "//input[@id='fileupload']") 
    FileDrop.send_keys(f"{config.CurrentPath}\\Aramark Invoices\\{AramarkInvoice}")

    # Select box (no wait)
    select = Select(BrowserControl.driver.find_element(By.XPATH, "//select[@id='MainContent_comboOutput']"))
    select.select_by_visible_text('Text Plain (txt)')

    # Convert (No wait)
    ConvertButton = BrowserControl.driver.find_element(By.XPATH, "//input[@id='MainContent_btnOCRConvert']") 
    ConvertButton.click()

    # Getting Output text
    wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@id='MainContent_txtOCRResultText']")))
    OutputArea = BrowserControl.driver.find_element(By.XPATH, "//textarea[@id='MainContent_txtOCRResultText']") 
    return OutputArea.text

def GetPDFText(AramarkInvoice,Method):
    print("Grabbing text from documents...")
    TextGathered = ""
    if Method == "Adobe":
        Reader = PdfReader(f"{config.CurrentPath}\\Aramark Invoices\\{AramarkInvoice}") # Gets pdf file
        for page in Reader.pages: # Goes through each page of document
            TextGathered += page.extract_text() # Stores all text from the page intos AllTextFromDoc
        if TextGathered == "": # if no text was gather
            PrepareAdobePDFFile(AramarkInvoice) # Perform text recognition in adobe
            # Redo
            Reader = PdfReader(f"{config.CurrentPath}\\Aramark Invoices\\{AramarkInvoice}") # Gets pdf file
            for page in Reader.pages: # Goes through each page of document
                TextGathered += page.extract_text() # Stores all text from the page intos AllTextFromDoc      
            print("PDF is now text-readable by PyPDF!" if TextGathered != "" else "Mission Failed.")
    elif Method == "Online":
        TextGathered = OnlineOCR(AramarkInvoice)
        BrowserControl.eQuestMainPage()
    
    if TextGathered == "":
        exit("Fail")
    return TextGathered

# Get the SR Number
def ReadFiles():
    AllTextFromInvoice = "" # Extract text from each page
    if config.PDFRecognitionMethod != "Testing": # If we're not testing
        for AramarkInvoice in config.AramarkInvoices: # Goes through each document in the list of documents you placed
            # Get the text from PDF
            AllTextFromInvoice = GetPDFText(AramarkInvoice,config.PDFRecognitionMethod)
            # Find all 6 digit numbers that starts with 3 in the document
            All6DigitNums = re.findall(r'3\d{5}', AllTextFromInvoice)
            print(f"All 6 Digit Numbers that start with 3: {All6DigitNums}")
            for Num in All6DigitNums: # Go through each 3 digit number
                if AllTextFromInvoice[AllTextFromInvoice.find(Num):7].isdigit(): # If it's some different number
                    All6DigitNums.remove(Num) 
            print(f"Cleaned list without unrelated numbers: {All6DigitNums}")
            if All6DigitNums == []:
                print("We got nothin")
                os.rename(f"{config.CurrentPath}\\Aramark Invoices\\{AramarkInvoice}",f"{config.CurrentPath}\\Aramark Invoices\\Failure\\{FullSRName}.pdf")
                continue
            else:
                # we got an SR Number
                SRNum = f"{All6DigitNums[0]}"
                TrueSRNum = f"SR{All6DigitNums[0]}"
                print(f"{TrueSRNum} is the SR Number")
                AllAfterSR = AllTextFromInvoice[AllTextFromInvoice.find(SRNum):]
                FullSRName = "SR" + AllAfterSR[0:AllAfterSR.find(" ")]
                print(f"{FullSRName} is the full SR name (maybe), file will be renamed to that.")
                os.rename(f"{config.CurrentPath}\\Aramark Invoices\\{AramarkInvoice}",f"{config.CurrentPath}\\Aramark Invoices\\{FullSRName}.pdf")
                eQuestBrowsing.SearchSRNum(TrueSRNum)
                eQuestBrowsing.NotifySupport(f"{config.CurrentPath}\\Aramark Invoices\\{FullSRName}.pdf",TrueSRNum)
                print("We did it !! - Dora !!")
                # Put in Success folder
                os.rename(f"{config.CurrentPath}\\Aramark Invoices\\{AramarkInvoice}",f"{config.CurrentPath}\\Aramark Invoices\\Successfully Sent\\{FullSRName}.pdf")
                # Loop occurs
    else: # If we are testing
        SRNum = "SR327971"
        # No renaming
        eQuestBrowsing.SearchSRNum(SRNum)
        eQuestBrowsing.NotifySupport(f"{config.CurrentPath}\\Aramark Invoices\\SKM.pdf",SRNum)
        print("Test complete.")