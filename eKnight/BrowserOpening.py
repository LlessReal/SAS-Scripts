import time, config
# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys # Needed for sending keys

def MyCSUAutoLogin():
    options = Options() # Get options
    global driver
    driver = webdriver.Chrome(options=options) # Opens Chrome browser with options (if u put any)
    global actions
    actions = ActionChains(driver) # Prepares Chrome to make key actions (for future use in the program)
    driver.get("https://mycsu.columbusstate.edu/") # Opens URL for chat area (leads to login)
    driver.maximize_window() # Maxes window
    global wait
    wait = WebDriverWait(driver,300)
    wait.until(EC.presence_of_element_located((By.NAME,"loginfmt"))) # Wait for box to partially load
    time.sleep(1) # Wait for page to load
    # Email
    EmailBox = driver.find_element(By.NAME,"loginfmt") # Get it
    EmailBox.send_keys(config.MyCSUUser + "\n") # Put details in it
    wait.until(EC.presence_of_element_located((By.NAME,"passwd")))
    time.sleep(1) 
    # Password
    PasswordBox = driver.find_element(By.NAME,"passwd")
    PasswordBox.send_keys(config.MyCSUPassword + "\n")
    
    # Selects 2 Factor button or whatever
    wait.until(EC.presence_of_element_located((By.XPATH,"//div[text()='Verify your identity']")))
    actions.send_keys(Keys.ENTER)
    actions.perform()

    # Complete the 2 Factor
    
    # Wait for page to load
    wait.until(EC.title_contains("MyCSU"))
    eQuestMainPage()

def eQuestMainPage():
    driver.get("https://csuequest.easyvista.com/") # Open eQuest Service Manager Main Page
    # Wait till Search Box
    wait.until(EC.presence_of_element_located((By.XPATH,"//input[@id='search-input']")))
    # Program begins.
    time.sleep(1)