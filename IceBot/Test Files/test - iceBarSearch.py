from pywinauto import Application
from pywinauto.timings import Timings
import time

# Adjust timings if needed
Timings.after_clickinput_wait = 2  # Add a delay after each click

icebarapp = Application(backend='uia').connect(title_re=".*iceBar.*")
icebarwindow = icebarapp.window(title_re=".*iceBar.*")
icebarwindow.print_control_identifiers()
time.sleep(1000000)