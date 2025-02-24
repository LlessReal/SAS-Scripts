import pygetwindow as gw
import time
import pyautogui as pya
import keyboard
import pyperclip as pc
import os

# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pickle
# Prerequisite select functions

########################################################            
# Phase 0 - Open Page
########################################################
ExcelDocURL = r"https://csuequest.easyvista.com/index.php?PHPSESSID=ef650fe25b9544a1fc98a3be62e07b51&internalurltime=1740362294#"
MyCSUUser = ""
MyCSUPassword = ""

def StartUpBrowser():
    options = Options() # Get options
    global driver
    driver = webdriver.Chrome(options=options) # Opens Chrome browser with options (if u put any)
    driver.get(ExcelDocURL) # Opens URL for chat area (leads to login)
    driver.maximize_window() # Maxes window
    wait = WebDriverWait(driver,300)
    wait.until(EC.presence_of_element_located((By.NAME,"loginfmt")))
    time.sleep(1)
    EmailBox = driver.find_element(By.NAME,"loginfmt")
    EmailBox.send_keys(MyCSUUser + "\n")
    wait.until(EC.presence_of_element_located((By.NAME,"passwd")))
    time.sleep(1)
    PasswordBox = driver.find_element(By.NAME,"passwd")
    PasswordBox.send_keys(MyCSUPassword + "\n")
    time.sleep(25)
    
    global actions
    actions = ActionChains(driver) # Prepares Chrome to make key actions (for future use in the program)
    
StartUpBrowser()