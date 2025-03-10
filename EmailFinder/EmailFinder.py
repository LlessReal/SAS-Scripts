# The 7
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW
import pyperclip as pc
import Tools.BrowserControl, config, time 
def CheckforStudent():
    Tools.BrowserControl.driver.switch_to.window(Tools.BrowserControl.driver.window_handles[0])
    SearchArea = Tools.BrowserControl.driver.find_element(By.XPATH,"//input[@id='topSearchInput']")
    SearchArea.send_keys(PotentialName)
    ListOfUsers = Tools.BrowserControl.driver.find_element(By.XPATH,"//div[@role='listbox']")
    ListOfUsersText = ListOfUsers.text
    EmailOnly = ListOfUsersText[ListOfUsersText.find("\"") + 1:]
    EmailOnlyNoQuotes = EmailOnly.replace("\"","")
    Tools.BrowserControl.driver.switch_to.window(Tools.BrowserControl.driver.window_handles[1])
    Tools.BrowserControl.actions.send_keys(Keys.ARROW_RIGHT); time.sleep(0.25)
    Tools.BrowserControl.actions.send_keys(EmailOnlyNoQuotes)
    
Tools.BrowserControl.MyCSUAutoLogin(config.MyCSUUser,config.MyCSUPassword)
Tools.BrowserControl.driver.get("https://outlook.office.com/mail/")
Tools.BrowserControl.driver.execute_script("window.open('');")
# Wait for the new window or tab
Tools.BrowserControl.wait.until(EC.number_of_windows_to_be(2))
# Loop through until we find a new window handle
Tools.BrowserControl.driver.switch_to.window(Tools.BrowserControl.driver.window_handles[1])
Tools.BrowserControl.driver.get(r"https://colstate-my.sharepoint.com/:x:/r/personal/smith_barbara9_columbusstate_edu/_layouts/15/Doc.aspx?sourcedoc=%7B393213BA-2679-4C4F-BCFF-397B856FA80E%7D&file=Check%20Vendors%20as%20of%202.28.25.xlsx&fromShare=true&action=default&mobileredirect=true")
time.sleep(10)

PotentialName = pc.paste()


CheckforStudent()
    