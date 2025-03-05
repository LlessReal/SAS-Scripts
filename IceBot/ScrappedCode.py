import os
# Formerly, if brainrot mode was on itwould play all the files created before deleting them, but then i found i way to sorta add em together sooooo
if BrainrotModeActivated == 1: # No for now lol
    BrainrotSpeedSoFar = 8
    for i in range(15):
        NewSoundName = SoundName.replace(".mp3",f" Altered {i}.mp3")
        output_audio = fr"{CurrentPath}\Custom Sounds\{NewSoundName}"
        ChangeAudio(input_audio, output_audio, speed=BrainrotSpeedSoFar) # Makes audio based on new slow tempo
        BrainrotSpeedSoFar -= 0.5
        
    AllAlteredAudios = [x for x in os.listdir(fr"{CurrentPath}\Custom Sounds") if "Altered" in x]
    AllAlteredAudios.sort()
    for AlteredAudio in AllAlteredAudios:
        SoundPlaying = pygame.mixer.Sound(fr"{CurrentPath}\Custom Sounds\{AlteredAudio}").play()
        os.remove(fr"{CurrentPath}\Custom Sounds\{AlteredAudio}")
        while SoundPlaying.get_busy():
            pass     

# Apparently changing the system settings don't affect microsoft's settings sooo good bye !!
RegularInputDeviceName = "Internal Microphone (Synaptics HD Audio)" # Replace with the exact name | Saves: Microphone (Realtek(R) Audio), Internal Microphone (Synaptics HD Audio)
StereoInputDeviceName = "Stereo Mix (Synaptics HD Audio)" # Same Thing | Saves: Stereo Mix (Synaptics HD Audio)

def ChangeToRegularMic():
    os.system(fr'powershell -Command "& {{(Get-AudioDevice -List | Where-Object {{ $_.Name -like \"{RegularInputDeviceName}\" }}) | Set-AudioDevice }}"')

def ChangeToStereoMix():
    os.system(fr'powershell -Command "& {{(Get-AudioDevice -List | Where-Object {{ $_.Name -like \"{StereoInputDeviceName}\" }}) | Set-AudioDevice }}"')
# Gui Maker
# Regular Mic Toggle Button
RegularMicToggle = Button( root, text="Turn on Regular Mic", bg="purple",fg="white",command= ChangeToRegularMic) 
RegularMicToggle.grid(row=9 + NextInLine,column=0)
# Stereo Mix Toggle Button
StereoToggle = Button( root, text="Turn on Stereo Mix", bg="purple",fg="white",command= ChangeToStereoMix) 
StereoToggle.grid(row=9 + NextInLine,column=1)



def ChangeInputandOutput(StereoMixArea,SpeakerArea):
    try:
        MicrosoftDropDown = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\MicrosoftDropDown.png')
        pya.click(MicrosoftDropDown); time.sleep(0.5)
    except: print("Couldn't find Microsoft Dropdown :("); return
    for i in range(3): pya.press("tab")
    time.sleep(1)
    for i in range(StereoMixArea - 1): pya.press("tab") # Tab onto the correct Incoming Audio Choice
    time.sleep(0.5); pya.press('enter') # Wait then press enter
    try:
        MicrosoftDropDown = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\MicrosoftDropDown.png')
        pya.click(MicrosoftDropDown); time.sleep(0.5)
    except: print("Couldn't find Microsoft Dropdown :("); return

    # Now change to speaker
    try:
        MicrosoftDropDown = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\MicrosoftDropDown.png')
        pya.click(MicrosoftDropDown); time.sleep(0.5)
    except: print("Couldn't find Microsoft Dropdown :("); return
    for i in range(7): pya.press("tab")
    time.sleep(1)
    for i in range(SpeakerArea - 1): pya.press("tab") # Tab onto the correct Incoming Audio Choice
    time.sleep(0.5); pya.press('enter') # Wait then press enter
    try:
        MicrosoftDropDown = pya.locateOnScreen(fr'{CurrentPath}\..\IceBarImages\MicrosoftDropDown.png')
        pya.click(MicrosoftDropDown); time.sleep(0.5)
    except: print("Couldn't find Microsoft Dropdown :("); return