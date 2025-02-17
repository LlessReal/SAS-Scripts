import os, whisper

ViewAllDeviceNames = False # Btw , if this is on the program won't go
TestingBot = False
TestingStereoInput = False
VoicelineFolderName = "Mickey" # Add GoodAfternoon.wav, GoodMorning.wav, Greeting.wav (With numbers after), PleaseWait.wav, and Repeat.wav inside this folder
RegularInputDeviceName = "Internal Microphone (Synaptics HD Audio)" # Replace with the exact name | Saves: Microphone (Realtek(R) Audio), Internal Microphone (Synaptics HD Audio)
StereoInputDeviceName = "Stereo Mix (Synaptics HD Audio)" # Same Thing | Saves: Stereo Mix (Synaptics HD Audio)

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

# Model name
model = whisper.load_model("base") # Download the model

""" 
Before you use this program,
run Install-Module -Name AudioDeviceCmdlets -Scope CurrentUser on Powershell
This is for python to run the commands that change the input devices via commandline
Also download ffmpeg from their site and put ffmpeg at the root folder
Go to the ffmpeg install page, select your device, then select gyan.dev
https://www.gyan.dev/ffmpeg/builds/
Download it, go to bin, and copy ffmpeg.exe to the root folder
"""

# Post Config Stuff (Just ignore)
CurrentPath = os.path.dirname(__file__)
CustomSounds = os.listdir(fr"{CurrentPath}\Custom Sounds")
# Building the character voice lines list
CharacterVoiceLines = [CharacterVoiceLine for CharacterVoiceLine in os.listdir(fr"{CurrentPath}\{VoicelineFolderName}") if "mp3" in CharacterVoiceLine]
# Makes a new list with only files that have "mp3" in it