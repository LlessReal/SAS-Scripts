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
    # Email
    CommitActionOnElement("//input[@name='loginfmt']",config.MyCSUUser,PressEnter=True)
    # Password
    CommitActionOnElement("//input[@name='passwd']",config.MyCSUPassword,PressEnter=True)
    
    # Selects 2 Factor button or whatever
    wait.until(EC.presence_of_element_located((By.XPATH,"//div[text()='Verify your identity']")))
    actions.send_keys(Keys.ENTER).perform()
    # Complete the 2 Factor
    
    # Wait for page to load
    wait.until(EC.title_contains("MyCSU"))
    eQuestMainPage()

# eQuest main page
def eQuestMainPage():
    driver.get("https://csuequest.easyvista.com/") # Open eQuest Service Manager Main Page

# Function to click,send something to, or grab text from element
# Format: Element by XPATH, Action, eQuest Drop Down or not, and if there's an alternative element or nah
def CommitActionOnElement(Element,Action,eQuestDropDown=False,AltElement="",AltAction="",SwappingToIframe=False,MessageAfterClick="",PressEnter=False,Delay=0):
    if SwappingToIframe:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        iframe = driver.find_element(By.TAG_NAME, "iframe")  # Adjust selector
        driver.switch_to.frame(iframe)
        print(f"Swapped to Iframe!")
        time.sleep(1)

    wait.until(EC.presence_of_element_located((By.XPATH, Element)))
    ElementChosen = driver.find_element(By.XPATH, Element)
    print(f"{Element} found. Committing action in a sec...")
    time.sleep(1)
    if Action == "Grab Text":
        time.sleep(Delay)
        return ElementChosen.get_attribute("alt")
    
    if AltElement != "": # If we're dooing another element
        wait.until(EC.presence_of_element_located((By.XPATH, AltElement)))
        ElementChosen = driver.find_element(By.XPATH, AltElement)
        ElementChosen.send_keys(AltAction) if "Clicking" not in AltAction else ElementChosen.click()
        if Action == "Clicking and Inputting":
            actions.send_keys(MessageAfterClick).perform()
        
    else: # If regular
        ElementChosen.send_keys(Action) if "Clicking" not in Action else ElementChosen.click()
        if Action == "Clicking and Inputting":
            actions.send_keys(MessageAfterClick).perform()

    if PressEnter == True:
            time.sleep(1)
            actions.send_keys(Keys.ENTER).perform()

    if SwappingToIframe:
        driver.switch_to.default_content()
    # If statement to turn back to main page was supposed to be here but it wasn't goddamn working for some reason
    time.sleep(1)

    if eQuestDropDown:
        actions.send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(0.5)
        actions.send_keys(Keys.ENTER).perform()
        time.sleep(1)
    time.sleep(Delay)