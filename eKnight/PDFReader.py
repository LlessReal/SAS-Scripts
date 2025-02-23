import clipboard as cb 
import config
from PyPDF2 import PdfReader
import os

# Function that checks if the Req ID is in the document
def CheckForSRNum():
    if AllTextFromDoc.find("SR") == -1: # If the ID wasn't found in the text
        print(f"No SR Number detected") # If error didn't occur above, no SR was found
        return "No SR"
    else:
        return "SR Found"
    
AllTextFromDoc = "" # Extract text from each page
for AramarkInvoiceDoc in config.AramarkInvoices: # Goes through each document in the list of documents you placed
    Reader = PdfReader(f"{config.CurrentPath}\\Documents\\{AramarkInvoiceDoc}") # Gets pdf file
    for page in Reader.pages: # Goes through each page of document
        AllTextFromDoc += page.extract_text() # Stores all text from the page intos AllTextFromDoc
    print(AllTextFromDoc)
    #FullSRName = ""
    #os.rename(f"{config.CurrentPath}\\Documents\\{AramarkInvoiceDoc}",f"{config.CurrentPath}\\Documents\\{FullSRName}.pdf")
    input("")
    #CheckForSRNum()

# Check if text grabbed is still empty
if AllTextFromDoc == "":
    exit("Why is the Aramark Invoices folder empty.")

