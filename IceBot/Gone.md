git lfs install
pip install pip==21.3.1
pip install wheel setuptools pip --upgrade
C:\Users\marshall_miguel\AppData\Local\Programs\Python\Python311\python.exe -m pip install wheel setuptools pip --upgrade

run Get-PnpDevice -Class AudioEndpoint so that you can see all instance ids

???
Stop all sounds features
Get-PnpDevice -Class AudioEndpoint | Where-Object { $_.FriendlyName -eq "Internal Microphone (Synaptics HD Audio)" } | Disable-PnpDevice -Confirm:$false
Show Instance ID and stuff for certain microphone and shit
Get-PnpDevice -Class AudioEndpoint | Where-Object { $_.FriendlyName -eq "Internal Microphone (Synaptics HD Audio)" } | Format-List FriendlyName, InstanceId