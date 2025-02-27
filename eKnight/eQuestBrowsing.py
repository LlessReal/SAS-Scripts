import time, BrowserControl, config
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys # Needed for sending keys

# Put SR Number in the search
def SearchSRNum(TrueSRNum):    
    # Send SR Number to search box
    time.sleep(5)
    eQuestSearchBox = BrowserControl.driver.find_element(By.XPATH, "//input[@id='search-input']") 
    eQuestSearchBox.click()
    time.sleep(1)
    # Would do the same thing but that didn't work.
    BrowserControl.actions.send_keys(TrueSRNum)
    BrowserControl.actions.perform()
    print("Sent SR Number")
    BrowserControl.wait.until(EC.presence_of_element_located((By.CLASS_NAME,"results-list"))) # Wait for page to load.
    ResultsList = BrowserControl.driver.find_element(By.CLASS_NAME,"results-list")
    while ResultsList.text.replace(" ","") == "": # Wait until results show
        ResultsList = BrowserControl.driver.find_element(By.CLASS_NAME,"results-list")
        pass
    print("Found Results List")
    BrowserControl.actions.send_keys("\n") # Press enter to go to page.
    BrowserControl.actions.perform()
    BrowserControl.wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Details']"))) # Wait for page to load.
    time.sleep(2)

# Function to click,send something to, or grab text from element
# Format: Element by XPATH, Action, eQuest Drop Down or not, and if there's an alternative element or nah

# Pretty much the last function of the program, attach the pdf
def NotifySupport(PDFFilePath,SRNum):
    # Attaching doc
    BrowserControl.CommitActionOnElement("//span[text()='Details']","Clicking") # Press Details Box
    BrowserControl.CommitActionOnElement("//button[text()='Attachments']","Clicking") # Press Attachments button
    BrowserControl.CommitActionOnElement("//input[@id='file_to_upload']",PDFFilePath,SwappingToIframe=True) # Send file
    time.sleep(3)
    BrowserControl.CommitActionOnElement("//button[text()='Close']","Clicking") # Send file
    
    # Getting Support Person's name
    BrowserControl.CommitActionOnElement("//span[text()='Activity']","Clicking") # Click Activity Box
    SupportPersonName = BrowserControl.CommitActionOnElement("//img[@class='img-circle img-avatar img-extra-data ng-scope ev-avatar']","Text Grab") # Click Activity Box
    # We're getting from the first img alt since that'll be the support person
    print(f"The support person is {SupportPersonName}")

    # Committing Log Activity
    BrowserControl.CommitActionOnElement("//button[@ng-if='::data.form.extra.wizards.log_activity']","Clicking") 
    BrowserControl.CommitActionOnElement("//input[@id='eventcombo-ui']","_Internal Update_",eQuestDropDown=True,SwappingToIframe=True) # Selecting Type of Message/Alert or whatever
    BrowserControl.CommitActionOnElement("//span[@class='form_input_undefined']","Clicking and Inputting",MessageAfterClick=SupportPersonName,eQuestDropDown=True,SwappingToIframe=True) # Selecting Support Specialist as the contact
    # Sending message
    BrowserControl.CommitActionOnElement("//button[text()='Send Email & Finish']","Clicking") # Press "Send Email & Finish"
    BrowserControl.CommitActionOnElement("//iframe[@title='Rich Text Area']","Clicking",SwappingToIframe=True)
    BrowserControl.actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
    with open(f"{config.CurrentPath}\\CustomTags.txt","r") as file:
        eQuestCustomTags = file.read()
    BrowserControl.actions.send_keys(f"Hello, {SupportPersonName}. Please see the Aramark invoice for {SRNum} attached for payment processing.\n\nThanks,\nJay\n\n{eQuestCustomTags}").perform()
    time.sleep(1000) # Wait for allat to send
    BrowserControl.CommitActionOnElement("//button[text()='Finish']","Clicking") # Press Finish Buttion
    
    # Changing the status of the ticket
    BrowserControl.CommitActionOnElement("//button[@ng-if='::data.form.extra.wizards.hold_reopen']","Clicking") # Click Reopen Button
    BrowserControl.CommitActionOnElement("//textarea[@id='comment']","Ready For Processing.",SwappingToIframe=True) # Make a comment / Reopen Message
    BrowserControl.CommitActionOnElement("//button[text()='Finish']","Clicking") # Press the finish button

    # Doneso
    BrowserControl.eQuestMainPage()