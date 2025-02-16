import os, pygame
import sounddevice as sd
from config import ViewAllDeviceNames, RegularInputDeviceName
import GuiMaker 
pygame.mixer.init() # Initialization

def main():
    # Check all devices and dip
    if ViewAllDeviceNames == True:
        print(sd.query_devices())
        print("Performed Input Device Listing")
        return # The rest of the function won't run
    GuiMaker.makeTransferGui(Reset=False) 

if __name__ == '__main__':
    try:
        main() 
    except Exception as e:
        print("The program broke L", e) # Self-Explanatory
        # Below sets input device back to regular mic
        os.system(fr'powershell -Command "& {{(Get-AudioDevice -List | Where-Object {{ $_.Name -like \"{RegularInputDeviceName}\" }}) | Set-AudioDevice }}"')