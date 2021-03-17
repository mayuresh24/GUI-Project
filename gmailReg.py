import tkinter as tk
import mysql.connector
from tkinter import messagebox
import datetime
from datetime import datetime
from datetime import date
import re
import clx.xms
import requests
from tkinter import *
from pytube import YouTube
from tkinter import filedialog
import os
import tkinter
from PIL import Image, ImageTk
from tkinter.ttk import *


root=tk.Tk()
root.iconbitmap('mail.ico')
root.resizable(False,False)
root.configure(background='blue')
window_height = 170
window_width = 300

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))



db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="zomato"
    )

name_var=tk.StringVar()
contact_var=tk.StringVar()
email_var=tk.StringVar()
password_var=tk.StringVar()

def register():
    global contact_db
    today = date.today()
    now = datetime.now()

    name_db=name_entry.get()
    contact_db=contact_entry.get()
    email_db=email_entry.get()
    password_db=password_entry.get()
    date_db =today.strftime("%d/%m/%Y")
    time_db=now.strftime("%H:%M:%S")

    
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    # compiling regex 
    pat = re.compile(reg) 
    # searching regex				 
    mat = re.search(pat, password_db)

    namelen=len(name_db)
    emaillen=len(email_db)
    passlen=len(password_db)
    maxlen=len(contact_db)

    if(namelen!=0) or (emaillen!=0) or (passlen!=0):
        if(name_db.isalpha()) or (name_db.find(" ") !=-1):
            if(maxlen==10) or (maxlen==11):
                if(email_db.find("@") !=-1) and (email_db.find(".")!=-1):
                    if mat:
                     curs=db.cursor()
                     val=(name_db, contact_db,email_db,password_db,date_db,time_db)
                     curs.execute("insert into user(name,contact,email,password,date,time) values(%s,%s,%s,%s,%s,%s)",val)
                     db.commit()
                     name_entry.delete(0, 'end')
                     contact_entry.delete(0, 'end')
                     email_entry.delete(0, 'end')
                     password_entry.delete(0, 'end')
                     os.system("gmailDashboard.py")
                    else:
                        messagebox.showinfo("Message","Invalid Password")
                else:
                    messagebox.showinfo("Message","Invalid EMail")
            else:
                messagebox.showinfo("Message","Invalid Contact")
        else:
            messagebox.showinfo("Message","Invalid Name")
    else:
        messagebox.showinfo("Message","All Fields are mandatory")
                    
                 
def verify():
    contact_db=contact_entry.get()
    maxlen=len(contact_db)
    if(maxlen==10):
        global userInput
        import random
        global rnd_num
        #global contact_db
        global otp
        cdb="91"+contact_db
        final={cdb}#Coverting string to sets is like this , here cdb was string after enclosing it in {} it became sets
        dice_range = (1000,6000)
        roll = random.randint(*dice_range)
        client = clx.xms.Client(service_plan_id='c830f8a982cd4a57981f6ab7822ec7aa', token='8b305955301c403288d2e7464f0bd976')
        create = clx.xms.api.MtBatchTextSmsCreate()
        create.sender = '447537404817'
        create.recipients =final#{'7773902008'}
        rnd_num=create.body =roll
        otp=str(rnd_num)
        try:
            batch = client.create_batch(create)
        except(requests.exceptions.RequestException,clx.xms.exceptions.ApiException) as ex:
            print('Failed to communicate with XMS: %s' % str(ex))
        
        def otp_process():
            global userInput
            userInput=e1.get()
            global otp
            if(userInput==otp):
                if (sub_btn['state'] ==NORMAL)and(name_entry['state'] ==NORMAL)and(email_entry['state']==NORMAL)and(password_entry['state']==NORMAL):
                    name_entry['state'] =DISABLED
                    sub_btn['state'] =DISABLED
                    password_entry['state'] =DISABLED
                    email_entry['state'] =DISABLED
                else:
                    sub_btn['state'] =NORMAL
                    name_entry['state'] =NORMAL
                    email_entry['state'] =NORMAL
                    password_entry['state'] =NORMAL
                
            
            else:
                messagebox.showinfo("Message","Incorrect OTP")
            otp_btn.grid_forget()
            e1.grid_forget()
            check_btn.grid_forget()#To destroy any widget we use grid_forget()or pack_forget
            if (contact_entry['state'] ==NORMAL):
                contact_entry['state'] =DISABLED
            else:
                contact_entry['state'] =NORMAL        
        e1=tk.Entry(root)
        e1.grid(row=10,column=3)
        otp_btn=tk.Button(root,text="CHECK",command=otp_process)
        otp_btn.grid(row=12,column=3)
    else:
        messagebox.showinfo("Message","You must fill contact")
    
      
def only_characters(char):
    return char.isalpha()

def only_numbers(char):
    return char.isdigit()

vldalpha=root.register(only_characters)
vlddigit=root.register(only_numbers)
   
name_label=tk.Label(root,text="Enter Name",bg="blue",fg="white",font="bold")
name_entry=tk.Entry(root,textvariable=name_var,state=DISABLED)

contact_label=tk.Label(root,text="Enter Contact",bg="blue",fg="white",font="bold")  
contact_entry=tk.Entry(root,textvariable=contact_var,validate="key",validatecommand=(vlddigit,'%S'))
check_btn=tk.Button(root,text="VERIFY",command=verify)

email_label=tk.Label(root,text="Enter Email",bg="blue",fg="white",font="bold")  
email_entry=tk.Entry(root,textvariable=email_var,state=DISABLED)

bullet="\u2022"
password_label=tk.Label(root,text="Enter Password",bg="blue",fg="white",font="bold")  
password_entry=tk.Entry(root,textvariable=password_var,state=DISABLED,show=bullet)

sub_btn=tk.Button(root,text="REGISTER",state=DISABLED,command=register,bg="white",fg="blue",font="bold")

name_label.grid(row=0,column=1)
name_entry.grid(row=0,column=3)

contact_label.grid(row=2,column=1)
contact_entry.grid(row=2,column=3)
check_btn.grid(row=2,column=5)

email_label.grid(row=4,column=1)
email_entry.grid(row=4,column=3)

password_label.grid(row=6,column=1)
password_entry.grid(row=6,column=3)
sub_btn.grid(row=8,column=3)


root.mainloop()
