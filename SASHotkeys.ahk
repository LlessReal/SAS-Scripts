#Requires AutoHotkey v2.0

if WinActive("C:\Windows\system32\notepad.exe") {
  ~ctrl & r:: Reload
} ; If notepad.exe is open, Ctrl + R will reload the script (Save first tho)

; COMMANDS SO FAR
+RButton::QuickTransfer() ; Runs function that transfer callers
~ctrl & RButton::ToolbarArrow() ; Runs function that clicks the IceBar Arrow on the top right
~Ctrl & 1::NotifySuppMsgMaker() ; Runs the function that creates a message to inform support specialists about invoices
~Ctrl & 2::Send "Ready For Processing" ; # Sends "Ready For Processing" lol , nothing more

NotifySuppMsgMaker() {
  global SerialNum := InputBox("Enter the serial number.", "Serial Number", "w500 h100")
  global SupportName := InputBox("Enter the support person's name.", "Support Person", "w500 h100")
  Send "Hello, " SupportName.Value ". Please see the Aramark invoice for SR" SerialNum.Value " attached for payment processing."
  Send "{Enter}{Enter}"
  Send "Thanks,"
  Send "{Enter}"
  Send "Miguel" ; For some reason, spaces are added after {enter} sooooooo yea
}

QuickTransfer() {
  ActiveHwnd := WinExist("A") ; Gets current ID of active window and stores it
  MouseGetPos &x, &y ; Gets X and Y Coordinate of mouse and stores those into variables x and y
  global TransferNum := InputBox("Enter the phone number that the customer would like to be transferred towards.", "Phone Number Transfer", "w500 h100")
  if TransferNum.Result != "Cancel" {
    ToolbarArrow()
    TransferStart := Transfer()
    if TransferStart = "Not Active" {
      MsgBox "You are not currently in a call."
      WinActivate "ahk_id " ActiveHwnd ; Return back to original window
      MouseMove x, y ; Moves back the position you were initially at
      Sleep 200
      Send "{Shift Up}" ; Additional command to release shift to avoid issues
      Exit
    }
    ToolbarArrow()
    if WinActive("ahk_exe iceBar.exe") {
      WinActivate "ahk_id " ActiveHwnd ; Return back to original window
      MouseMove x, y ; Moves back the position you were initially at
      WinClose "ahk_exe ms-teams.exe" ; Closes the calling window (Because for some reason this prioritizes that and not the main window)
      Sleep 200
      Send "{Shift Up}" ; Additional command to release shift to avoid issues
    }   
    else {
      MsgBox "Fail. Idk what happened but try again"
    }
  }
  Return
}

ToolbarArrow() { ; Opening Icebar Toolbar Function
  while true {
    if WinActive("ahk_exe iceBar.exe") {
      MouseMove 1080, 40, 20 ; Moves mouse back to Icebar drop down
      Send "{LButton}" ; Presses click
      Sleep 250
      break
    }    
    else {
      WinActivate "ahk_exe iceBar.exe" ; Activates to iceBar toolbar at the top
      continue
    }
  }
}

Transfer() { ; Opening Transfer Function
  MouseMove 612, 108 ; Moves mouse to Transfer coordinate (directly on the arrow, use window spy)
  Sleep 100
  if PixelGetColor(612,108) = 0xF5F5F5 { ; If the transfer arrow thing is gray, do this (Same coordinates)
    return "Not Active"
  }
  Send "{LButton}"
  Sleep 400
  Send TransferNum.Value "{Enter}" ; Types whatever number i inputted
}