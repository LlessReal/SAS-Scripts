import os, pygame, config, random, threading, time
#pygame.mixer.init() # For debugging
#pygame.mixer.set_num_channels(22)

num_channels = pygame.mixer.get_num_channels()
print(f"Number of available channels: {num_channels}")
MusicPlaylist = os.listdir(f"{config.CurrentPath}\\Wait Music Playlist")
channel21 = pygame.mixer.Channel(21)
channel21.set_volume(0) # Initially radio is off

def MusicChanging():
    while True: # Loop that changes song when song stops
        MusicToBePlayed = pygame.mixer.Sound(f"{config.CurrentPath}\\Wait Music Playlist\\{random.choice(MusicPlaylist)}")
        channel21.play(MusicToBePlayed)
        while channel21.get_busy(): pygame.time.wait(100)  # Wait for 100 milliseconds to avoid busy-waiting
        
threading.Thread(target=MusicChanging).start()

def RadioControl(RadioAction=""):
    if RadioAction == "On": channel21.set_volume(1)
    elif RadioAction == "Off": channel21.set_volume(0)
    elif RadioAction == "Change Song": channel21.stop()

#while True:
#    input("Turn it on"); ToggleRadio("On")
#    input("Turn it off"); ToggleRadio("Off")
#    channel21.stop()
