import pyautogui as pya
import keyboard, threading
import pyperclip as pc
import clipboard as cb

running = True

def main():
    global running
    while running:
        pass
        # LOOP

    # If code ended due to hotkey, this goes.
    print("The code has halted.")

def start_function():
    global running
    running = True
    thread = threading.Thread(target=main)
    thread.start()

def stop_function():
    global running
    running = False
    print("The code will be halted shortly.")


if __name__ == "__main__":
    print("Press ctrl+shift+f to commense and press ctrl+shift+v to stop.")
    keyboard.add_hotkey("ctrl+shift+f", start_function)
    keyboard.add_hotkey("ctrl+shift+v", stop_function)
    keyboard.wait()