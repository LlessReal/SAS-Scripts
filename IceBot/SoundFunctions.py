import pyautogui as pya
import os, random, wave, pyaudio, pygame, datetime, subprocess
from config import VoicelineFolderName, CurrentPath 
# Play sound from soundboard
from pydub import AudioSegment
AudioSegment.converter = fr'{CurrentPath}\ffmpeg'

def ChangeAudio(input_file_path, output_file_path, speed):
    """
    Slows down an audio file using FFmpeg without changing pitch.
    :param input_file: Path to the input audio file. output_file: Path to save the slowed-down audio.
    :param speed: Playback speed (0.5 = half speed, 2.0 = double speed).
    """
    #command = [
    #    "ffmpeg", "-i", input_file, # Get the path to the file
    #    "-filter:a", f"atempo={speed}",
    #3    "-vn", output_file
    #]
    # subprocess.run(command, check=True)
    os.system(fr"ffmpeg -i {input_file_path} -filter:a atempo={speed} -vn {output_file_path}")

def playSound(SoundName,SpeedChange,BrainrotModeActivated,CharacterLine):
    SoundFolder = "Custom Sounds" if CharacterLine == False else VoicelineFolderName
    input_audio = fr"{CurrentPath}\{SoundFolder}\{SoundName}"
    try:
        if BrainrotModeActivated:
            if SoundName.replace(".mp3"," Brainrot Edition.mp3") in os.listdir(fr"{CurrentPath}\Brainrot Audio Cache"):
                Sound1Name = fr"{CurrentPath}\Brainrot Audio Cache\{SoundName}".replace(".mp3"," Brainrot Edition.mp3")
                # Skip the making brainrot phase
            else:
                BrainrotSpeedSoFar = 8.0
                AllAlteredAudios = []
                for i in range(16):
                    if i == 0:
                        NewSoundName = SoundName.replace(".mp3",f" Brainrot Edition.mp3")
                    else:
                        NewSoundName = SoundName.replace(".mp3",f" Altered {i}.mp3")
                    output_audio = fr"{CurrentPath}\Brainrot Audio Cache\{NewSoundName}"
                    ChangeAudio(input_audio, output_audio, speed=BrainrotSpeedSoFar) # Makes audio based on new slow tempo
                    BrainrotSpeedSoFar -= 0.5
                    AllAlteredAudios.append(fr"{CurrentPath}\Brainrot Audio Cache\{NewSoundName}")

                Sound1Name = AllAlteredAudios[0] 
                Sound1 = AudioSegment.from_mp3(Sound1Name)
                AllAlteredAudios.pop(0) # Removes the file
                for AlteredAudio in AllAlteredAudios:
                    NextSound = AudioSegment.from_mp3(AlteredAudio)
                    Sound1 += NextSound # need ffprobe for this to work, but add all the file together
                    os.remove(AlteredAudio) # Remove the files
                Sound1.export(Sound1Name, format="mp3") # Makes the new file
                
            pygame.mixer.Sound(Sound1Name).play()
 
        elif SpeedChange != 1.0:
            NewSoundName = SoundName.replace(".mp3"," Altered.mp3")
            output_audio = fr"{CurrentPath}\{SoundFolder}\{NewSoundName}"
            ChangeAudio(input_audio, output_audio, speed=SpeedChange)
            pygame.mixer.Sound(output_audio).play()
            os.remove(output_audio)
        else:
            pygame.mixer.Sound(input_audio).play()
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
        UnmuteAvailable = pya.locateOnScreen(fr"{CurrentPath}\..\IceBarImages\UnmuteAvailable.png")
        pya.click(UnmuteAvailable)
    except:
        pass
    AllVoicelines = [] # List Initialization
    for Voiceline in os.listdir(fr"{CurrentPath}\{VoicelineFolderName}"): # Gets all files in the Voiceliens folder
        if VoicelineType in os.path.join(fr"{CurrentPath}\{VoicelineFolderName}", Voiceline): # If the type of voiceline is in the file name
            AllVoicelines.append(os.path.join(fr"{CurrentPath}\{VoicelineFolderName}", Voiceline)) # Add it to the list
    try:
        RandomVoiceLineChosen = random.choice(AllVoicelines)
        if "wav" in RandomVoiceLineChosen:
            PlayWaveFile(random.choice(AllVoicelines)) # Play a random sound from the type
        else:
            pygame.mixer.Sound(RandomVoiceLineChosen).play()
    except:
        print("Voiceline wasn't found.")

def StopSounds():
    if pygame.mixer.get_busy():
        pygame.mixer.stop()

# General Greeting (Good Morning/Afternoon and Greet)
def GeneralGreeting():
    CurrentDateandTime = datetime.datetime.now() # Gets time to determine whether Good Afternoon or Good Morning
    playVoiceLine("GoodMorning" if CurrentDateandTime.strftime("%p") == "AM" else "GoodAfternoon")
    playVoiceLine("Greeting")