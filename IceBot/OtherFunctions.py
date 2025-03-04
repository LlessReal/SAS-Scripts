import pygetwindow as gw

# Opens Window
def OpenWindow(WindowName):
    Window = gw.getWindowsWithTitle(WindowName)[0] # Goes back to Excel Sheet
    if Window.isMinimized: Window.restore() # If the window is minimized
    Window.activate()  # Activates the window
    
# Closes Window
def CloseWindow(WindowName):
    Window = gw.getWindowsWithTitle(WindowName)[0] # Goes back to Excel Sheet
    Window.close()  # Activates the window