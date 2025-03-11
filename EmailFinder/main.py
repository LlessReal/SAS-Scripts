# The 7
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW
import pyperclip as pc
import keyboard as kb
import threading, os, sys, config, time
# Add tools path
ToolsPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'..', 'Tools'))
if ToolsPath not in sys.path: sys.path.append(ToolsPath)
SASPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
if SASPath not in sys.path: sys.path.append(SASPath)
import Tools.BrowserControl

# Initiation
Tools.BrowserControl.MyCSUAutoLogin(config.MyCSUUser,config.MyCSUPassword)
# Open outlook
Tools.BrowserControl.driver.get("https://outlook.office.com/mail/")
# Open new tab and open Excel
Tools.BrowserControl.driver.execute_script("window.open('');")
Tools.BrowserControl.wait.until(EC.number_of_windows_to_be(2))
Tools.BrowserControl.driver.switch_to.window(Tools.BrowserControl.driver.window_handles[1])
Tools.BrowserControl.driver.get(r"https://colstate-my.sharepoint.com/:x:/r/personal/smith_barbara9_columbusstate_edu/_layouts/15/Doc.aspx?sourcedoc=%7B393213BA-2679-4C4F-BCFF-397B856FA80E%7D&file=Check%20Vendors%20as%20of%202.28.25.xlsx&fromShare=true&action=default&mobileredirect=true")

# Function to put email in next column then go to next row
def InputValue(ValueToInput):
    Tools.BrowserControl.driver.switch_to.window(Tools.BrowserControl.driver.window_handles[1])
    Tools.BrowserControl.QuickPress("Right"); time.sleep(0.25)
    # If we're not skipping, send values and go next, else just go next
    if ValueToInput != "Skip Box": Tools.BrowserControl.actions.send_keys(ValueToInput); time.sleep(0.5)
    else: pass
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
    SearchArea.send_keys(PotentialName); time.sleep(2)
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

# Main Function
def main():
    print("Program starts in a sec."); time.sleep(3)
    while runningprogram: 
        # Copy the name / company name from box that you're on
        Tools.BrowserControl.QuickPress("Copy")
        if "Retrieving" not in pc.paste(): PotentialName = pc.paste()
        else: print("Failed to get contents, waiting for a bit then trying again"); time.sleep(10); continue
        # Checks for student if there's a comma (indicates a user)
        if "," in pc.paste(): CheckforStudent(PotentialName)
        else: InputValue("Skip Box")

def start_function():
    global runningprogram; runningprogram = True
    thread = threading.Thread(target=main); thread.start()

def stop_function(): global runningprogram; runningprogram = False

print("Click the first box, then Press ctrl+shift+f to commense and press ctrl+shift+v to stop.")
kb.add_hotkey("ctrl+shift+f", start_function)
kb.add_hotkey("ctrl+shift+v", stop_function)
kb.wait()    