import time, config, Tools.BrowserControl, main
from selenium.webdriver.common.by import By

# Search SR Number after page loads
def SearchSRNum(SRNum):   
    Tools.BrowserControl.CommitActionOnElement("//span[text()='Welcome to the Production Service Manager Technician Portal!']",SwappingToIframe=True)  
    Tools.BrowserControl.CommitActionOnElement("//input[@id='search-input']","ClickElement,InputtingElement",MessageAfterClick=f"SR{SRNum}",SuccessMessage="Sent SR Number") 
    # Wait for results list to have text/SR Numbers
    while Tools.BrowserControl.driver.find_element(By.XPATH,"//div[@class='results-list']").text.replace(" ","") == "": 
        time.sleep(0.25)
        pass
    Tools.BrowserControl.QuickPress("Enter")

# Pretty much the last function of the program, attach the pdf

# Function to attach PDF to ticket
def AttachPDFtoTicket(PDFFilePath):
    Tools.BrowserControl.CommitActionOnElement("//span[text()='Details']","ClickElement") # Press Details Box
    try:
        Tools.BrowserControl.driver.find_element("//span[text()='Closed']") # If ticket is closed ignore the ticket
        Tools.BrowserControl.eQuestMainPage()
        return "Already Closed"
    except: pass
    Tools.BrowserControl.CommitActionOnElement("//button[text()='Attachments']","ClickElement") # Press Attachments button
    Tools.BrowserControl.CommitActionOnElement("//input[@id='file_to_upload']",PDFFilePath,SwappingToIframe=True,Delay=3) # Send file
    Tools.BrowserControl.CommitActionOnElement("//button[text()='Close']","ClickElement") # Send file
    return "Success"

def NotifySupport(SRNum):   
    # Getting Support Person's name
    Tools.BrowserControl.CommitActionOnElement("//span[text()='Activity']","ClickElement") # Click Activity Box
    SupportPersonName = Tools.BrowserControl.CommitActionOnElement("//img[@class='img-circle img-avatar img-extra-data ng-scope ev-avatar']","Grab Alt Text",TypeOfItem="Support Person") # Click Activity Box
    # We're getting from the first img alt since that'll be the support person

    # Committing Log Activity
    Tools.BrowserControl.CommitActionOnElement("//button[@ng-if='::data.form.extra.wizards.log_activity']","ClickElement") 
    Tools.BrowserControl.CommitActionOnElement("//input[@id='eventcombo-ui']","_Internal Update_",eQuestDropDown=True,SwappingToIframe=True) # Selecting Type of Message/Alert or whatever
    Tools.BrowserControl.CommitActionOnElement("//span[@class='form_input_undefined']","ClickElement, InputtingElement",MessageAfterClick=SupportPersonName,eQuestDropDown=True,SwappingToIframe=True) # Selecting Support Specialist as the contact
    
    # Sending message
    Tools.BrowserControl.CommitActionOnElement("//button[text()='Send Email & Finish']","ClickElement") # Press "Send Email & Finish"
    # Putting Email Message
    eQuestCustomTags = open(f"{main.CurrentPath}\\CustomTags.txt","r").read() 
    SupportMessage = f"Hello, {SupportPersonName}. Please see the Aramark invoice for SR{SRNum} attached for payment processing.\n\nThanks,\nJay\n\n{eQuestCustomTags}"
    Tools.BrowserControl.CommitActionOnElement("//iframe[@title='Rich Text Area']","ClickElement, InputtingElement, ResetElement",SwappingToIframe=True,MessageAfterClick=SupportMessage)
    if not config.TestingProgram: Tools.BrowserControl.CommitActionOnElement("//button[text()='Finish']","ClickElement",Delay=3) # Press Finish Buttion
    else: Tools.BrowserControl.CommitActionOnElement("//button[text()='Cancel']","ClickElement",AlertBox="Accept",Delay=3)
    
    # Changing the status of the ticket
    Tools.BrowserControl.CommitActionOnElement("//button[@ng-if='::data.form.extra.wizards.hold_reopen']","ClickElement") # Click Reopen Button
    Tools.BrowserControl.CommitActionOnElement("//textarea[@id='comment']","Ready For Processing.",SwappingToIframe=True) # Make a comment / Reopen Message
    if not config.TestingProgram: Tools.BrowserControl.CommitActionOnElement("//button[text()='Finish']","ClickElement") # Press Finish Buttion
    else: Tools.BrowserControl.CommitActionOnElement("//button[text()='Cancel']","ClickElement",AlertBox="Accept",Delay=3)

    # Doneso
    Tools.BrowserControl.eQuestMainPage()