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
ExcelDocURL = r"https://colstate-my.sharepoint.com/:x:/r/personal/tinsley_kele_columbusstate_edu1/Documents/Documents/BOR_POAP_DETAIL_CSU_1641220935.xlsx?d=wa5432ca0ad5f4566b7a7bc21b2048b72&csf=1&web=1&e=5vxhuQ"
MyCSUUser = "marshall_miguel@columbusstate.edu"
MyCSUPassword = "Ll3ss1@3$5^Ll3ss1@3$5^"

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
    WebCookies = driver.get_cookies()
    driver.add_cookie(WebCookies) # Adds those cookies back to the site so you want have to relogin
    # Better: Make a cookie.py file with below as variable
    cookies = [ { "domain":"xxx" }, {"domain":"yyy"} ]
    # in main... do this
    cookiefile = open("cookies.py","w")
    time.sleep(2)
    from cookies import cookies # from cookies.py file
    for i in cookies:
        driver.add_cookie(cookies[i]) # Gets all the cookies
    global actions
    actions = ActionChains(driver) # Prepares Chrome to make key actions (for future use in the program)
    
StartUpBrowser()