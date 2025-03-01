from PyPDF2 import PdfReader
import pyautogui as pya
import keyboard as kb
from time import sleep
import os, threading, Tools.BrowserControl
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# Function that makes a text-readable PDF document
def PrepareAdobePDFFile(PDFPath,CurrentPath):
    # Function that checks if the Req ID is in the document
    def OpenInvoice():
        os.system(f'"{PDFPath}"') # Doing it alone will cause issues
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
            pya.locateOnScreen(f"{CurrentPath}\\..\\Acrobat Images\\in this fear.png") # signified by In This File
            sleep(0.1) # If it's still on screen, we wait
        except:
            break # else the scan is finished

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
        for page in Reader.pages: # Goes through each page of document
            TextGathered += page.extract_text() # Stores all text from the page
        if TextGathered == "": # if no text was gather
            PrepareAdobePDFFile(PDFPath,CurrentPath) # Perform text recognition in adobe
            # Redo
            Reader = PdfReader(PDFPath)
            for page in Reader.pages: 
                TextGathered += page.extract_text()     
            print("PDF is now text-readable by PyPDF!" if TextGathered != "" else "Mission Failed.")
    elif Method == "Online":
        TextGathered = OnlineOCR(PDFPath)
        Tools.BrowserControl.eQuestMainPage()
    
    if ShowText:
        print(f"{TextGathered}\n\nReview above text")
    
    if TextGathered == "":
        exit("Fail")
    return TextGathered