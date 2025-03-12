import os
ColumnDistance = 4 # Shifts this amount of times to go to each box , do ur math kiddos
ReqIDColumnOnTheLeft = True # If it's on the left, else it's from the right

# Post Config
CurrentPath = os.path.dirname(__file__) 
eProDocs = [f"{CurrentPath}\\..\\ePro Documents\\{Doc}" for Doc in os.listdir(f"{CurrentPath}\\..\\ePro Documents\\")] # Gets all documents from the documents folder
MyCSUUser, MyCSUPassword = "", ""
ExcelDocURL = r"https://colstate-my.sharepoint.com/:x:/r/personal/tinsley_kele_columbusstate_edu1/_layouts/15/doc2.aspx?sourcedoc=%7BBDF92665-7B45-42C7-8757-0B5F01B42943%7D&file=BOR_POAP_DETAIL_CSU_1269485841._1.28.25%20updated_Miguel.xlsx&action=default&mobileredirect=true&DefaultItemOpen=1&ct=1740789519685&wdOrigin=OFFICECOM-WEB.START.EDGEWORTH&cid=60935c83-2f53-45f4-b435-129f545a0ebb&wdPreviousSessionSrc=HarmonyWeb&wdPreviousSession=a1e96881-7572-4284-9cfc-4d1032862af0"
AllColors = ["Orange","Yellow","Green","Blue","Purple"]

try:
    open(f"{CurrentPath}\\NextColor.txt","x").close()
    with open(f"{CurrentPath}\\NextColor.txt","w") as f: f.write("Orange")
except: pass