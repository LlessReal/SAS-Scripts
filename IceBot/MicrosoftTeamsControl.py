from config import SpeakerArea,HeadPhoneArea,StereoMixArea,MicArea,SpeakerOptions,MicOptions
from pywinauto import Application
import time

# https://teams.microsoft.com/ - Microsoft teams website
# Change the Input Device on Microsoft Teams Call
def MicrosoftTeamsChangeDevice(Action=""):
    global SpeakingToClient
    if Action == "Speaking to Client": ChangeInputandOutput(Action); SpeakingToClient = True
    elif Action == "Listening to Client": ChangeInputandOutput(Action); SpeakingToClient = False

def ChangeInputandOutput(Action):
    # Launch or connect to Microsoft Teams
    app = Application(backend='uia').connect(title_re=".*Microsoft Teams.*")
    teams_window = app.window(title_re=".*Microsoft Teams.*")
    # Find and interact with the Speaker ComboBox
    if Action == "Speaking to Client":
        speaker_combo = teams_window.child_window(control_type="ComboBox", found_index=1)  # Adjust index if necessary
        speaker_combo.expand()
        speaker_combo.type_keys("{UP}" * SpeakerOptions)  # Adjust for correct device
        speaker_combo.type_keys("{DOWN}" * (SpeakerArea - 1))  # Adjust for correct device
        speaker_combo.type_keys("{ENTER}")
        speaker_combo = teams_window.child_window(control_type="ComboBox", found_index=2)  # Adjust index if necessary
        speaker_combo.expand()
        speaker_combo.type_keys("{UP}" * MicOptions)  # Adjust for correct device
        speaker_combo.type_keys("{DOWN}" * (StereoMixArea - 1))  # Adjust for correct device
        speaker_combo.type_keys("{ENTER}")
    elif Action == "Listening to Client":
        speaker_combo = teams_window.child_window(control_type="ComboBox", found_index=1)  # Adjust index if necessary
        speaker_combo.expand()
        speaker_combo.type_keys("{UP}" * SpeakerOptions)  # Adjust for correct device
        speaker_combo.type_keys("{DOWN}" * (HeadPhoneArea - 1))  # Adjust for correct device
        speaker_combo.type_keys("{ENTER}")
        speaker_combo = teams_window.child_window(control_type="ComboBox", found_index=2)  # Adjust index if necessary
        speaker_combo.expand()
        speaker_combo.type_keys("{UP}" * MicOptions)  # Adjust for correct device
        speaker_combo.type_keys("{DOWN}" * (MicArea - 1))  # Adjust for correct device
        speaker_combo.type_keys("{ENTER}")