import os

MyCSUUser = ""
MyCSUPassword = ""
PDFRecognitionMethod = "Online" # Adobe or Online
# Post Config shit
CurrentPath = os.path.dirname(__file__)
AramarkInvoices = os.listdir(f"{CurrentPath}\\Aramark Invoices") # Gets all documents from the documents folder
for file in AramarkInvoices:
    if "pdf" not in file: # Ignore folders and non-files
        AramarkInvoices.remove(file) # Remove it from list pretty much