import time, config
# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def StartUpBrowser():
    options = Options() # Get options
    global driver
    driver = webdriver.Chrome(options=options) # Opens Chrome browser with options (if u put any)
    driver.get("https://mycsu.columbusstate.edu/") # Opens URL for chat area (leads to login)
    driver.maximize_window() # Maxes window
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
    
    # Complete 2 Factor
    
    # Wait for page to load
    wait.until(EC.title_contains("MyCSU"))
    time.sleep(1)
    # Open eQuest Service Manage
    driver.get("https://csuequest.easyvista.com/")
    # Wait till Search Box
    wait.until(EC.presence_of_element_located((By.ID,"search-input")))
    
    global actions
    actions = ActionChains(driver) # Prepares Chrome to make key actions (for future use in the program)