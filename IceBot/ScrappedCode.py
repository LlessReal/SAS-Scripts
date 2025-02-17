# Formerly, if brainrot mode was on itwould play all the files created before deleting them, but then i found i way to sorta add em together sooooo
if BrainrotModeActivated == 1: # No for now lol
    BrainrotSpeedSoFar = 16.0
    for i in range(6):
        NewSoundName = SoundName.replace(".mp3",f" Altered {i}.mp3")
        output_audio = fr"{CurrentPath}\Custom Sounds\{NewSoundName}"
        ChangeAudio(input_audio, output_audio, speed=BrainrotSpeedSoFar) # Makes audio based on new slow tempo
        BrainrotSpeedSoFar /= 2.0
        
    AllAlteredAudios = [x for x in os.listdir(fr"{CurrentPath}\Custom Sounds") if "Altered" in x]
    AllAlteredAudios.sort()
    for AlteredAudio in AllAlteredAudios:
        SoundPlaying = pygame.mixer.Sound(fr"{CurrentPath}\Custom Sounds\{AlteredAudio}").play()
        os.remove(fr"{CurrentPath}\Custom Sounds\{AlteredAudio}")
        while SoundPlaying.get_busy():
            pass     