import config, time, re
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

def BuildTextFile(AramarkInvoice):
    options = Options() # Get options
    global driver
    driver = webdriver.Chrome(options=options) # Opens Chrome browser with options (if u put any)
    driver.maximize_window() # Maxes window
    wait = WebDriverWait(driver,300)
    driver.get("https://www.onlineocr.net/")
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='fileupload']")))
    time.sleep(1)
    FileDrop = driver.find_element(By.XPATH, "//input[@id='fileupload']") 
    FileDrop.send_keys(f"{config.CurrentPath}\\Aramark Invoices\\{AramarkInvoice}")

    # Select box (no wait)
    select = Select(driver.find_element(By.XPATH, "//select[@id='MainContent_comboOutput']"))
    select.select_by_visible_text('Text Plain (txt)')

    # Convert (No wait)
    ConvertButton = driver.find_element(By.XPATH, "//input[@id='MainContent_btnOCRConvert']") 
    ConvertButton.click()

    # Getting Output text
    wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@id='MainContent_txtOCRResultText']")))
    OutputArea = driver.find_element(By.XPATH, "//textarea[@id='MainContent_txtOCRResultText']") 
    return OutputArea.text

text = BuildTextFile(config.AramarkInvoices[0])
print(text)
All6DigitNums = re.findall(r'3\d{5}', text)
print(All6DigitNums)