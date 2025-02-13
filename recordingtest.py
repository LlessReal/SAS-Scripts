import speech_recognition as sr
import os
StereoInputDeviceName = "Stereo Mix (Synaptics HD Audio)" # Same Thing
os.system(fr'powershell -Command "& {{(Get-AudioDevice -List | Where-Object {{ $_.Name -like \"{StereoInputDeviceName}\" }}) | Set-AudioDevice }}"')

recognizer = sr.Recognizer()
microphone = sr.Microphone()
  
with microphone as source:
    print("Say something!")
    audio = recognizer.listen(source)
    try:
        print("Stopped recording")
        with open("recorded_audio.wav", "wb") as file:
            file.write(audio.get_wav_data())
        print("Audio saved as recorded_audio.wav")
    except Exception as e:
        print(f"Could not request results; {e}")
    words = recognizer.recognize_google(audio)
    print(words)

