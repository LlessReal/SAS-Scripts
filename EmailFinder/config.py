import os,sys
ToolsPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'..', 'Tools'))
if ToolsPath not in sys.path: sys.path.append(ToolsPath)
# Post Config
CurrentPath = os.path.dirname(__file__) 
MyCSUUser, MyCSUPassword = "marshall_miguel@columbusstate.edu", "Ll3ss1@3$5^Ll3ss1@3$5^"
ExcelDocURL = r"https://colstate-my.sharepoint.com/:x:/r/personal/smith_barbara9_columbusstate_edu/_layouts/15/Doc.aspx?sourcedoc=%7B393213BA-2679-4C4F-BCFF-397B856FA80E%7D&file=Check%20Vendors%20as%20of%202.28.25.xlsx&fromShare=true&action=default&mobileredirect=true"
OneDriveURL = r"https://colstate-my.sharepoint.com/:f:/r/personal/smith_barbara9_columbusstate_edu/Documents/UITS/Special%20Projects/Purchasing/FY25?csf=1&web=1&e=Otngsl"
DownloadsPath = r"C:\Users\marshall_miguel\Downloads"