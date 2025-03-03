import os, main

MyCSUUser,MyCSUPassword = "", "" # User, Password
PDFRecognitionMethod = "Adobe" # Adobe, Online
TestingProgram = False
# Post Config shit
# Gets all PDF documents from the Aramark Invoices folder
AramarkInvoices = [f"{main.CurrentPath}\\Aramark Invoices\\{Invoice}" for Invoice in os.listdir(f"{main.CurrentPath}\\Aramark Invoices") if "pdf" in Invoice] 