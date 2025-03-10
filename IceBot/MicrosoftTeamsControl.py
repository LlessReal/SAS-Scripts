from config import SpeakerArea,HeadPhoneArea,StereoMixArea,MicArea,SpeakerOptions,MicOptions
from pywinauto import Application

# https://teams.microsoft.com/ - Microsoft teams website
# Change the Input Device on Microsoft Teams Call
def MicrosoftTeamsChangeDevice(Action=""):
    global SpeakingToClient
    ChangeInputandOutput(Action)
    if Action == "Speaking to Client": SpeakingToClient = True
    elif Action == "Listening to Client": SpeakingToClient = False

def ChangeInputandOutput(Action):
    # Launch or connect to Microsoft Teams
    app = Application(backend='uia').connect(title_re=".*Settings.*")
    teams_window = app.window(title_re=".*Settings.*")
    #icebarapp = Application(backend='uia').connect(title_re=".*iceBar.*")
    #icebarwindow = icebarapp.window(title_re=".*iceBar.*")
    # Find and interact with the Speaker ComboBox
    if Action == "Speaking to Client":
        speaker_combo = teams_window.child_window(control_type="ComboBox", found_index=1)  # Adjust index if necessary
        speaker_combo.expand()
        speaker_combo.type_keys("{UP}" * SpeakerOptions)  # Adjust for correct device
        speaker_combo.type_keys("{DOWN}" * (SpeakerArea - 1))  # Adjust for correct device
        speaker_combo.type_keys("{ENTER}")
    elif Action == "Listening to Client":
        speaker_combo = teams_window.child_window(control_type="ComboBox", found_index=1)  # Adjust index if necessary
        speaker_combo.expand()
        speaker_combo.type_keys("{UP}" * SpeakerOptions)  # Adjust for correct device
        speaker_combo.type_keys("{DOWN}" * (HeadPhoneArea - 1))  # Adjust for correct device
        speaker_combo.type_keys("{ENTER}")
        #MuteButton = icebarwindow.child_window(title="Mute", auto_id="MuteButton_1", control_type="Button")
        #MuteButton.click_input()
        #UnmuteButton = icebarwindow.child_window(title="Unmute", auto_id="UnmuteButton_1", control_type="Button")
        #UnmuteButton.click_input()
    elif Action == "Change to Stereo":
        speaker_combo = teams_window.child_window(control_type="ComboBox", found_index=2)  # Adjust index if necessary
        speaker_combo.expand()
        speaker_combo.type_keys("{UP}" * MicOptions)  # Adjust for correct device
        speaker_combo.type_keys("{DOWN}" * (StereoMixArea - 1))  # Adjust for correct device
        speaker_combo.type_keys("{ENTER}")
    elif Action == "Switch to Human":
        speaker_combo = teams_window.child_window(control_type="ComboBox", found_index=2)  # Adjust index if necessary
        speaker_combo.expand()
        speaker_combo.type_keys("{UP}" * MicOptions)  # Adjust for correct device
        speaker_combo.type_keys("{DOWN}" * (MicArea - 1))  # Adjust for correct device
        speaker_combo.type_keys("{ENTER}")