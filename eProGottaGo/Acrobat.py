import clipboard as cb 
import config
from PyPDF2 import PdfReader

AllTextFromDoc = "" # Extract text from each page
for eProDoc in config.eProDocs: # Goes through each document in the list of documents you placed
    Reader = PdfReader(f"{config.CurrentPath}\\Documents\\{eProDoc}") # Gets pdf file
    for page in Reader.pages: # Goes through each page of document
        AllTextFromDoc += page.extract_text() # Stores all text from the page intos AllTextFromDoc

# Check if text grabbed is still empty
if AllTextFromDoc == "":
    exit("Why is the documents folder empty.")

# Function that checks if the Req ID is in the document
def CheckForSRNum(ReqID):
    if AllTextFromDoc.find(ReqID) == -1: # If the ID wasn't found in the text
        print(f"No SR for {ReqID}") # If error didn't occur above, no SR was found
        cb.copy(f"{ReqID} (No SR Found)") # Copies Status
        return "No SR"
    else:
        print(f"SR Found for {ReqID}") # If no box was found, SR is there
        cb.copy(f"{ReqID} (SR Found)") # Copies Status
        return "SR Found"