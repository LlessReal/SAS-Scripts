import pygame
pygame.mixer.init(); pygame.mixer.set_num_channels(22)
import os, GuiMaker
import sounddevice as sd
from config import ViewAllDeviceNames

def main():
    # Check all devices and dips (If Enabled)
    if ViewAllDeviceNames: print(sd.query_devices()); print("Performed Input Device Listing"); return 
    GuiMaker.makeTransferGui(ResettingGui=False,StartingProgram=True) 
   
if __name__ == '__main__':
    while True:
        try: main() 
        except Exception as e: 
            print(e)
            if "Restarting Program" in str(e): continue
            else: print("The program broke L", e); break 