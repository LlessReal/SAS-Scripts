def NextRow(Status="Success",Swipes=1,NextBox=1):
    if Status == "Fail": # If Fail is in paremeter, this gets printed
        print("Process failed, doing next line")
    ScrollDownSign = pya.locateOnScreen(rf"{config.CurrentPath}\eProImages\ScrollDownSign.png",confidence=0.9)
    keyboard.write("\n")
    for i in range(Swipes + 1):
        pya.click(ScrollDownSign)
        time.sleep(0.25)
    pya.press('up') # Go back to same box
    time.sleep(0.25)
    for i in range(NextBox - 1):
        pya.click(ScrollDownSign)
        time.sleep(0.25)