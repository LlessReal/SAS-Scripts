import time, pyautogui,keyboard, pyautogui
import BrowserOpening
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys # Needed for sending keys

# Put SR Number in the search
def SearchSRNum(SRNum):    
    # Send SR Number to search box
    time.sleep(5)
    eQuestSearchBox = BrowserOpening.driver.find_element(By.XPATH, "//input[@id='search-input']") 
    eQuestSearchBox.click()
    time.sleep(1)
    # Would do the same thing but that didn't work.
    BrowserOpening.actions.send_keys(SRNum)
    BrowserOpening.actions.perform()
    print("Sent SR Number")
    BrowserOpening.wait.until(EC.presence_of_element_located((By.CLASS_NAME,"results-list"))) # Wait for page to load.
    ResultsList = BrowserOpening.driver.find_element(By.CLASS_NAME,"results-list")
    while ResultsList.text.replace(" ","") == "": # Wait until results show
        ResultsList = BrowserOpening.driver.find_element(By.CLASS_NAME,"results-list")
        pass
    print("Found Results List")
    BrowserOpening.actions.send_keys("\n") # Press enter to go to page.
    BrowserOpening.actions.perform()
    BrowserOpening.wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Details']"))) # Wait for page to load.
    time.sleep(2)

# Function to select from drop down request in eQuest
def eQuestDropDownSelect():
    BrowserOpening.actions.send_keys(Keys.ARROW_DOWN)
    BrowserOpening.actions.perform()
    time.sleep(0.5)
    BrowserOpening.actions.send_keys(Keys.ENTER)
    BrowserOpening.actions.perform()

# Pretty much the last function of the program, attach the pdf
def AttachPDF(PDFFilePath,SRNum,FullSRNum):
    # Press Details Box
    DetailsBox = BrowserOpening.driver.find_element(By.XPATH, "//span[text()='Details']") 
    DetailsBox.click()
    BrowserOpening.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Attachments']")))
    time.sleep(1)

    # Press Attachment Button
    AttachmentButton = BrowserOpening.driver.find_element(By.XPATH, "//button[text()='Attachments']") 
    AttachmentButton.click()
    BrowserOpening.wait.until(EC.presence_of_element_located((By.ID, "file_to_upload")))
    time.sleep(1)

    # Gets drop box
    PDFDropBox = BrowserOpening.driver.find_element(By.XPATH, "//input[@type='file'")
    # Perform the drag and drop action
    PDFDropBox.send_keys(PDFFilePath)
    BrowserOpening.wait.until(EC.presence_of_element_located((By.XPATH, f"//span[text()='{FullSRNum}']")))
    time.sleep(1)

    # Click close button
    CloseButton = BrowserOpening.driver.find_element(By.XPATH, "//button[text()='Close']") 
    CloseButton.click()
    time.sleep(1)

    # Click Activity Box
    ActivityBox = BrowserOpening.driver.find_element(By.XPATH, "//span[text()='Activity']") 
    ActivityBox.click()
    time.sleep(1)

    # Get Support Person's Name
    SupportPersonBox = BrowserOpening.driver.find_element(By.XPATH, "//div[@field-label='Support Person']") 
    SupportPersonBoxContents = SupportPersonBox.text
    SupportPersonName = SupportPersonBoxContents.replace("Support Person","").replace(" ","")

    # Click Log Activity Box
    LogActivityBox = BrowserOpening.driver.find_element(By.XPATH, "//button[text()='Log Activity']") 
    LogActivityBox.click()
    BrowserOpening.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='eventcombo-ui']")))
    time.sleep(1)
    
    # Type Internal Input
    ActionType = BrowserOpening.driver.find_element(By.XPATH, "//input[@id='eventcombo-ui']") 
    ActionType.send_keys("_Internal Update_")
    time.sleep(2)
    eQuestDropDownSelect()

    # Put in the input for Support Person
    BrowserOpening.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
    time.sleep(1)
    SupportPersonInput = BrowserOpening.driver.find_element(By.XPATH, "//input[@type='text']") 
    SupportPersonInput.send_keys(SupportPersonName)
    time.sleep(10)
    eQuestDropDownSelect()
    time.sleep(10)
    SendEmailBox = BrowserOpening.driver.find_element(By.XPATH, "//button[text()='Send Email & Finish']") 
    SendEmailBox.click()
    time.sleep(5)

    # Send EMail
    EmailMessageBox = BrowserOpening.driver.find_element(By.XPATH, "//body[@id='tinymce']") 
    EmailMessageBox.send_keys(f"Hello, {SupportPersonName}. Please see the Aramark invoice for {SRNum} attached for payment processing.\n\nThanks,\nJay")
    time.sleep(5)

    # Press the finish button
    FinishBox = BrowserOpening.driver.find_element(By.XPATH, "//button[text()='Finish']") 
    FinishBox.click()
    time.sleep(2)
    
    # Click ReopenButton
    ReopenButton = BrowserOpening.driver.find_element(By.XPATH, "//button[text()='Reopen']") 
    ReopenButton.click()

    # Make a comment/ Reopen Message
    BrowserOpening.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@id='comment']")))
    time.sleep(1)
    ReopenMessage = BrowserOpening.driver.find_element(By.XPATH, "//textarea[@id='comment']") 
    ReopenMessage.send_keys("Ready For Processing.")
    time.sleep(0.5)

    # Press the finish button
    FinishBox = BrowserOpening.driver.find_element(By.XPATH, "//button[text()='Finish']") 
    FinishBox.click()
    time.sleep(2)

    # Doneso
    BrowserOpening.eQuestMainPage()