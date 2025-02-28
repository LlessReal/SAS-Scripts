import time, BrowserControl, config
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys # Needed for sending keys

# Put SR Number in the search
def SearchSRNum(TrueSRNum):    
    # Send SR Number to search box
    BrowserControl.CommitActionOnElement("//input[@id='search-input']","Clicking and Inputting",MessageAfterClick=TrueSRNum,SuccessMessage="Sent SR Number") # Press Details Box
    BrowserControl.wait.until(EC.presence_of_element_located((By.CLASS_NAME,"results-list"))) # Wait for page to load.
    print("Found Results List")
    time.sleep(1)
    ResultsList = BrowserControl.driver.find_element(By.CLASS_NAME,"results-list")
    while ResultsList.text.replace(" ","") == "": # Wait until results show
        ResultsList = BrowserControl.driver.find_element(By.CLASS_NAME,"results-list")
        pass
    BrowserControl.actions.send_keys("\n").perform() # Press enter to go to page.

# Pretty much the last function of the program, attach the pdf
def NotifySupport(PDFFilePath,SRNum):
    # Attaching doc
    BrowserControl.CommitActionOnElement("//span[text()='Details']","Clicking") # Press Details Box
    BrowserControl.CommitActionOnElement("//button[text()='Attachments']","Clicking") # Press Attachments button
    BrowserControl.CommitActionOnElement("//input[@id='file_to_upload']",PDFFilePath,SwappingToIframe=True,Delay=3) # Send file
    BrowserControl.CommitActionOnElement("//button[text()='Close']","Clicking") # Send file
    
    # Getting Support Person's name
    BrowserControl.CommitActionOnElement("//span[text()='Activity']","Clicking") # Click Activity Box
    SupportPersonName = BrowserControl.CommitActionOnElement("//img[@class='img-circle img-avatar img-extra-data ng-scope ev-avatar']","Grab Text",TypeOfItem="Support Person") # Click Activity Box
    # We're getting from the first img alt since that'll be the support person

    # Committing Log Activity
    BrowserControl.CommitActionOnElement("//button[@ng-if='::data.form.extra.wizards.log_activity']","Clicking") 
    BrowserControl.CommitActionOnElement("//input[@id='eventcombo-ui']","_Internal Update_",eQuestDropDown=True,SwappingToIframe=True) # Selecting Type of Message/Alert or whatever
    BrowserControl.CommitActionOnElement("//span[@class='form_input_undefined']","Clicking and Inputting",MessageAfterClick=SupportPersonName,eQuestDropDown=True,SwappingToIframe=True) # Selecting Support Specialist as the contact
    
    # Sending message
    BrowserControl.CommitActionOnElement("//button[text()='Send Email & Finish']","Clicking") # Press "Send Email & Finish"
    BrowserControl.CommitActionOnElement("//iframe[@title='Rich Text Area']","Clicking",SwappingToIframe=True)
    BrowserControl.actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
    eQuestCustomTags = open(f"{config.CurrentPath}\\CustomTags.txt","r").read() 
    # Putting Email Message
    BrowserControl.actions.send_keys(f"Hello, {SupportPersonName}. Please see the Aramark invoice for {SRNum} attached for payment processing.\n\nThanks,\nJay\n\n{eQuestCustomTags}").perform()
    BrowserControl.CommitActionOnElement("//button[text()='Finish']","Clicking") # Press Finish Buttion
    
    # Changing the status of the ticket
    BrowserControl.CommitActionOnElement("//button[@ng-if='::data.form.extra.wizards.hold_reopen']","Clicking") # Click Reopen Button
    BrowserControl.CommitActionOnElement("//textarea[@id='comment']","Ready For Processing.",SwappingToIframe=True) # Make a comment / Reopen Message
    BrowserControl.CommitActionOnElement("//button[text()='Finish']","Clicking") # Press the finish button

    # Doneso
    BrowserControl.eQuestMainPage()