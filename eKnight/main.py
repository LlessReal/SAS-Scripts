import MyCSUAutoLogin
import PDFReader

def main():
    MyCSUAutoLogin.StartUpBrowser()
    PDFReader.ReadFiles()
    print("All documents complete !!")

if __name__ == "__main__":
    main()