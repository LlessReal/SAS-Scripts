import os, main

MyCSUUser, MyCSUPassword = "", "" # User, Password
PDFRecognitionMethod = "Online" # Adobe, Online
TestingProgram = True
# Post Config shit
# Gets all PDF documents from the Aramark Invoices folder
AramarkInvoices = [f"{main.CurrentPath}\\Aramark Invoices\\{Invoice}" for Invoice in os.listdir(f"{main.CurrentPath}\\Aramark Invoices") if "pdf" in Invoice] 