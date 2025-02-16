import os, whisper

ViewAllDeviceNames = False # Btw , if this is on the program won't go
TestStereo = False
TestingBot = True
VoicelineFolderName = "Mickey" # Add GoodAfternoon.wav, GoodMorning.wav, Greeting.wav (With numbers after), PleaseWait.wav, and Repeat.wav inside this folder
CharacterVoiceLines = ["Laugh"] # Add mp3 files inside the same folder.
CustomSounds = ["Get out","I missed the part where that's my problem","Packgod Meme","Thwomp","Packgod Mickey","Never"]
RegularInputDeviceName = "Internal Microphone (Synaptics HD Audio)" # Replace with the exact name 
StereoInputDeviceName = "Stereo Mix (Synaptics HD Audio)" # Same Thing
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

# Before you use this program, run Install-Module -Name AudioDeviceCmdlets -Scope CurrentUser on Powershell
# This is for python to run the commands that change the input devices via commandline
# Also download ffmpeg from their site and put ffmpeg at the root folder
# Go to the ffmpeg install page, select your device, then select gyan.dev
# https://www.gyan.dev/ffmpeg/builds/
# Download it, go to bin, and copy ffmpeg.exe to the root folder
# gonna this lol
CurrentPath = os.path.dirname(__file__)