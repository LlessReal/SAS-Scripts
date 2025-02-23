import os
ColumnDistance = 4 # Shifts this amount of times to go to each box , do ur math kiddos
ReqIDColumnOnTheLeft = True # If it's on the left, else it's from the right

# Post Config
CurrentPath = os.path.dirname(__file__) # Gonna need this
eProDocs = os.listdir(f"{CurrentPath}\\Documents") # Gets all documents from the documents folder