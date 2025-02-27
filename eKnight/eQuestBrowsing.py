import time, BrowserOpening, config
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

# Function to click,send something to, or grab text from element
# Format: Element by XPATH, Action, eQuest Drop Down or not, and if there's an alternative element or nah
def CommitActionOnElement(Element,Action,eQuestDropDown=False,AltElement="",AltAction="",SwappingToIframe=False,MessageAfterClick=""):
    if SwappingToIframe:
        BrowserOpening.wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        iframe = BrowserOpening.driver.find_element(By.TAG_NAME, "iframe")  # Adjust selector
        BrowserOpening.driver.switch_to.frame(iframe)
        print(f"Swapped to Iframe!")
        time.sleep(1)

    BrowserOpening.wait.until(EC.presence_of_element_located((By.XPATH, Element)))
    ElementChosen = BrowserOpening.driver.find_element(By.XPATH, Element)
    print(f"{Element} found. Committing action in a sec...")
    time.sleep(1)
    if Action == "Text Grab":
        time.sleep(1)
        return ElementChosen.get_attribute("alt")
    
    if AltElement != "": # If we're dooing another element
        BrowserOpening.wait.until(EC.presence_of_element_located((By.XPATH, AltElement)))
        ElementChosen = BrowserOpening.driver.find_element(By.XPATH, AltElement)
        ElementChosen.send_keys(AltAction) if "Clicking" not in AltAction else ElementChosen.click()
        if Action == "Clicking and Inputting":
            BrowserOpening.actions.send_keys(MessageAfterClick).perform()
    else: # If regular
        ElementChosen.send_keys(Action) if "Clicking" not in Action else ElementChosen.click()
        if Action == "Clicking and Inputting":
            BrowserOpening.actions.send_keys(MessageAfterClick).perform()

    if SwappingToIframe:
        BrowserOpening.driver.switch_to.default_content()
    # If statement to turn back to main page was supposed to be here but it wasn't goddamn working for some reason
    time.sleep(1)

    if eQuestDropDown:
        BrowserOpening.actions.send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(0.5)
        BrowserOpening.actions.send_keys(Keys.ENTER).perform()
        time.sleep(1)

# Pretty much the last function of the program, attach the pdf
def NotifySupport(PDFFilePath,SRNum):
    # Attaching doc
    CommitActionOnElement("//span[text()='Details']","Clicking") # Press Details Box
    CommitActionOnElement("//button[text()='Attachments']","Clicking") # Press Attachments button
    CommitActionOnElement("//input[@id='file_to_upload']",PDFFilePath,SwappingToIframe=True) # Send file
    time.sleep(3)
    CommitActionOnElement("//button[text()='Close']","Clicking") # Send file
    
    # Getting Support Person's name
    CommitActionOnElement("//span[text()='Activity']","Clicking") # Click Activity Box
    SupportPersonName = CommitActionOnElement("//img[@class='img-circle img-avatar img-extra-data ng-scope ev-avatar']","Text Grab") # Click Activity Box
    # We're getting from the first img alt since that'll be the support person
    print(f"The support person is {SupportPersonName}")

    # Committing Log Activity
    CommitActionOnElement("//button[@ng-if='::data.form.extra.wizards.log_activity']","Clicking") 
    CommitActionOnElement("//input[@id='eventcombo-ui']","_Internal Update_",eQuestDropDown=True,SwappingToIframe=True) # Selecting Type of Message/Alert or whatever
    CommitActionOnElement("//span[@class='form_input_undefined']","Clicking and Inputting",MessageAfterClick=SupportPersonName,eQuestDropDown=True,SwappingToIframe=True) # Selecting Support Specialist as the contact
    # Sending message
    CommitActionOnElement("//button[text()='Send Email & Finish']","Clicking") # Press "Send Email & Finish"
    CommitActionOnElement("//iframe[@title='Rich Text Area']","Clicking",SwappingToIframe=True)
    BrowserOpening.actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
    with open(f"{config.CurrentPath}\\CustomTags.txt","r") as file:
        eQuestCustomTags = file.read()
    BrowserOpening.actions.send_keys(f"Hello, {SupportPersonName}. Please see the Aramark invoice for {SRNum} attached for payment processing.\n\nThanks,\nJay\n\n{eQuestCustomTags}").perform()
    time.sleep(1000) # Wait for allat to send
    CommitActionOnElement("//button[text()='Finish']","Clicking") # Press Finish Buttion
    
    # Changing the status of the ticket
    CommitActionOnElement("//button[@ng-if='::data.form.extra.wizards.hold_reopen']","Clicking") # Click Reopen Button
    CommitActionOnElement("//textarea[@id='comment']","Ready For Processing.",SwappingToIframe=True) # Make a comment / Reopen Message
    CommitActionOnElement("//button[text()='Finish']","Clicking") # Press the finish button

    # Doneso
    BrowserOpening.eQuestMainPage()