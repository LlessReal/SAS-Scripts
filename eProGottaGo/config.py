import os
ColumnDistance = 4 # Shifts this amount of times to go to each box , do ur math kiddos
ReqIDColumnOnTheLeft = True # If it's on the left, else it's from the right
ExcelSheetName = "BOR_POAP" # Doesn't have to be the full thing, but enough to distinguish it from other windows
eProDocName = "Manage Requisitions" # Same thing, but put the window in the middle monitor or it wont work
FulleProDocName = "Manage Requisitions. Sept to November"

# Post Config
CurrentPath = os.path.dirname(__file__) # Gonna need this