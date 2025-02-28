import config, time, re, BrowserControl, os
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

def OnlineOCR(AramarkInvoice):
    BrowserControl.driver.get("https://www.onlineocr.net/")
    BrowserControl.CommitActionOnElement("//input[@id='fileupload']",f"{config.CurrentPath}\\Aramark Invoices\\{AramarkInvoice}")

    # Select box (no wait)
    select = Select(BrowserControl.driver.find_element(By.XPATH, "//select[@id='MainContent_comboOutput']"))
    select.select_by_visible_text('Text Plain (txt)')

    # Convert (No wait)
    ConvertButton = BrowserControl.driver.find_element(By.XPATH, "//input[@id='MainContent_btnOCRConvert']") 
    ConvertButton.click()

    # Getting Output text
    return BrowserControl.CommitActionOnElement("//textarea[@id='MainContent_txtOCRResultText']","Grab Text")
 
AllTextFromInvoice = OnlineOCR(config.AramarkInvoices[0])
print(AllTextFromInvoice)
All6DigitNums = re.findall(r'3\d{5}', AllTextFromInvoice)
print(All6DigitNums)
# we got an SR Number
SRNum = f"{All6DigitNums[0]}"
TrueSRNum = f"SR{All6DigitNums[0]}"
print(f"{SRNum} is the SR Number")
AllAfterSR = AllTextFromInvoice[AllTextFromInvoice.find(SRNum):]
FullSRName = "SR" + AllAfterSR[0:AllAfterSR.find(" ")]
print(f"{FullSRName} is the full SR name (maybe), file will be renamed to that.")
os.rename(f"{config.CurrentPath}\\Aramark Invoices\\SKM.pdf",f"{config.CurrentPath}\\Aramark Invoices\\{FullSRName}.pdf")