from PyPDF2 import PdfReader
import pyautogui as pya
import keyboard as kb
from time import sleep
import os, threading, Tools.BrowserControl
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pygetwindow as gw


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


def NewOCR(AramarkInvoice):
    Tools.BrowserControl.driver.get("https://www.newocr.com/")
    Tools.BrowserControl.CommitActionOnElement("//input[@id='userfile']",AramarkInvoice)
    
    Tools.BrowserControl.driver.find_element(By.XPATH, "//button[@id='preview']").click() 
    Tools.BrowserControl.CommitActionOnElement("//button[@id='ocr']","ClickElement") 
    
    return Tools.BrowserControl.CommitActionOnElement("//textarea[@id='ocr-result']","Grab Text") 


def GetPDFText(PDFPath,Method,ShowText=False,CurrentPath=""):
    print("Grabbing text from documents...")
    TextGathered = ""
    if Method == "Adobe":
        Reader = PdfReader(PDFPath) # Gets pdf file
        # Goes through each page of document # Stores all text from the page
        for page in Reader.pages: TextGathered += page.extract_text() 
        if TextGathered == "": # if no text was gather
            while TextGathered == "": # Spam extract until TextGathered doesn't equal "" anymore
                Reader = PdfReader(PDFPath)
                for page in Reader.pages: TextGathered += page.extract_text() 
                sleep(1)    
        print("PDF is now text-readable by PyPDF!" if TextGathered != "" else "Mission Failed.")
    elif Method == "OnlineOCR": TextGathered = OnlineOCR(PDFPath)
    elif Method == "NewOCR": TextGathered = NewOCR(PDFPath)
    
    if ShowText: print(f"{TextGathered}\n\nReview above text")
    
    if TextGathered == "": exit("Fail")
    return TextGathered