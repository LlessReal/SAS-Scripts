import pygetwindow as gw

# Opens Window
def OpenWindow(WindowName):
    Window = gw.getWindowsWithTitle(WindowName)[0] # Goes back to Excel Sheet
    if Window.isMinimized: Window.restore() # If the window is minimized
    try: Window.activate()  # Activates the window
    except Exception as e: print(e)
    
# Closes Window
def CloseWindow(WindowName): Window = gw.getWindowsWithTitle(WindowName)[0]; Window.close()  