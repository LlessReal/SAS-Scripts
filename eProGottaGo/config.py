import os
ColumnDistance = 4 # Shifts this amount of times to go to each box , do ur math kiddos
# Saves: 4 - Practice , 1 - New
ReqIDColumnOnTheLeft = True # If it's on the left, else it's from the right
ShowText = True

# Post Config
CurrentPath = os.path.dirname(__file__) # Gonna need this
eProDocs = os.listdir(f"{CurrentPath}\\Documents") # Gets all documents from the documents folder

AllColors = ["Orange","Yellow","Green","Blue","Purple"]

try:
    open(f"{CurrentPath}\\NextColor.txt","x").close()
    with open(f"{CurrentPath}\\NextColor.txt","w") as f:
        f.write("Orange")
except:
    pass