import sys, os
ToolsPath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Tools'))
if ToolsPath not in sys.path: sys.path.append(ToolsPath)

Choice = int(input("Choose Your Program: 1 - eKnight 2 - eProGottaGo"))

AllPrograms = ["eKnight","eProGottaGo"]
# Get the absolute path to the Blue folder
if Choice != 2:
    FolderPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', f'SAS-Scripts\\{AllPrograms[Choice - 1]}'))
    if FolderPath not in sys.path: sys.path.append(FolderPath)
if Choice == 1:
    import eKnight.main
    eKnight.main.main()
elif Choice == 2:
    Choice = int(input("Choose Mode: 1 - eProGottaGo 2 - eProGottaGoNow"))
    if Choice == 1:
        FolderPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', f'SAS-Scripts\\eProGottaGo'))
        if FolderPath not in sys.path: sys.path.append(FolderPath)
        import eProGottaGo.main
    elif Choice == 2:
        FolderPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', f'SAS-Scripts\\eProGottaGoNow'))
        if FolderPath not in sys.path: sys.path.append(FolderPath)
        import eProGottaGoNow.main