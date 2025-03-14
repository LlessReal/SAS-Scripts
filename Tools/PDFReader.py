from PyPDF2 import PdfReader
import pyautogui as pya
import keyboard as kb
from time import sleep
import os, threading, Tools.BrowserControl
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pygetwindow as gw

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys # Needed for sending keys


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


def NewOCR(Document):
    AllOCRText = ""
    Tools.BrowserControl.driver.get("https://www.newocr.com/")
    Tools.BrowserControl.CommitActionOnElement("//input[@id='userfile']",Document)
    Tools.BrowserControl.driver.find_element(By.XPATH, "//button[@id='preview']").click() 
    Tools.BrowserControl.CommitActionOnElement("//button[@id='ocr']","ClickElement") 
    # Go through each page
    pagenumdropdown = Select(Tools.BrowserControl.driver.find_element(By.XPATH, "//select[@id='page']"))
    OptionsList = [dropdownoption.text for dropdownoption in pagenumdropdown.options]
    for option in OptionsList: 
        pagenumdropdown = Select(Tools.BrowserControl.driver.find_element(By.XPATH, "//select[@id='page']"))
        pagenumdropdown.select_by_visible_text(option); sleep(15)
        Tools.BrowserControl.CommitActionOnElement("//button[@id='ocr']","ClickElement") 
        AllOCRText += Tools.BrowserControl.CommitActionOnElement("//textarea[@id='ocr-result']","Grab Text") 
    return AllOCRText


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