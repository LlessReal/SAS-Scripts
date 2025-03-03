import time
# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys # Needed for sending keys

def MyCSUAutoLogin(MyCSUUser,MyCSUPassword,TargetWebsite="",URL=""):
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
    CommitActionOnElement("//input[@type='email']","ClickElement,InputtingElement",MessageAfterClick=MyCSUUser,PressEnter=True)
    # Password
    CommitActionOnElement("//input[@name='passwd']","ClickElement,InputtingElement",MessageAfterClick=MyCSUPassword,PressEnter=True)
    # Gotta do clicks cuz bug
    
    # Selects 2 Factor button or whatever
    wait.until(EC.presence_of_element_located((By.XPATH,"//div[text()='Verify your identity']")))
    actions.send_keys(Keys.ENTER).perform()
    # Complete the 2 Factor
    
    # Wait for page to load
    wait.until(EC.title_contains("MyCSU"))

def openPage(URL): driver.get(URL)
def eQuestMainPage(MyCSUFirst=False): 
    if MyCSUFirst: openPage("https://mycsu.columbusstate.edu/")
    driver.get("https://csuequest.easyvista.com/") # eQuest main page

# Function to click,send something to, or grab text from element
# Format: Element by XPATH, Action, eQuest Drop Down or not, and if there's an alternative element or nah
def CommitActionOnElement(Element,Action="",eQuestDropDown=False,AltElement="",AltAction="",SwappingToIframe=False,MessageAfterClick="",PressEnter=False,Delay=0,SuccessMessage="Successfully Completed",TypeOfItem="",AlertBox=""):
    if SwappingToIframe:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        iframe = driver.find_element(By.TAG_NAME, "iframe")  # Adjust selector
        driver.switch_to.frame(iframe)
        print(f"Swapped to Iframe!")
        time.sleep(1)

    wait.until(EC.presence_of_element_located((By.XPATH, Element)))
    ElementChosen = driver.find_element(By.XPATH, Element)
    
    print(f"{Element} found. Committing action in a sec..." if Action != "" else f"{Element} found.")
    time.sleep(1)
    if Action == "Grab Alt Text":
        time.sleep(Delay)
        print(f"{TypeOfItem} - {ElementChosen.get_attribute('alt')}")
        return ElementChosen.get_attribute('alt')
    
    if Action == "Grab Text":
        time.sleep(Delay)
        print(f"{TypeOfItem} - {ElementChosen.text}")
        return ElementChosen.text
    
    if AltElement != "": # If we're dooing another element
        wait.until(EC.presence_of_element_located((By.XPATH, AltElement)))
        ElementChosen = driver.find_element(By.XPATH, AltElement)
        ElementChosen.send_keys(AltAction) if "ClickElement" not in AltAction else ElementChosen.click()
        if "InputtingElement" in AltAction:
            if "ResetElement" in Action:
                QuickPress("a")
                time.sleep(0.25)
            actions.send_keys(MessageAfterClick).perform()
        
    else: # If regular
        if Action != "":
            ElementChosen.send_keys(Action) if "ClickElement" not in Action else ElementChosen.click()   
            if "InputtingElement" in Action:
                if "ResetElement" in Action:
                    QuickPress("a")
                time.sleep(0.5)
                actions.send_keys(MessageAfterClick).perform()
        else:
            pass # No action will be done

    if PressEnter == True:
        time.sleep(1)
        actions.send_keys(Keys.ENTER).perform()

    if SwappingToIframe: driver.switch_to.default_content()
    # If statement to turn back to main page was supposed to be here but it wasn't goddamn working for some reason
    time.sleep(1)

    if eQuestDropDown: 
        actions.send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(0.5)
        actions.send_keys(Keys.ENTER).perform()
        time.sleep(1)

    if AlertBox != "":
        alert = driver.switch_to.alert
        alert.accept() if AlertBox == "Accept" else alert.dismiss()
        
    print(SuccessMessage)
    time.sleep(Delay)

def QuickPress(ImportantKey,Limit=1):
    LimitCounter = 0
    while LimitCounter != Limit:
        if ImportantKey == "Up":
            actions.send_keys(Keys.ARROW_UP).perform()
        elif ImportantKey == "Right":
            actions.send_keys(Keys.ARROW_RIGHT).perform()
        elif ImportantKey == "Down":
            actions.send_keys(Keys.ARROW_DOWN).perform()
        elif ImportantKey == "Left":
            actions.send_keys(Keys.ARROW_LEFT).perform()
        elif ImportantKey == "Enter":
            actions.send_keys(Keys.ENTER).perform()
        elif ImportantKey == "Copy":
            actions.key_down(Keys.CONTROL).send_keys("c").key_up(Keys.CONTROL).perform()
        elif ImportantKey == "Paste":
            actions.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
        elif ImportantKey == "Cut":
            actions.key_down(Keys.CONTROL).send_keys("x").key_up(Keys.CONTROL).perform()
        elif ImportantKey == "Select All":
            actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
        LimitCounter += 1