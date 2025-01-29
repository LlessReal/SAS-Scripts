import tkinter as tk
from tkinter import messagebox
# Don't name the file tinker...,.,.
root = tk.Tk() # Creates main window
root.wait_visibility() # Wait until the label becomes visible
root.geometry("240x75") # Sets the window size

# declaring string variable
# for storing name and password

def submit():
    print("The name is : " + name_var.get())
    print("The password is : " + passw_var.get())
    name_var.set("")
    passw_var.set("")

name_label = tk.Label(root, text = 'Username', font=('calibre',10, 'bold'))
name_var=tk.StringVar()
name_entry = tk.Entry(root,textvariable = name_var, font=('calibre',10,'normal'))

passw_label = tk.Label(root, text = 'Password', font = ('calibre',10,'bold'))
passw_var=tk.StringVar()
passw_entry=tk.Entry(root, textvariable = passw_var, font = ('calibre',10,'normal'))
 
sub_btn=tk.Button(root,text = 'Submit', command = submit) # creating a button using the widget , it will call the submit function
 
# placing the label and entry in the required position using grid method
name_label.grid(row=0,column=0)
name_entry.grid(row=0,column=1)
passw_label.grid(row=1,column=0)
passw_entry.grid(row=1,column=1)
sub_btn.grid(row=2,column=1)

root.mainloop() # Keeps the Tkinter event loop running to make gui elements work right