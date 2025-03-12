import os,sys
ToolsPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'..', 'Tools'))
if ToolsPath not in sys.path: sys.path.append(ToolsPath)
# Post Config
CurrentPath = os.path.dirname(__file__) 
MyCSUUser, MyCSUPassword = "marshall_miguel@columbusstate.edu", "Ll3ss1@3$5^Ll3ss1@3$5^"
ExcelDocURL = r"https://colstate-my.sharepoint.com/:x:/r/personal/smith_barbara9_columbusstate_edu/_layouts/15/Doc.aspx?sourcedoc=%7B393213BA-2679-4C4F-BCFF-397B856FA80E%7D&file=Check%20Vendors%20as%20of%202.28.25.xlsx&fromShare=true&action=default&mobileredirect=true"
OneDriveURL = r"https://colstate-my.sharepoint.com/personal/smith_barbara9_columbusstate_edu/_layouts/15/onedrive.aspx?e=5%3A8449d9ab126840cd821a3fbe410a0a13&web=1&openShare=true&fromShare=true&at=9&CT=1741809880917&OR=OWA%2DNT%2DMail&CID=67cfa693%2D6549%2De4c9%2Dc931%2De51da556fe48&id=%2Fpersonal%2Fsmith%5Fbarbara9%5Fcolumbusstate%5Fedu%2FDocuments%2FUITS%2FSpecial%20Projects%2FPurchasing%2FFY25&FolderCTID=0x012000344D8BC79006874A9000CF6E7CD3F4EC&view=0"