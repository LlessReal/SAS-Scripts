import os, main

MyCSUUser,MyCSUPassword = "", ""
PDFRecognitionMethod = "NewOCR" # OnlineOCR, NewOCR 
# honorable (not rlly) mentions: https://www.adobe.com/acrobat/online/ocr-pdf.html , https://www.ocr2edit.com/
TestingProgram = False
# Post Config shit
# Gets all PDF documents from the Aramark Invoices folder
AramarkInvoices = [f"{main.CurrentPath}\\Aramark Invoices\\{Invoice}" for Invoice in os.listdir(f"{main.CurrentPath}\\Aramark Invoices") if "pdf" in Invoice] 