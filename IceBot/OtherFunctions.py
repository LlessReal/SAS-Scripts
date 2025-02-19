import pygetwindow as gw
# Selenium
import speech_recognition as sr
from config import model, CurrentPath
from SoundFunctions import playVoiceLine

# Opens Window
def OpenWindow(WindowName):
    Window = gw.getWindowsWithTitle(WindowName)[0] # Goes back to Excel Sheet
    if Window.isMinimized: # If the window is minimized
        Window.restore() # Unminimizes it
    Window.activate()  # Activates the window
# Closes Window
def CloseWindow(WindowName):
    Window = gw.getWindowsWithTitle(WindowName)[0] # Goes back to Excel Sheet
    Window.close()  # Activates the window

# Gets caller's message
def getCallerMessage():   
    recognizer = sr.Recognizer() # Initiate Recognizer
    microphone = sr.Microphone() # Initiate Mic
    AskedtoSpeakAlready = False
    with microphone as source: # Gets mic to listen to
        while True:
            print("Now Listening to Caller.....")
            try:
                audio = recognizer.listen(source, timeout=5) # Listens to customer's yap
                AskedtoSpeakAlready = False # Reset if it was True
            except sr.WaitTimeoutError:
                print("No message detected.")
                if AskedtoSpeakAlready:
                    playVoiceLine("Goodbye") # Says good bye and closes call window
                    CloseWindow("(External)") # Closes the call window
                    return "Left the Call"
                else:
                    playVoiceLine("NoResponse")
                    AskedtoSpeak = True
                    continue
            
            print("Stopped recording")
            try: # Try to save their message
                with open(fr"{CurrentPath}\Caller's Message\CallersMessage.wav", "wb") as file:
                    file.write(audio.get_wav_data())
                print("Audio saved as CallersMessage.wav")
            except Exception as e:
                print(f"Unable to save audio somehow {e}")
            try: # Tries to transcribe audio
                result = model.transcribe(fr"{CurrentPath}\Caller's Message\CallersMessage.wav",fp16=False, language='English')
                with open(fr"{CurrentPath}\Caller's Message\CallersMessageTranscription.txt","w") as f:
                    f.write(result["text"]) # Put it in a transcript.txt file
                print(f"Message said was: {result["text"]}")
                if result["text"].replace(" ","") == "":
                    print("No message detected.")
                    if AskedtoSpeakAlready:
                        playVoiceLine("Goodbye") # Says good bye and closes call window
                        CloseWindow("(External)") # Closes the call window
                        return "Left the Call"
                    else:
                        playVoiceLine("NoResponse")
                        AskedtoSpeak = True
                    continue
                return result["text"] # Returns the transcript for the user
            except Exception as e:
                print("Failed to recognize audio", e)
                return ""