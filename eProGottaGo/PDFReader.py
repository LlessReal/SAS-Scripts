import clipboard as cb 
import config
from PyPDF2 import PdfReader

AllTextFromeProDoc = "" # Extract text from each page
for eProDoc in config.eProDocs: # Goes through each document in the list of documents you placed
    Reader = PdfReader(f"{config.CurrentPath}\\Documents\\{eProDoc}") # Gets pdf file
    for page in Reader.pages: # Goes through each page of document
        AllTextFromeProDoc += page.extract_text() # Stores all text from the page intos AllTextFromDoc
    
# we're reading all the pages from each doc ya 

# Check if text grabbed is still empty
if AllTextFromeProDoc == "":
    exit("Why is the documents folder empty.")

# Function that checks if the Req ID is in the document
def CheckForSRNum(ReqID):
    if AllTextFromeProDoc.find(ReqID) == -1: # If the ID wasn't found in the text
        print(f"No SR for {ReqID}") # If error didn't occur above, no SR was found
        cb.copy(f"{ReqID} (No SR Found)") # Copies Status
        return "No SR"
    else:
        print(f"SR Found for {ReqID}") # If no box was found, SR is there
        cb.copy(f"{ReqID} (SR Found)") # Copies Status
        return "SR Found"