import os, re, eQuestBrowsing, config, Tools.BrowserControl, Tools.PDFReader, time

CurrentPath = os.path.dirname(__file__) 
def main():
    Tools.BrowserControl.MyCSUAutoLogin(config.MyCSUUser,config.MyCSUPassword) # Login
    for AramarkInvoice in config.AramarkInvoices: # Goes through each document in the list of documents you placed
        AllTextFromInvoice = Tools.PDFReader.GetPDFText(AramarkInvoice,config.PDFRecognitionMethod,CurrentPath=CurrentPath)
        Tools.BrowserControl.eQuestMainPage() # Return to page
        
        # FINDING THE SR NUMBER
        # Find all 6 digit numbers that starts with 3 in the document
        PotentialSRNumbers = [Num for Num in re.findall(r'3\d{5}', AllTextFromInvoice) if not AllTextFromInvoice[AllTextFromInvoice.find(Num):7].isdigit()]
        print(f"All 6 Digit Numbers that start with 3: {PotentialSRNumbers}" if PotentialSRNumbers != [] else "We got nothin")
        if len(PotentialSRNumbers) > 1: input("Found 2 6-digit numbers that start with 3, check up on that")
        # If it's empty, put it in Failures folder
        if PotentialSRNumbers == []:  os.rename(AramarkInvoice,AramarkInvoice.replace("\\Aramark Invoices\\","\\Aramark Invoices\\Failure\\"))
        else:
            # we got an SR Number, i think
            SRNum = f"{PotentialSRNumbers[0]}"
            print(f"{SRNum} is the SR Number")                
            SRNumAndAllAfter = AllTextFromInvoice[AllTextFromInvoice.find(SRNum):]
            FullSRNameMaybe = "SR" + SRNumAndAllAfter[0:SRNumAndAllAfter.find(" ")].replace(f"/","-")
            print(f"{FullSRNameMaybe} is the full SR name (maybe), file will be renamed to that.")
            os.rename(AramarkInvoice,f"{CurrentPath}\\Aramark Invoices\\{FullSRNameMaybe}.pdf")
            eQuestBrowsing.SearchSRNum(SRNum)
            eQuestBrowsing.AttachPDFtoTicket(f"{CurrentPath}\\Aramark Invoices\\{FullSRNameMaybe}.pdf")
            eQuestBrowsing.NotifySupport(SRNum)
            print("We did it !! - Dora !!") # Put in Success folder
            os.rename(f"{CurrentPath}\\Aramark Invoices\\{FullSRNameMaybe}.pdf",f"{CurrentPath}\\Aramark Invoices\\Successfully Sent\\{FullSRNameMaybe}.pdf")
            # LOOP
    print("All documents complete !!") # When we're done boom

if __name__ == "__main__": main()