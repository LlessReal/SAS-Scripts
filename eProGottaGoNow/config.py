import os
ColumnDistance = 4 # Shifts this amount of times to go to each box , do ur math kiddos
ReqIDColumnOnTheLeft = True # If it's on the left, else it's from the right
CurrentPath = os.path.dirname(__file__) 

# Post Config
eProDocs = [f"{CurrentPath}\\..\\ePro Documents\\{Doc}" for Doc in os.listdir(f"{CurrentPath}\\..\\ePro Documents")] # Gets all documents from the documents folder
AllColors = ["Orange","Yellow","Green","Blue","Purple"]

try:
    open(f"{CurrentPath}\\NextColor.txt","x").close()
    with open(f"{CurrentPath}\\NextColor.txt","w") as f:
        f.write("Orange")
except:
    pass

