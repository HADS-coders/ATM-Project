from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk   
import sqlite3
from datetime import datetime as dt

main = Tk()
main.title("HADS BANK")
main.geometry("620x510")

l0 = Label(main, text="REGISTRATION FORM",font=("Times", 15),fg='black')
l0.place(x=200,y=15)    

l1 = Label(main, text="USER NAME",font=("Times", 15),fg='black')
l1.place(x=80,y=70)
e1 = Entry(main, bd = 8, font = 'LargeFont')
e1.place(x=320,y=70)
e1.insert(0,'SURNAME NAME')
def callback(event):
    e1.delete(0, END)
e1.bind('<FocusIn>',callback)
def callback1(event):
    if (e1.get()==''):
        e1.insert(0,'SURNAME NAME')
e1.bind('<FocusOut>',callback1)


l2 = Label(main, text="DATE OF BIRTH",font=("Times", 15) ,fg='black')
l2.place(x=80,y=140)
e2 = Entry(main, bd = 8, font = 'LargeFont')
e2.place(x=320,y=140)
e2.insert(0,'DD/MM/YYYY')
def callback(event):
    e2.delete(0, END)
    e2.insert(3,'   /')
    e2.insert(5,'  /  ')
e2.bind('<FocusIn>',callback)
def callback2(event):
    if (e2.get()==''):
        e2.insert(0,'DD/MM/YYYY')
e2.bind('<FocusOut>',callback2)

l3 = Label(main, text="E-MAIL",font=("Times", 15),fg='black')
l3.place(x=80,y=210)
e3 = Entry(main, bd = 8, font = 'LargeFont')
e3.place(x=320,y=210)
e3.insert(0,'ENTER G-MAIL ID')
def callback(event):
    e3.delete(0, END)
e3.bind('<FocusIn>',callback)
def callback3(event):
    if (e3.get()==''):
        e3.insert(0,'ENTER 10 DIGIT ACC. NO.')
e3.bind('<FocusOut>',callback3)


l4 = Label(main, text="MOBILE NO.",font=("Times", 15),fg='black')
l4.place(x=80,y=280)
e4 = Entry(main, bd = 8, font = 'LargeFont')
e4.place(x=320,y=280)
e4.insert(0,'ENTER 10 DIGIT MOBILE NO.')
def callback(event):
    e4.delete(0, END)
e4.bind('<FocusIn>',callback)
def callback4(event):
    if (e4.get()==''):
        e4.insert(0,'ENTER 10 DIGIT MOBILE NO.')
e4.bind('<FocusOut>',callback4)

l5 = Label(main, text="PIN CODE",font=("Times", 15),fg='black')
l5.place(x=80,y=350)
e5 = Entry(main, bd = 8 , font = 'LargeFont')
e5.place(x=320,y=350)
e5.insert(0,'ENTER 4 DIGIT PINCODE')
def callback(event):
    e5.delete(0, END)
e5.bind('<FocusIn>',callback)
def callback5(event):
    if (e5.get()==''):
        e5.insert(0,'ENTER 4 DIGIT PINCODE')
e5.bind('<FocusOut>',callback5)

def callback6(): 
    p = set(e3.get())
    q = set(e4.get())
    r = set(e5.get())
    if (p!=''):
        for i in q:
            if i.isdigit():
                b=0
            else:
                messagebox.showerror('WARNING','You have entered alphabet instead of a number inside\nCard no. that is : '+i+" \nPlease Re-enter" ) 
                e4.delete(0, END)
                b=1
        for i in r:
            if i.isdigit():
                c=0
            else:
                messagebox.showerror('WARNING','You have entered alphabet instead of a number inside\nPincode that is : '+i+" \nPlease Re-enter" )
                e5.delete(0, END)
                c=1

checkvar = IntVar()
c = Checkbutton(main,text = '*I Hereby confirm that all above info is correct',font=("Times", 15,'italic'),variable = checkvar,bd=0,width = 39,command = callback6)
c.place(x=90,y=410)


 

def save(): 
    if (checkvar.get()!=0):
        conn = sqlite3.connect('data.sqlite')
        cur = conn.cursor()
        p = e3.get()
        q = e4.get()
        r = e5.get()
        if(p!=0):
            name=e1.get()
            dob=e2.get()
            email=e3.get()
            mobile=int(e4.get())
            pin=int(e5.get())
            first_depo=1000

            cur.execute("INSERT INTO Personal (name,email,mobile,dob) VALUES (?,?,?,?)",(name,email,mobile,dob))
            cur.execute("SELECT id FROM Personal WHERE (name,email,mobile,dob) = (?,?,?,?)",(name,email,mobile,dob))
            personal_id = cur.fetchone()[0]

            cur.execute("SELECT account_no FROM Account WHERE personal_id=?",(personal_id-1,))	#selecting previous id's account_no
            account_no=cur.fetchone()[0]

            cur.execute("INSERT INTO Account (account_no,balance,personal_id) VALUES (?,?,?) ",(int(account_no)+1,first_depo,personal_id))
            cur.execute("SELECT id FROM Account WHERE personal_id = ? ",(personal_id,))
            account_id = cur.fetchone()[0]

            cur.execute("SELECT card_no FROM Card WHERE personal_id=?",(personal_id-1,))	#selecting previous id's card_no
            card_no=cur.fetchone()[0]

            cur.execute("""INSERT INTO Card (card_no,pin,card_state,pin_count, unblock_time, account_id, personal_id, expiry ,csv) 
                        VALUES (?,?,?,?,?,?,?,?,?)  """,(int(card_no)+1,pin,1,3,dt.now(),account_id,personal_id,'1/25',100))

            cur.execute('''INSERT INTO Trans (trans,amount,datetime,account_id) VALUES (?,?,?,?)''',('Debited',first_depo,str(dt.now()).split('.')[0],account_id))
            p = "REGISTERED NUMBER OF ENTRIES ARE : "+ str(personal_id)
            messagebox.showinfo('ALL SET',"Congratulations for your new account\nNow you can use our all services")
            messagebox.showinfo('SUCCESSFUL',p)
            conn.commit()
        else:
            messagebox.showerror('SOME ERROR HAS BEEN OCCURED ')
    else:
        c.flash()


b = Button(main,text='SUBMIT',width=6,fg='black',command = save,font=("Times", 13),relief = 'raised')
b.place(x=100,y=460)

def clear(): # a function to clear entry fields
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    e5.delete(0, END)

b = Button(main,text='CLEAR',width=5,fg='black',command = clear,font=("Times", 13))
b.place(x=250,y=460)

def exit():
    sys.exit()

b = Button(main,text='EXIT',width=5,fg='black',command = exit,font=("Times", 13))
b.place(x=400,y=460)
main.configure(background='ghost white')
main.mainloop()
