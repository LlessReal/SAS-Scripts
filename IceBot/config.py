import os, whisper

ViewAllDeviceNames = False # Btw , if this is on the program won't go
VoicelineFolderName = "Mickey" # Add GoodAfternoon.wav, GoodMorning.wav, Greeting.wav (With numbers after), PleaseWait.wav, and Repeat.wav inside this folder
ModelName = "sblight2"  # Replace with your desired Ollama model
SpeakerName = "Speakers (Synaptics HD Audio)"
api_key = ""
# Incoming Audio Areas (Gotta press Tab 7 TImes to get to)
SpeakerArea = 2 
HeadPhoneArea = 1 
# Input Areas (Gotta press Tab 3 TImes to get to)
StereoMixArea = 1 # 3 times
MicArea = 2
SpeakerOptions = 4 # Put the amount u see
MicOptions = 2

# Go to Microsoft settings -> Devices, and press the Icon that's next to Audio Settings (AFTER MOVING THE SETTING TO WHERE YOU WANT IT TO BE !!!!!!!)
# Important phone numbers and names
ImportantTermDictionary = {
    "human resources": (7065078920,""),
    "admissions": (6001,""),
    "financial aid": (6002,""),
    "bursar": (6002,""),
    "registrar": (6004,""),
    "orientation": (7065078593,""),
    "advisor": (7065078780,""),
    "military": (7065078866,""),
    "housing": (7065078710,""),
}

model = whisper.load_model("base") # Download the model

# Post Config Stuff (Just ignore)
CurrentPath = os.path.dirname(__file__)