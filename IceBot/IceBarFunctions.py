import pyautogui as pya
import GuiMaker
from time import sleep
from config import CurrentPath
from SoundFunctions import playVoiceLine
from OtherFunctions import CloseWindow

def PressIceButton(ImagePath,FailMessage):
    AlreadyTried = False 
    Timeout = 0   
    while True:
        try:
            transferbutton = pya.locateOnScreen(ImagePath) # Finds transfer button, if it's not on screen, goes to except
            pya.click(transferbutton) # Click the button
            return
        except:
            if AlreadyTried == False:
                print(FailMessage) 
                AlreadyTried = True
            
            ResetState = GuiMaker.BackToStageOne(True)
            if ResetState == "ResetGuiNow":
                return
            sleep(0.1)
            Timeout += 1
            if Timeout == 100:
                return "Fail"
            continue 

# Auto Transfer
def AutoTransferSubmitVersion(TransferNumber,SayVoiceLine,WaitBeforeGo,StartingProgram=False):
    if StartingProgram:
        print("Program hasn't started yet")
        return
    if SayVoiceLine: # If Say Voice Line Check Box is Checked
        playVoiceLine("TransferingNow") # Plays line
        if WaitBeforeGo: # If Wait for reaction is checked
            print("Waiting for reaction")
            sleep(5) # Wait for reacton
    print(f"{TransferNumber} Will be sent")
    try:
        IcebarDropDownArrow = pya.locateOnScreen(fr"{CurrentPath}\..\IceBarImages\Icebardropdownarrow.png") # Can do directories as well btw
        InitialPosition = pya.position()
        pya.click(IcebarDropDownArrow) # Click the button        
    except:
        print("Ice bar is closed/missing")
        ResetState = GuiMaker.BackToStageOne(True)
        return
    sleep(1)
    MoveOnStatus = PressIceButton(fr"{CurrentPath}\..\IceBarImages\TransferButton.png","You're not in a call.")   
    if MoveOnStatus == "Fail":
        pya.click(IcebarDropDownArrow) # Clicks again to close
        pya.moveTo(InitialPosition) # Go to OG position
        return

    # Tries to find initiate transfer button to see if we should type info or not
    for i in range(99):
        try:
            InitiateTransferButton = pya.locateOnScreen(fr"{CurrentPath}\..\IceBarImages\InitiateTransferButton.png") # Checks if the 2nd window after you press transfer is up
            pya.write(f"{TransferNumber} \n") # Types number and then press enter
            sleep(1)
            break
        except:
            print("Couldn't find the initiate transfer button, retrying")
            sleep(0.1)
            if i == 99: # If 10 seconds passed and transfer still not complete
                print("Failed operation. PC too laggy") 
                pya.moveTo(InitialPosition) 
                return
            
    CloseWindow("(External)") # Close the calling window   
    print("Transfer Successful!")
    pya.moveTo(InitialPosition) # End
    # FINAL PHASE - Return to Normal
    print("The deed is done")
