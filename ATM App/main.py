import csv
from datetime import datetime as dt, timedelta
import os
import sqlite3
from PIL import Image,ImageTk  
import time
from tkinter.ttk import *
from tkinter import *
from tkinter import messagebox
from qr_scanner import Scanner
from face_cap import Capture
from mailer import Mailer
import threading

root = Tk()
root.title('HADS ATM')
root.geometry('1600x900')
bk = Label(root,relief='sunken',bd=15,bg = 'Deepskyblue')
bk.place(x=0,y=0,relheight = 1,relwidth = 1)
label = Label(root,text="Welcome to HADS ATM",font=("Times", 44,'bold'),bg = 'Deepskyblue')
label.place(x=450,y=300)



class Audios():
    def f(self):
        os.system("welcome.mp3") 
    def card_window(self):
        os.system(" card_no.mp3") 

class Atm():

    entered_card = ''
    entered_pin = 0
    pin = 0
    balance = 0
    card_state = 0
    pin_count = 0
    unblock_time = dt.now()

    def __init__(self,root):
        self.btn = Button(root,text="Continue",bg = 'lightgray',command=self.option_window,font=("Times", 24,'bold'),bd=6,relief = 'raised',)
        self.btn.place(x=710,y=400)
        root.after(1000,Audios().f)
    
    def option_window(self):
        self.top = Toplevel()
        self.top.geometry('1600x900')

        bk = Label(self.top,relief='sunken',bd=15,bg = 'Deepskyblue')
        bk.place(x=0,y=0,relheight = 1,relwidth = 1)
        
        label = Label(self.top,text="SELECT AN OPTION TO PROCEED",font=("Times", 44,'bold'),bg = 'Deepskyblue')
        label.place(x=300,y=200)

        btn1 = Button(self.top,text='ATM CARD',width=11,fg='black',command = self.card_window,height=2,font=("Times", 13,'bold'),relief = 'raised',bd = 3)
        btn1.place(x=100,y=400)
        
        btn2 = Button(self.top,text='VIRTUAL CARD',width=15,fg='black',command = self.vcard_window,height=2,font=("Times", 13,'bold'),relief = 'raised',bd = 3)
        btn2.place(x=1300,y=400)
    
    # TO CREATE A NUMPAD 
    def numpad(self,window,row=0,column=0):
        
        back = Label(window,background='gray',relief='sunken',bd=15)
        back.place(x=560,y=390,width=410,height=330)
        
        b1 = Button(window,text='1',width=5,bg='lightgray',fg='black',command = lambda:self.numpad_click(window,'1'),height=2,font=("Times", 14,'bold'),relief = 'raised',bd = 3)
        b1.place(x=590,y=420)

        
        b2 = Button(window,text='2',width=5,bg='lightgray',fg='black',command =lambda:self.numpad_click(window,'2'),height=2,font=("Times", 14,'bold'),relief = 'raised',bd = 3)
        b2.place(x=680,y=420)

        b3 = Button(window,text='3',width=5,bg='lightgray',fg='black',command =lambda:self.numpad_click(window,'3'),height=2,font=("Times", 14,'bold'),relief = 'raised',bd = 3)
        b3.place(x=770,y=420)

        b4 = Button(window,text='4',width=5,bg='lightgray',fg='black',command = lambda:self.numpad_click(window,'4'),height=2,font=("Times", 14,'bold'),relief = 'raised',bd = 3)
        b4.place(x=590,y=490)

        b5 = Button(window,text='5',width=5,bg='lightgray',fg='black',command = lambda:self.numpad_click(window,'5'),height=2,font=("Times", 14,'bold'),relief = 'raised',bd = 3)
        b5.place(x=680,y=490)

       
        b6 = Button(window,text='6',width=5,bg='lightgray',fg='black',command = lambda:self.numpad_click(window,'6'),height=2,font=("Times", 14,'bold'),relief = 'raised',bd = 3)
        b6.place(x=770,y=490)

        b7 = Button(window,text='7',width=5,bg='lightgray',fg='black',command = lambda:self.numpad_click(window,'7'),height=2,font=("Times", 14,'bold'),relief = 'raised',bd = 3)
        b7.place(x=590,y=560)

        b8 = Button(window,text='8',width=5,bg='lightgray',fg='black',command = lambda:self.numpad_click(window,'8'),height=2,font=("Times", 14,'bold'),relief = 'raised',bd = 3)
        b8.place(x=680,y=560)

        
        b9 = Button(window,text='9',width=5,bg='lightgray',fg='black',command = lambda:self.numpad_click(window,'9'),height=2,font=("Times", 14,'bold'),relief = 'raised',bd = 3)
        b9.place(x=770,y=560)

        bn = Button(window,width=5,height=2,bg='lightgray',fg='black',relief = 'raised',bd = 3,font=("Times", 14,'bold'))
        bn.place(x=590,y=630)

        b0 = Button(window,text='0',width=5,height=2,bg='lightgray',fg='black',command = lambda:self.numpad_click(window,'0'),font=("Times", 14,'bold'),relief = 'raised',bd = 3)
        b0.place(x=680,y=630)

        bn = Button(window,width=5,height=2,bg='lightgray',fg='black',relief = 'raised',bd = 3,font=("Times", 14,'bold'))
        bn.place(x=770,y=630)
        
        b = Button(window,text='CLEAR',width=5,bg='orange',fg='black',command = lambda:self.numpad_click(window,'clear'),height=2,font=("Times", 13,'bold'),relief = 'raised',bd = 3)
        b.place(x=860,y=490)

        b = Button(window,text='DELETE',width=6,bg='yellow',fg='black',height=2,font=("Times",12,'bold'),command = lambda:self.numpad_click(window,'delete'),relief = 'raised',bd = 3)
        b.place(x=860,y=560)
        
        b = Button(window,text='CANCEL',bg='red',width=6,fg='black',height=2,font=("Times",12,'bold'),command =lambda:self.on_cancel(window),relief = 'raised',bd = 3)
        b.place(x=860,y=420)



    # NUMPAD ACTIONS
    def numpad_click(self,window,key):
        previous = self.e.get()
        if key=='clear':
            self.e.delete(0,END)
        elif (key=='delete'):    
            self.e.delete(0,END)
            self.e.insert(0,previous[0:len(previous)-1])
        else:
            self.e.delete(0,END)
            self.e.insert(0,previous+key)

    def on_cancel(self,window):
        window.destroy()
        top=Toplevel()
        top.resizable(False,False)
        top.geometry('1600x900')
        top.configure(background="Deepskyblue")
        Label(top,relief='sunken',bd=15,bg = 'Deepskyblue').place(x=0,y=0,relheight = 1,relwidth = 1)
        Label(top,text="Thank you for using our ATM",font=("Times", 44,'bold'),bg = 'Deepskyblue').place(x=400,y=300)
        top.after(6000,top.destroy)

    def on_time_limit_succeeded(self):
        print("Times up")
        top=Toplevel()
        top.resizable(False,False)
        top.geometry('1600x900')
        top.configure(background="Deepskyblue")
        Label(top,relief='sunken',bd=15,bg = 'Deepskyblue').place(x=0,y=0,relheight = 1,relwidth = 1)
        Label(top,text="Time limit succceeded, try doing transaction again",font=("Times", 44,'bold'),bg = 'Deepskyblue').place(x=200,y=300)
        top.after(6000,top.destroy)

    def vcard_window(self):
        self.top.destroy()
        self.top=Toplevel()
        self.top.geometry("1600x900")
        self.top.configure(background="Deepskyblue")
        self.label = Label(self.top,text="Scan the QR Code",background="Deepskyblue",font=("Times", 44,'bold'))
        self.label.place(x=550,y=300)
        self.top.after(100,self.qr_scan)

    def qr_scan(self):
        text=Scanner.scan(Scanner)
        print(text)
        if text:
            self.top.destroy()
            self.search_win(text)
        else:
            self.label.configure(text="QR code not found")
            self.top.after(3000,self.top.destroy)

    # FUNTION TO CREATE A WINDOW TO ENTER CARD NO.
    def card_window(self):
        self.top.destroy()
        self.top = Toplevel()
        self.top.geometry('1600x900')
        
        bk = Label(self.top,relief='sunken',bd=15,bg = 'Deepskyblue')
        bk.place(x=0,y=0,relheight = 1,relwidth = 1)
        
        label = Label(self.top,text="Enter your card number",font=("Times", 25,'bold'),bg = 'Deepskyblue')
        label.place(x=570,y=100)

        self.e = Entry(self.top,width=20,font=("largefont", 20,'bold'),justify='center')
        self.e.place(x=560,y=200)
        
        self.numpad(self.top,row=3)
        next = Button(self.top,text="NEXT",command=self.search_win,bd=3,relief='raised',font=("Times", 13,'bold'),bg = 'limegreen',fg='black',width=5,height=2)
        next.place(x=860,y=630)

        self.destroyTimer(20,self.top)

        self.top.after(500,Audios().card_window) 

    #FUNCTION TO CREATE A WINDOW TO SEARCH USER
    def search_win(self,*card):
        top1 = Toplevel()
        top1.geometry('1600x900')
        top1.configure(background="Deepskyblue")

        label = Label(top1,text="SEARCHING...",font=("Times", 25,'bold'))
        label.configure(background="Deepskyblue")
        label.place(x=650,y=300)
        
        s = Style()
        s.theme_use("default")
        s.configure("TProgressbar", thickness=50)
        
        # Progress bar widget 
        progress = ttk.Progressbar(top1,style='TProgressbar', orient = HORIZONTAL, length = 500, mode = 'indeterminate') 
        progress.place(x=500,y=400)
        progress.start(10)
        
        entered_card = card[0] if card else self.e.get()
        self.top.destroy()
        found = self.search_user(entered_card)
        if found:
            if (self.card_state == 0 and self.unblock_time > dt.now()):
                top1.after(3000,self.card_blocked)
                top1.after(3000,top1.destroy)
                self.conn.commit()
            elif found:
                if (self.card_state == 0):
                    self.edit_balance('unblock')
                label.configure(text="Scan your face")
                # messagebox.showinfo('OPENING CAMERA','INSTRUCTIONS \n1.REMOVE MASK OR ANY OTHER ACCECERIES \n2.PLACE YOUR FACE PROPERLY BEFORE THE CAMERA\n3.WAIT FOR FEW SECONDS')
                print("found")
                top1.after(100,self.cam,top1,label)
                print('opening camera')
        else:
            print('not found')
            top1.after(1000,self.not_found)
            top1.after(3000,top1.destroy)
            self.conn.commit()
        top1.after(20000,top1.destroy)
            

    def cam(self,top1,label):
       Capture.capture(Capture)
       if Capture.clicked:
           top1.after(500,self.pin_window,top1)
           Capture.clicked=0
       else:
           label.configure(text="Face not detected")
           top1.after(3000,top1.destroy)
           print("Face detection failed")

    def not_found(self):
        top = Toplevel()
        top.geometry('1600x900')
        back = Label(top,relief='sunken',bd=15,bg = 'Deepskyblue')
        back.place(x=0,y=0,relheight = 1,relwidth = 1)
        label = Label(top,text = 'CARD NOT FOUND!',font=('Times',45,'bold'),bg = 'Deepskyblue')
        label.place(x=560,y=250)
        label2 = Label(top,text='PLEASE VERIFY YOUR CARD NUMBER',font=('Times',35,'bold'),bg = 'Deepskyblue')
        label2.place(x=400,y=450)
        top.after(6000,top.destroy)


    def card_blocked(self):
        top = Toplevel()
        top.geometry('1600x900')
        back = Label(top,relief='sunken',bd=15,bg = 'Deepskyblue')
        back.place(x=0,y=0,relheight = 1,relwidth = 1)
        label = Label(top,text = 'CARD BLOCKED!',font=('Times',45,'bold'),bg = 'Deepskyblue')
        label.place(x=560,y=250)
        label2 = Label(top,text='VISIT NEARBY BRANCH FOR INQUIRY',font=('Times',35,'bold'),bg = 'Deepskyblue')
        label2.place(x=400,y=450)
        top.after(6000,top.destroy)           

    def pin_window(self,top1):  #taking top1 as argument to destroy
        top1.destroy()
        self.top2 = Toplevel()
        self.top2.geometry('1600x900')

        bk = Label(self.top2,relief='sunken',bd=15,bg = 'Deepskyblue')
        bk.place(x=0,y=0,relheight = 1,relwidth = 1)

        label = Label(self.top2,text="Enter your pin",font=("Times", 25,'bold'),bg = 'Deepskyblue')
        label.place(x=630,y=130)
      
        self.e = Entry(self.top2,width=20,font=("largefont", 20,'bold'),show="*",justify='center')
        self.e.place(x=560,y=200)

        self.numpad(self.top2,row=3)
        next = Button(self.top2,text="NEXT",command=self.check_pin,bd=3,relief='raised',font=("Times", 13,'bold'),bg = 'limegreen',fg='black',width=5,height=2)
        next.place(x=860,y=630)

        self.destroyTimer(20,self.top2)

    def check_pin(self):
        entered_pin = self.e.get()
        self.top2.destroy()
        if (int(entered_pin)== self.pin):
            print("pin verified")
            self.menu()
        else:
            self.pin_count-=1
            self.edit_balance("pin_count")
            if self.pin_count==0:
                self.card_blocked()
                self.edit_balance('block')#edit card state to 0
            else:
                self.wrong_pin()
                print("wrong pin")

    def wrong_pin(self):
        self.top2 = Toplevel()
        self.top2.geometry('1600x900')
        
        back = Label(self.top2,relief='sunken',bd=15,bg = 'Deepskyblue')
        back.place(x=0,y=0,relheight = 1,relwidth = 1)
        label = Label(self.top2,text=" WRONG PIN! ",font=("Times", 45,'bold'),bg = 'Deepskyblue')
        label.place(x=300,y=250)

        label1 = Label(self.top2,text=" YOU HAVE ENTERED WRONG PIN NUMBER ",font=("Times", 25,'bold'),bg = 'Deepskyblue')
        label1.place(x=300,y=350)
        
        self.top2.after(5000,self.top2.destroy)

            
    def destroyTimer(self,time,window):
        print("GETS DESTROYED IN ",time)
        if time==0:
            window.destroy()
            self.on_time_limit_succeeded()
            return
        window.after(1000,self.destroyTimer,time-1,window)
        

    def edit_balance(self,*detail):  
        print("in edit")
        self.cur.execute("SELECT email,account_no FROM Personal JOIN Account ON Personal.id=Account.personal_id WHERE Account.id=?",(self.account_id,))
        email,account_no=self.cur.fetchone()
        try:
            if detail[0]=="pin_count":
                self.cur.execute('UPDATE Card SET pin_count=? WHERE account_id=?',(self.pin_count,self.account_id))
                print('pincount updated')
                threading.Thread(target=Mailer.mail,args=(Mailer,email,"wrong pin",account_no)).start()
            if detail[0] == 'unblock':
                self.cur.execute('UPDATE Card SET card_state=?,pin_count=? WHERE account_id=?',(1,3,self.account_id))
            if detail[0] == 'block':
                self.cur.execute('UPDATE Card SET card_state=?,unblock_time=? WHERE account_id=?',(0,dt.now()+ timedelta(hours=24),self.account_id))
                threading.Thread(target=Mailer.mail,args=(Mailer,email,"block",account_no)).start()
                print("blocked on ", dt.now())
            if detail[0]=="pin":
                print("in pin")
                self.cur.execute('UPDATE Card SET pin=? WHERE account_id=?',(self.pin,self.account_id))   
                threading.Thread(target=Mailer.mail,args=(Mailer,email,"pin",account_no)).start()            
            if detail[0] == "withdraw":
                self.balance = self.balance - self.withdraw_amount
                self.cur.execute('UPDATE Account SET balance=? WHERE id=?',(self.balance,self.account_id))
                threading.Thread(target=Mailer.mail,args=(Mailer,email,"withdraw",account_no,self.withdraw_amount)).start()
                self.add_trans("withdraw")
            if detail[0] =="deposit":
                self.balance = self.balance + self.deposit_amount
                self.cur.execute('UPDATE Account SET balance=? WHERE id=?',(self.balance,self.account_id))
                self.add_trans("deposit")
                threading.Thread(target=Mailer.mail,args=(Mailer,email,"deposit",account_no,self.deposit_amount)).start()
            if detail[0] == "check balance":
                threading.Thread(target=Mailer.mail,args=(Mailer,email,"check balance",account_no,self.balance)).start()
            if detail[0] == "mini statement":
                threading.Thread(target=Mailer.mail,args=(Mailer,email,"mini statement",account_no,detail[1])).start()
        except:
            print('No internet!')

        self.conn.commit()


    def search_user(self,entered_card):

        self.conn = sqlite3.connect("data.sqlite")
        self.cur = self.conn.cursor()

        self.cur.execute("SELECT account_id,balance,pin,card_state,pin_count,unblock_time,expiry FROM Account JOIN Card ON Account.id=Card.account_id WHERE card_no=?",(entered_card,))
        user = self.cur.fetchone()
        if user:
            account_id,balance,pin,card_state,pin_count,unblock_time,expiry = user
            self.account_id = account_id
            self.pin = pin
            self.balance = balance
            self.pin_count = pin_count
            self.card_state = card_state
            t_str = unblock_time
            self.unblock_time = dt(int(t_str[0:4]),int(t_str[5:7]),int(t_str[8:10]),int(t_str[11:13]),int(t_str[14:16]),int(t_str[17:19]))
            return 1
        return 0


    def add_trans(self,detail):
        if detail == "deposit":
            print("transaction added")
            trans="Credited"
            amount = self.deposit_amount
            self.cur.execute('''INSERT INTO "Trans" (trans,amount,balance,datetime,account_id) VALUES (?,?,?,?,?)''',(trans,amount,self.balance,str(dt.now()).split('.')[0],self.account_id))
        if detail == "withdraw":
            trans="Debited"
            amount = self.withdraw_amount
            self.cur.execute('INSERT INTO "Trans" (trans,amount,balance,datetime,account_id) VALUES (?,?,?,?,?)',(trans,amount,self.balance,str(dt.now()).split('.')[0],self.account_id))
        self.conn.commit()


    def menu(self):
        self.top4 = Toplevel()
        self.top4.geometry('1600x900')
       
        bk = Label(self.top4,relief='sunken',bd=15,bg = 'Deepskyblue')
        bk.place(x=0,y=0,relheight = 1,relwidth = 1)

        label = Label(self.top4,text="SELECT YOUR OPTION",font=("Times", 25,'bold'),bg = 'Deepskyblue')
        label.place(x=630,y=130)


        btn1 = Button(self.top4,text="Withdraw",command=self.withdraw_win,bd=3,relief='raised',font=("Times", 20,'bold'),fg='black',width=11,height=2)
        btn1.place(x=50,y=250)


        btn2 = Button(self.top4,text="Deposit",command=self.deposit_win,bd=3,relief='raised',font=("Times", 20,'bold'),fg='black',width=9,height=2)
        btn2.place(x=50,y=500)

        btn3 = Button(self.top4,text="Change Pin",command=self.change_pin1,bd=3,relief='raised',font=("Times", 20,'bold'),fg='black',width=12,height=2)
        btn3.place(x=1380,y=250)

        btn4 = Button(self.top4,text="Check Balance",command=self.check_balance,bd=3,relief='raised',font=("Times", 20,'bold'),fg='black',width=12,height=2)
        btn4.place(x=1380,y=500)

        btn5 = Button(self.top4,text="Mini Statement",command=self.mini_statement,bd=3,relief='raised',font=("Times", 20,'bold'),fg='black',width=15,height=2)
        btn5.place(x=670,y=750)

       
        self.destroyTimer(20,self.top4)            

    def withdraw_check(self):
        self.withdraw_amount = float(self.e.get())
        self.top8.destroy()
        if self.withdraw_amount < self.balance :
            self.edit_balance("withdraw")
            top = Toplevel()
            top.geometry('1600x900')
            back = Label(top,relief='sunken',bd=15,bg = 'Deepskyblue')
            back.place(x=0,y=0,relheight = 1,relwidth = 1)
            label = Label(top,text = 'TRANSACTION SUCCESSFULL!',font=('Times',45,'bold'),bg = 'Deepskyblue')
            label.place(x=430,y=350)
            top.after(6000,top.destroy)
        else:
            top = Toplevel()
            top.geometry('1600x900')
            back = Label(top,relief='sunken',bd=15,bg = 'Deepskyblue')
            back.place(x=0,y=0,relheight = 1,relwidth = 1)
            label = Label(top,text = 'INSUFFICIENT BALANCE!',font=('Times',45,'bold'),bg = 'Deepskyblue')
            label.place(x=430,y=350)
            top.after(6000,top.destroy)

    def withdraw_win(self):
        self.top4.destroy()
        self.top8 = Toplevel()
        self.top8.geometry('1600x900')
        
        bk = Label(self.top8,relief='sunken',bd=15,bg = 'Deepskyblue')
        bk.place(x=0,y=0,relheight = 1,relwidth = 1)

        label = Label(self.top8,text="Enter the amount to Withdraw in rupees",font=("Times", 25,'bold'),bg = 'Deepskyblue')
        label.place(x=500,y=130)

        self.e =Entry(self.top8,width=20,font=("largefont", 20,'bold'),justify='center')
        self.e.place(x=560,y=200)
        
        self.numpad(self.top8,row=3)
        next = Button(self.top8,text="NEXT",command=self.withdraw_check,bd=3,relief='raised',font=("Times", 13,'bold'),bg = 'limegreen',fg='black',width=5,height=2)
        next.place(x=860,y=630)

        
        self.destroyTimer(20,self.top8)

    def deposit_check(self):
        self.deposit_amount = float(self.e.get())
        self.top9.destroy()
        self.edit_balance("deposit")
        top = Toplevel()
        top.geometry('1600x900')
        back = Label(top,relief='sunken',bd=15,bg = 'Deepskyblue')
        back.place(x=0,y=0,relheight = 1,relwidth = 1)
        label = Label(top,text = 'TRANSACTION SUCCESSFULL!',font=('Times',45,'bold'),bg = 'Deepskyblue')
        label.place(x=430,y=350)
        top.after(6000,top.destroy)


    def deposit_win(self):
        self.top4.destroy()
        self.top9 = Toplevel()
        self.top9.geometry('1600x900')
       
        bk = Label(self.top9,relief='sunken',bd=15,bg = 'Deepskyblue')
        bk.place(x=0,y=0,relheight = 1,relwidth = 1)

        label = Label(self.top9,text="Enter the amount to deposit in rupees",font=("Times", 25,'bold'),bg = 'Deepskyblue')
        label.place(x=500,y=130)

        self.e =Entry(self.top9,width=20,font=("largefont", 20,'bold'),justify='center')
        self.e.place(x=560,y=200)

        self.numpad(self.top9,row=3)
        next = Button(self.top9,text="NEXT",command=self.deposit_check,bd=3,relief='raised',font=("Times", 13,'bold'),bg = 'limegreen',fg='black',width=5,height=2)
        next.place(x=860,y=630)

        self.destroyTimer(20,self.top9)

    def change_pin1(self):
        self.top4.destroy()
        self.top6 = Toplevel()
        self.top6.geometry('1600x900')
        bk = Label(self.top6,relief='sunken',bd=15,bg = 'Deepskyblue')
        bk.place(x=0,y=0,relheight = 1,relwidth = 1)

        label = Label(self.top6,text="Enter Your Current Pin",font=("Times", 25,'bold'),bg = 'Deepskyblue')
        label.place(x=570,y=130)

        self.e =Entry(self.top6,width=20,font=("largefont", 20,'bold'),justify='center',show="*")
        self.e.place(x=560,y=200)

        self.numpad(self.top6,row=3)
        next = Button(self.top6,text="NEXT",command=self.change_pin2,bd=3,relief='raised',font=("Times", 13,'bold'),bg = 'limegreen',fg='black',width=5,height=2)
        next.place(x=860,y=630)
        self.destroyTimer(20,self.top6)


    def change_pin2(self):
        if (int(self.e.get()) == self.pin):
            self.top6.destroy()
            self.top7 = Toplevel()
            self.top7.geometry('1600x900')
            bk = Label(self.top7,relief='sunken',bd=15,bg = 'Deepskyblue')
            bk.place(x=0,y=0,relheight = 1,relwidth = 1)

            label = Label(self.top7,text="Enter Your New Pin",font=("Times", 25,'bold'),bg = 'Deepskyblue')
            label.place(x=590,y=130)

            self.e =Entry(self.top7,width=20,font=("largefont", 20,'bold'),justify='center',show='*')
            self.e.place(x=560,y=200)

            self.numpad(self.top7,row=3)
            next = Button(self.top7,text="NEXT",command=self.change_pin3,bd=3,relief='raised',font=("Times", 13,'bold'),bg = 'limegreen',fg='black',width=5,height=2)
            next.place(x=860,y=630)
            self.destroyTimer(20,self.top7)

        else:
            self.top6.destroy()
            top = Toplevel()
            top.geometry('1600x900')
            back = Label(top,relief='sunken',bd=15,bg = 'Deepskyblue')
            back.place(x=0,y=0,relheight = 1,relwidth = 1)
            label = Label(top,text=" WRONG PIN! ",font=("Times", 45,'bold'),bg = 'Deepskyblue')
            label.place(x=300,y=250)

            label = Label(top,text=" YOU HAVE ENTERED WRONG PIN NUMBER ",font=("Times", 25,'bold'),bg = 'Deepskyblue')
            label.place(x=300,y=350)

            self.top.after(6000,self.top.destroy)

    def change_pin3(self):
        if(self.pin !=  int(self.e.get()) ):
            new_pin = int(self.e.get())
            self.top7.destroy()
            self.pin = new_pin
            self.edit_balance("pin")
            top = Toplevel()
            top.geometry('1600x900')
            back = Label(top,relief='sunken',bd=15,bg = 'Deepskyblue')
            back.place(x=0,y=0,relheight = 1,relwidth = 1)
            label = Label(top,text = 'PIN CHANGED SUCCESSFULLY!',font=('Times',45,'bold'),bg = 'Deepskyblue')
            label.place(x=400,y=350)
            top.after(6000,top.destroy)
        else:
            top = Toplevel()
            top.geometry('1600x900')
            back = Label(top,relief='sunken',bd=15,bg = 'Deepskyblue')
            back.place(x=0,y=0,relheight = 1,relwidth = 1)
            label = Label(top,text = 'ERROR',font=('Times',45,'bold'),bg = 'Deepskyblue')
            label.place(x=300,y=250)
            label1 = Label(top,text = 'YOU HAVE ENTERED NEW PIN SAME AS YOUR PREVIOUS PIN.',font=('Times',25,'bold'),bg = 'Deepskyblue')
            label1.place(x=300,y=380)
            label2 = Label(top,text = 'INSERT THE CARD AGAIN AND RETRY.',font=('Times',25,'bold'),bg = 'Deepskyblue')
            label2.place(x=300,y=450)
            top.after(6000,top.destroy)

    def check_balance(self):
        self.top4.destroy()
        top5 = Toplevel()
        top5.geometry('1600x900')
        bk = Label(top5,relief='sunken',bd=15,bg = 'Deepskyblue')
        bk.place(x=0,y=0,relheight = 1,relwidth = 1)

        label = Label(top5,text=" YOUR CURRENT BALANCE IS :",font=("Times", 25,'bold'),bg = 'Deepskyblue')
        label.place(x=550,y=230)

        label = Label(top5,text=self.balance,font=("Times", 25,'bold'),bg = 'Deepskyblue')
        label.place(x=780,y=330)
        self.edit_balance("check balance")
        
        top5.after(10000,top5.destroy)

    def mini_statement(self):
        details = list(self.cur.execute('SELECT trans,amount,balance,datetime FROM Trans WHERE account_id=? ORDER BY id DESC LIMIT ?',(self.account_id,5)))
        data=[]
        data.append(["Date","Time","Transaction","Amount","Balance"])
        for i in range(len(details),0,-1):
            trans,amount,balance,datetime = details[i-1]
            data.append([str(datetime).split(' ')[0],str(datetime).split(' ')[1],trans,str(amount),str(balance)])
        self.edit_balance("mini statement",data)
        self.top4.destroy()

        top = Toplevel()
        top.geometry('550x700')
        top.title('HADS BANK')

        label = Label(top,text= 'HADS BANK',font=('Times',25,'bold'))
        label.place(x=170,y=30)

        label1 = Label(top,text= 'Sector 3,Near XYZ,Pincode - 410206',font=('Times',20,'bold'))
        label1.place(x=80,y=80)

        label2 = Label(top,text= '_________________________',font=('Times',25,'bold'))
        label2.place(x=70,y=110)

        Type = Label(top,text = 'TYPE',font=('Times',15,'bold')) 
        Type.place(x=50,y=180)

        date = Label(top,text = 'DATE',font=('Times',15,'bold')) 
        date.place(x=150,y=180)

        time = Label(top,text = 'TIME',font=('Times',15,'bold')) 
        time.place(x=280,y=180)

        Amount = Label(top,text = 'AMOUNT',font=('Times',15,'bold')) 
        Amount.place(x=420,y=180)
        
        text_list = []
        for i in range(len(details),0,-1):
            trans,amount,balance,datetime = details[i-1]
            text = trans+'\t'+str(datetime).split(' ')[0]+'\t'+str(datetime).split(' ')[1]+'\t\t'+str(amount)
            text_list.append(text)
            
        entry1 = Label(top,text =text_list[0],font=('Times',15,'bold')) 
        entry1.place(x=50,y=230)

        entry2 = Label(top,text = text_list[1],font=('Times',15,'bold')) 
        entry2.place(x=50,y=280)

        entry3 = Label(top,text = text_list[2],font=('Times',15,'bold')) 
        entry3.place(x=50,y=330)

        entry4 = Label(top,text = text_list[3],font=('Times',15,'bold')) 
        entry4.place(x=50,y=380)

        entry5 = Label(top,text = text_list[4],font=('Times',15,'bold')) 
        entry5.place(x=50,y=430)

        label3 = Label(top,text= '_________________________',font=('Times',25,'bold'))
        label3.place(x=70,y=450)

        balance= Label(top,text = 'BALANCE :',font=('Times',15,'bold')) 
        balance.place(x=280,y=500)

        balance1= Label(top,text = str(self.balance),font=('Times',15,'bold')) 
        balance1.place(x=450,y=500)
        top.after(10000,top.destroy)



atm = Atm(root)

root.mainloop()

print('after call')
