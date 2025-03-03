import os, main

MyCSUUser,MyCSUPassword = "marshall_miguel@columbusstate.edu", "Ll3ss1@3$5^Ll3ss1@3$5^"
PDFRecognitionMethod = "NewOCR" # Adobe, OnlineOCR, NewOCR 
# honorable (not rlly) mentions: https://www.adobe.com/acrobat/online/ocr-pdf.html , https://www.ocr2edit.com/
TestingProgram = False
# Post Config shit
# Gets all PDF documents from the Aramark Invoices folder
AramarkInvoices = [f"{main.CurrentPath}\\Aramark Invoices\\{Invoice}" for Invoice in os.listdir(f"{main.CurrentPath}\\Aramark Invoices") if "pdf" in Invoice] 