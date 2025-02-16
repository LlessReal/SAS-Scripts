import pyautogui as pya
import os, random, wave, pyaudio, pygame, datetime
from config import VoicelineFolderName, CurrentPath 
# Play sound from soundboard
def playCustomSound(SoundName):
    try:
        (pygame.mixer.Sound(fr"{CurrentPath}\Custom Sounds\{SoundName}")).play()
    except:
        print("No sound found. (bars)")
# Play character line that's in their folder
def playCharacterLine(SoundName):
    try:
        (pygame.mixer.Sound(fr"{CurrentPath}\{VoicelineFolderName}\{SoundName}")).play()
    except:
        print("No sound found. (bars)")
# Play a wav file
def PlayWaveFile(WavFile):
    chunk = 1024  
    wf = wave.open(WavFile, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(chunk)
    while data:
        stream.write(data)
        data = wf.readframes(chunk)
    stream.stop_stream() # Stop receiving data
    stream.close() # Close Stream
    p.terminate()
# Play voice line from character folder
def playVoiceLine(VoicelineType):
    try:
        UnmuteSign = pya.locateOnScreen(fr"{CurrentPath}\..\IceBarImages\Unmute.png")
        pya.click(UnmuteSign)
    except:
        pass
    AllVoicelines = [] # List Initialization
    for Voiceline in os.listdir(fr"{CurrentPath}\{VoicelineFolderName}"): # Gets all files in the Voiceliens folder
        if VoicelineType in os.path.join(fr"{CurrentPath}\{VoicelineFolderName}", Voiceline): # If the type of voiceline is in the file name
            AllVoicelines.append(os.path.join(fr"{CurrentPath}\{VoicelineFolderName}", Voiceline)) # Add it to the list
    try:
        PlayWaveFile(random.choice(AllVoicelines)) # Play a random sound from the type
    except:
        print("Voiceline wasn't found.")
# General Greeting (Good Morning/Afternoon and Greet)
def GeneralGreeting():
    CurrentDateandTime = datetime.datetime.now() # Gets time to determine whether Good Afternoon or Good Morning
    playVoiceLine("GoodMorning" if CurrentDateandTime.strftime("%p") == "AM" else "GoodAfternoon")
    playVoiceLine("Greeting")