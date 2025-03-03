from PyPDF2 import PdfReader
import pyautogui as pya
import keyboard as kb
from time import sleep
import os, threading, Tools.BrowserControl
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
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

def OnlineOCR(AramarkInvoice):
    Tools.BrowserControl.driver.get("https://www.onlineocr.net/")
    Tools.BrowserControl.CommitActionOnElement("//input[@id='fileupload']",AramarkInvoice)

    # Select box (no wait)
    select = Select(Tools.BrowserControl.driver.find_element(By.XPATH, "//select[@id='MainContent_comboOutput']"))
    select.select_by_visible_text('Text Plain (txt)')

    # Convert (No wait)
    ConvertButton = Tools.BrowserControl.driver.find_element(By.XPATH, "//input[@id='MainContent_btnOCRConvert']") 
    ConvertButton.click()

    # Getting Output text
    return Tools.BrowserControl.CommitActionOnElement("//textarea[@id='MainContent_txtOCRResultText']","Grab Text")

def GetPDFText(PDFPath,Method,ShowText=False,CurrentPath=""):
    print("Grabbing text from documents...")
    TextGathered = ""
    if Method == "Adobe":
        Reader = PdfReader(PDFPath) # Gets pdf file
        # Goes through each page of document # Stores all text from the page
        for page in Reader.pages: TextGathered += page.extract_text() 
        if TextGathered == "": # if no text was gather
            PrepareAdobePDFFile(PDFPath,CurrentPath) # Perform text recognition in adobe
            while TextGathered == "": # Spam extract until TextGathered doesn't equal "" anymore
                Reader = PdfReader(PDFPath)
                for page in Reader.pages: TextGathered += page.extract_text() 
                sleep(1)    
        print("PDF is now text-readable by PyPDF!" if TextGathered != "" else "Mission Failed.")
    elif Method == "Online": TextGathered = OnlineOCR(PDFPath)
    
    if ShowText: print(f"{TextGathered}\n\nReview above text")
    
    if TextGathered == "": exit("Fail")
    return TextGathered