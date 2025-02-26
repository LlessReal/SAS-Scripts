from PyPDF2 import PdfReader
import pyautogui as pya
import keyboard as kb
from time import sleep
import os, threading, re, eQuestBrowsing, config, MyCSUAutoLogin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


wait = WebDriverWait(MyCSUAutoLogin.driver,300)
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
    MyCSUAutoLogin.driver.get("https://www.onlineocr.net/")
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='fileupload']")))
    sleep(1)
    FileDrop = MyCSUAutoLogin.driver.find_element(By.XPATH, "//input[@id='fileupload']") 
    FileDrop.send_keys(f"{config.CurrentPath}\\Aramark Invoices\\{AramarkInvoice}")

    # Select box (no wait)
    select = Select(MyCSUAutoLogin.driver.find_element(By.XPATH, "//select[@id='MainContent_comboOutput']"))
    select.select_by_visible_text('Text Plain (txt)')

    # Convert (No wait)
    ConvertButton = MyCSUAutoLogin.driver.find_element(By.XPATH, "//input[@id='MainContent_btnOCRConvert']") 
    ConvertButton.click()

    # Getting Output text
    wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@id='MainContent_txtOCRResultText']")))
    OutputArea = MyCSUAutoLogin.driver.find_element(By.XPATH, "//textarea[@id='MainContent_txtOCRResultText']") 
    return OutputArea.text

def GetPDFText(AramarkInvoice,Method):
    TextGathered = ""
    if Method == "Adobe":
        Reader = PdfReader(f"{config.CurrentPath}\\Aramark Invoices\\{AramarkInvoice}") # Gets pdf file
        for page in Reader.pages: # Goes through each page of document
            TextGathered += page.extract_text() # Stores all text from the page intos AllTextFromDoc
        if TextGathered == "":
            PrepareAdobePDFFile(AramarkInvoice)
            # Redo
            Reader = PdfReader(f"{config.CurrentPath}\\Aramark Invoices\\{AramarkInvoice}") # Gets pdf file
            for page in Reader.pages: # Goes through each page of document
                TextGathered += page.extract_text() # Stores all text from the page intos AllTextFromDoc      
            print("PDF is now text-readable by PyPDF!" if TextGathered != "" else "Mission Failed.")
    elif Method == "Online":
        return OnlineOCR(AramarkInvoice)

# Make the PDF File
def ReadFiles():
    AllTextFromInvoice = "" # Extract text from each page
    for AramarkInvoice in config.AramarkInvoices: # Goes through each document in the list of documents you placed
        AllTextFromInvoice = GetPDFText(AramarkInvoice,config.PDFRecognitionMethod)
        if AllTextFromInvoice == "":
            exit("Fail")

            
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