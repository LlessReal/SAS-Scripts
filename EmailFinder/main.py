# The 7
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW
import pyperclip as pc
import keyboard as kb
import threading, os, sys, config, time, re
# Add tools path
ToolsPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'..', 'Tools'))
if ToolsPath not in sys.path: sys.path.append(ToolsPath)
SASPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
if SASPath not in sys.path: sys.path.append(SASPath)
import Tools.BrowserControl
import Tools.PDFReader

# Initiation
Tools.BrowserControl.MyCSUAutoLogin(config.MyCSUUser,config.MyCSUPassword)
# Open outlook
Tools.BrowserControl.driver.get("https://outlook.office.com/mail/")
# Open new tab and open Excel
Tools.BrowserControl.driver.execute_script("window.open('');")
Tools.BrowserControl.wait.until(EC.number_of_windows_to_be(2))
Tools.BrowserControl.driver.switch_to.window(Tools.BrowserControl.driver.window_handles[1])
Tools.BrowserControl.driver.get(config.ExcelDocURL)
# Open new tab and open OneDrive
Tools.BrowserControl.driver.execute_script("window.open('');")
Tools.BrowserControl.wait.until(EC.number_of_windows_to_be(3))
Tools.BrowserControl.driver.switch_to.window(Tools.BrowserControl.driver.window_handles[2])
Tools.BrowserControl.driver.get(config.OneDriveURL)
# Head back
Tools.BrowserControl.driver.switch_to.window(Tools.BrowserControl.driver.window_handles[1])

# Function to put email in next column then go to next row
def InputValue(ValueToInput="",NextRow=True):
    Tools.BrowserControl.driver.switch_to.window(Tools.BrowserControl.driver.window_handles[1])
    Tools.BrowserControl.QuickPress("Right"); time.sleep(0.25)
    # If we're not skipping, send values and go next, else just go next
    if ValueToInput != "Skip Box": Tools.BrowserControl.actions.send_keys(ValueToInput); time.sleep(0.5)
    else: pass
    if NextRow:
        Tools.BrowserControl.QuickPress("Down")
        Tools.BrowserControl.QuickPress("Left")
    time.sleep(0.5)


# Function to go to outlook and check if we got a student
def CheckforStudent(PotentialName):
    # Switch to outlook
    Tools.BrowserControl.driver.switch_to.window(Tools.BrowserControl.driver.window_handles[0])
    # Click search area and input value from box
    SearchArea = Tools.BrowserControl.driver.find_element(By.XPATH,"//input[@id='topSearchInput']")
    SearchArea.click()
    Tools.BrowserControl.QuickPress("Select All"); time.sleep(1)
    SearchArea.send_keys(PotentialName)
    # Grab all text from what's shown in the options
    Tools.BrowserControl.wait.until(EC.presence_of_element_located((By.XPATH,"//div[@role='listbox' and @aria-label='Search Suggestions']")))
    ListOfUsers = Tools.BrowserControl.driver.find_element(By.XPATH,"//div[@role='listbox' and @aria-label='Search Suggestions']")
    ListOfUsersText = ListOfUsers.text
    if "No suggestions found" in ListOfUsersText: InputValue("N/A"); return 
    else:
        # Attempt to grab email
        EmailOnly = ListOfUsersText[ListOfUsersText.find("\"") + 1:]
        EmailOnlyNoQuotes = EmailOnly.replace("\"","")
        InputValue(EmailOnlyNoQuotes)


def FindCompanyEmail(CompanyName):
    # Switch to OneDrive
    Tools.BrowserControl.driver.switch_to.window(Tools.BrowserControl.driver.window_handles[2])
    # Click search area and input company name into box
    SearchArea = Tools.BrowserControl.driver.find_element(By.XPATH,"//input[@type='search']")
    SearchArea.click()
    Tools.BrowserControl.QuickPress("Select All"); time.sleep(1)
    SearchArea.send_keys(CompanyName)
    
    # Grab all text from what's shown in the options
    Tools.BrowserControl.wait.until(EC.presence_of_element_located((By.XPATH,"//ul[@role='group' and @id='file']")))
    ListofDocs = Tools.BrowserControl.driver.find_element(By.XPATH,"//ul[@role='group' and @id='file']")
    # Tries to find and click pdf file
    try: Tools.BrowserControl.CommitActionOnElement("//span[contains(text(),'pdf')]","ClickElement",SuccessMessage="Found a PDF document !!") # Press Attachments button
    # If it failed, will just skip the box
    except: print("No PDF Doc found"); InputValue("Skip Box") # Skip the box if found no

    # Heads to tab
    Tools.BrowserControl.wait.until(EC.number_of_windows_to_be(4)); 
    Tools.BrowserControl.driver.switch_to.window(Tools.BrowserControl.driver.window_handles[3])
    # Opens Acrobat
    Tools.BrowserControl.CommitActionOnElement("//span[contains(@class,'ms-Button-label') and contains(text(),'Open')]","ClickElement")
    Tools.BrowserControl.CommitActionOnElement("//span[contains(@class,'ms-ContextualMenu-itemText') and contains(text(),'Open in Adobe Acrobat')]","ClickElement")
    Tools.BrowserControl.wait.until(EC.number_of_windows_to_be(5)); 
    Tools.BrowserControl.driver.switch_to.window(Tools.BrowserControl.driver.window_handles[4])
    Tools.BrowserControl.CommitActionOnElement("//button[@aria-label='Download this document']","ClickElement")
    time.sleep(5)
    OrderText = Tools.PDFReader.NewOCR(f"{config.DownloadsPath}\\{Tools.BrowserControl.driver.title}")
    
    PotentialEmails = re.findall(r'\b\w*@\w*\b', OrderText)
    print(f"All Emails: {PotentialEmails}")
    Tools.BrowserControl.driver.close()
    Tools.BrowserControl.driver.switch_to.window(Tools.BrowserControl.driver.window_handles[3])
    Tools.BrowserControl.driver.close()
    # If no emails found, marks cell as N/A, else it will put email 
    # (if multiple, will be multiple columns)
    if PotentialEmails == []: print("No emails found"); InputValue("N/A")
    else: 
        for Email in PotentialEmails: InputValue(Email,NextRow=False)
        Tools.BrowserControl.QuickPress("Down")
        for Email in PotentialEmails: Tools.BrowserControl.QuickPress("Left") 
        # Return back to OG position
    
# Main Function
def main():
    print("Program starts in a sec."); time.sleep(3)
    global runningprogram
    while runningprogram: 
        # Copy the name / company name from box that you're on
        Tools.BrowserControl.QuickPress("Copy")
        if "Retrieving" not in pc.paste(): NameToSearch = pc.paste()
        else: print("Failed to get contents, waiting for a bit then trying again"); time.sleep(10); continue
        # Checks for student if there's a comma (indicates a user)
        if "," in NameToSearch and " Inc" not in NameToSearch: CheckforStudent(NameToSearch)
        elif NameToSearch.replace(" ","") != "": FindCompanyEmail(NameToSearch)
        else: print("We have reached the end, ending program."); runningprogram = False 

def start_function():
    global runningprogram; runningprogram = True
    thread = threading.Thread(target=main); thread.start()

def stop_function(): global runningprogram; runningprogram = False

print("Click the first box, then Press ctrl+shift+f to commense and press ctrl+shift+v to stop.")
kb.add_hotkey("ctrl+shift+f", start_function)
kb.add_hotkey("ctrl+shift+v", stop_function)
kb.wait()    