from pywinauto import Application
from pywinauto.timings import Timings

# Adjust timings if needed
Timings.after_clickinput_wait = 2  # Add a delay after each click

try:
    # Step 1: Launch or connect to Microsoft Teams
    app = Application(backend='uia').connect(title_re=".*Microsoft Teams.*")
    print("Successfully connected to Microsoft Teams!")

    # Step 2: Get the main window of the application
    main_window = app.window(title_re=".*Microsoft Teams.*")
    
    # Check if the main window is found
    if main_window.exists():
        print("Main window found!")
        print("Window title:", main_window.window_text())
    else:
        print("Main window not found!")

    # Step 3: Perform some actions (optional)
    # For example, you can try to maximize the window
    # Step 3: Locate the sidebar (usually a pane or toolbar)
    one_drive_button = main_window.child_window(
    title="OneDrive",  # Title of the button
    auto_id="5af6a76b-40fc-4ba1-af29-8f49b08e44fd",  # Automation ID
    control_type="Button"  # Control type
)

    # Wait for the button to be ready (optional but recommended)
    #one_drive_button.wait('ready', timeout=10)

    one_drive_button.set_focus()
    #one_drive_button.click()
    one_drive_button.invoke()

    # Click the "OneDrive" button
    #one_drive_button.click_input() # or click() if that didnt work

except Exception as e:
    print(f"An error occurred: {e}")