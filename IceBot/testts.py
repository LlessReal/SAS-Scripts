import pyttsx3
from time import sleep

engine = pyttsx3.init() # Initialize the engine
print(engine.getProperty('voices'))
# Adjust speaking rate
rate = engine.getProperty('rate')
engine.setProperty('rate', 100)
rate = engine.getProperty('rate') # Doesn't work right for some reason
print(f'Current speaking rate: {rate}')

# Adjust volume
volume = engine.getProperty('volume')
print(f'Current volume level: {volume}')
engine.setProperty('volume', 1.0)

# Change voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Selecting a female voice

# Make the engine speak
engine.say(f"Hello World! My current speaking rate is {rate}")
engine.runAndWait()

engine.stop() # Stop the engine