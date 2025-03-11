import speech_recognition as sr
import os
StereoInputDeviceName = "Stereo Mix (Synaptics HD Audio)" # Same Thing
RegularInputDeviceName = "Internal Microphone (Synaptics HD Audio)" # Replace with the exact name 

os.system(fr'powershell -Command "& {{(Get-AudioDevice -List | Where-Object {{ $_.Name -like \"{RegularInputDeviceName}\" }}) | Set-AudioDevice }}"')

recognizer = sr.Recognizer()
microphone = sr.Microphone()
CurrentPath = os.path.dirname(__file__)
with microphone as source:
    print("Say something!")
    audio = recognizer.listen(source)
    try:
        print("Stopped recording")
        with open(fr"{CurrentPath}\GoodMorning.wav", "wb") as file: # GoodMorning, GoodAfternoon, Greeting, Wait, TransferingNow, Repeat
            file.write(audio.get_wav_data())
        print("Audio saved")
    except Exception as e:
        print(f"Could not request results; {e}")