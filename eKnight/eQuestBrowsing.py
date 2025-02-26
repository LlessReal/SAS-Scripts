import time
import MyCSUAutoLogin
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys # Needed for sending keys

wait = WebDriverWait(MyCSUAutoLogin.driver,300)

def SearchSRNum(SRNum):
    wait.until(EC.presence_of_element_located((By.NAME,"loginfmt"))) # Wait for box to partially load
    # Send stuff to search box
    eQuestSearchBox = MyCSUAutoLogin.driver.find_element(By.ID,"search-input")
    eQuestSearchBox.send_keys(SRNum)
    ResultsList = MyCSUAutoLogin.driver.find_element(By.CLASS_NAME,"results-list")
    while ResultsList.text.replace(" ","") == "":
        pass
    eQuestSearchBox.send_keys("\n")
    time.sleep(5)

def AttachPDF(PDFFilePath,SRNum,FullSRNumIG):
    DetailsBox = MyCSUAutoLogin.driver.find_element(By.XPATH, "//span[text()='Details']") 
    DetailsBox.click()
    wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Attachments']")))
    time.sleep(1)

    # Attachment Button
    AttachmentButton = MyCSUAutoLogin.driver.find_element(By.XPATH, "//button[text()='Attachments']") 
    AttachmentButton.click()
    wait.until(EC.presence_of_element_located((By.ID, "file_to_upload")))
    time.sleep(1)

    # Gets drop box
    PDFDropBox = MyCSUAutoLogin.driver.find_element(By.ID, "file_to_upload")
    # Perform the drag and drop action
    MyCSUAutoLogin.actions.drag_and_drop(PDFFilePath, PDFDropBox)
    MyCSUAutoLogin.actions.perform()
    wait.until(EC.presence_of_element_located((By.XPATH, f"//span[text()='{FullSRNumIG}.pdf']")))
    time.sleep(1)

    # Click close button
    CloseButton = MyCSUAutoLogin.driver.find_element(By.XPATH, "//button[text()='Close']") 
    CloseButton.click()
    time.sleep(1)

    # Click Activity Box
    ActivityBox = MyCSUAutoLogin.driver.find_element(By.XPATH, "//span[text()='Activity']") 
    ActivityBox.click()
    time.sleep(1)

    SupportPersonBox = MyCSUAutoLogin.driver.find_element(By.XPATH, "//div[@field-label='Support Person']") 
    SupportPersonBoxContents = SupportPersonBox.text
    SupportPersonName = SupportPersonBoxContents.replace("Support Person","").replace(" ","")

    # Click Log Activity Box
    LogActivityBox = MyCSUAutoLogin.driver.find_element(By.XPATH, "//button[text()='Log Activity']") 
    LogActivityBox.click()
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='eventcombo-ui']")))
    time.sleep(1)
    
    # Type Internal Input
    ActionType = MyCSUAutoLogin.driver.find_element(By.XPATH, "//input[@id='eventcombo-ui']") 
    ActionType.send_keys("_Internal Update_")
    MyCSUAutoLogin.actions.send_keys(Keys.ARROW_DOWN)
    MyCSUAutoLogin.actions.perform()
    time.sleep(0.25)
    MyCSUAutoLogin.actions.send_keys(Keys.ENTER)
    MyCSUAutoLogin.actions.perform()
    time.sleep(2)
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
    time.sleep(1)
    SupportPersonInput = MyCSUAutoLogin.driver.find_element(By.XPATH, "//input[@type='text']") 
    SupportPersonInput.send_keys(SupportPersonName)
    time.sleep(10)
    MyCSUAutoLogin.actions.send_keys(Keys.ARROW_DOWN)
    MyCSUAutoLogin.actions.perform()
    time.sleep(0.25)
    MyCSUAutoLogin.actions.send_keys(Keys.ENTER)
    MyCSUAutoLogin.actions.perform()
    time.sleep(10)
    SendEmailBox = MyCSUAutoLogin.driver.find_element(By.XPATH, "//button[text()='Send Email & Finish']") 
    SendEmailBox.click()
    time.sleep(5)

    EmailMessageBox = MyCSUAutoLogin.driver.find_element(By.XPATH, "//body[@id='tinymce']") 
    EmailMessageBox.send_keys(f"Hello, {SupportPersonName}. Please see the Aramark invoice for {SRNum} attached for payment processing.\n\nThanks,\nJay")
    time.sleep(5)

    FinishBox = MyCSUAutoLogin.driver.find_element(By.XPATH, "//button[text()='Finish']") 
    FinishBox.click()
    time.sleep(2)
    
    # Click Log Activity Box
    ReopenBox = MyCSUAutoLogin.driver.find_element(By.XPATH, "//button[text()='Reopen']") 
    ReopenBox.click()
    wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@id='comment']")))
    time.sleep(1)

    # Reopen Message
    ReopenMessage = MyCSUAutoLogin.driver.find_element(By.XPATH, "//textarea[@id='comment']") 
    ReopenMessage.send_keys("Ready For Processing.")
    time.sleep(0.5)
    FinishBox = MyCSUAutoLogin.driver.find_element(By.XPATH, "//button[text()='Finish']") 
    FinishBox.click()
    time.sleep(2)
