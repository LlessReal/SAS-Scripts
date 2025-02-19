Welcome to IceBot, the auto call bot for IceBar

Before you use this program,
This is for python to run the commands that change the input devices via commandline
How to get working:
1. run Install-Module -Name AudioDeviceCmdlets -Scope CurrentUser on Powershell
2. pip install -r requirements.txt 
2.5. pip install -r SAS-Scripts/requirements.txt if in VSCode
3. pip install git+https://github.com/openai/whisper.git
4. Download ffmpeg 
Go to the ffmpeg install page, select your device, then select gyan.dev
https://www.gyan.dev/ffmpeg/builds/ - ffmpeg-git-full.7z
Download it, go to bin, and copy ffmpeg.exe and ffprobe.exe to the same folder as the main script (root folder if in VSCode, or same folder trial and error)
This both for the audio transcribing thing to work and the audio editing to work
5. Setup config
6. Get voicelines (Check other folders for examples)
7. Wallah !! 

run Get-PnpDevice -Class AudioEndpoint so that you can see all instance ids

???
Stop all sounds features
Get-PnpDevice -Class AudioEndpoint | Where-Object { $_.FriendlyName -eq "Internal Microphone (Synaptics HD Audio)" } | Disable-PnpDevice -Confirm:$false
Show Instance ID and stuff for certain microphone and shit
Get-PnpDevice -Class AudioEndpoint | Where-Object { $_.FriendlyName -eq "Internal Microphone (Synaptics HD Audio)" } | Format-List FriendlyName, InstanceId
It seems like a specific number will target someone depending on the measures
February 17th 2025
- Change Speed of Sound (I think)
- Brainrot mode


February 18th 2025
- Refresh Gui (Can change up files around then refresh wink wink)

git lfs install
pip install pip==21.3.1
pip install wheel setuptools pip --upgrade
C:\Users\marshall_miguel\AppData\Local\Programs\Python\Python311\python.exe -m pip install wheel setuptools pip --upgrade

pip install -vvv torch
pip install numpy
pip3 install --pre torch -f https://download.pytorch.org/whl/nightly/cpu/torch_nightly.html