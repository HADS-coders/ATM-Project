# Python code to illustrate Sending mail with attachments 
# from your Gmail account  
  
# libraries to be imported 
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
from csv import writer
import os
from datetime import datetime 

class Mailer():

        def mail(self,toaddr,*detail):

            print("writing the mail....")
            # print(detail)

            fromaddr = "atmproject321@gmail.com"
            #toaddr = "daniyal.dolare@gmail.com"
            
            # instance of MIMEMultipart 
            msg = MIMEMultipart() 
            
            # storing the senders email address   
            msg['From'] = fromaddr 
            
            # storing the receivers email address  
            msg['To'] = toaddr 
            
            # storing the subject  
            msg['Subject'] = "ATM Transaction Details"

            atm_address="\tHADS BANK ATM\nSector 3, Near XYZ, Pincode - 410206\n\n"
            
            # string to store the body of the mail
            body = atm_address+"Account No.:"+str(detail[1])+"\nDate: "+str(datetime.now()).split(' ')[0]+"\nTime: "+str(datetime.now()).split(' ')[1]
            if detail[0]=="wrong pin":
                body = body + "\nDear customer, someone has just accessed your account and entered wrong pin"
            elif detail[0]=="block":
                body = body + "\nDear customer, someone just entered wrong pin for 3 times, hence your card is blocked.\nContact bank for further details"
            elif detail[0]=="pin":
                body = body+"\nDear customer, someone has just accessed your account and changed the pin."
            elif detail[0]=="withdraw":
                body = body+"\nTransaction: Withdrawl \nAmount: "+str(detail[2])
            elif detail[0]=="deposit":
                body = body+"\nTransaction: Deposit \nAmount: "+str(detail[2])
            elif detail[0] == "check balance":
                body = body+"\nDear customer, someone has just accessed your account and requested for balance.\nCurrent balance: "+str(detail[2])
            elif detail[0] == "mini statement":
                body = body +"\nDear customer, someone has just accessed your account and requested for mini statement.\n"

            # attach the body with the msg instance 
            msg.attach(MIMEText(body, 'plain')) 
            
            # open the file to be sent  
            filename = "face.jpg"
            attachment = open(filename, "rb") 
            
            # instance of MIMEBase and named as p 
            p = MIMEBase('application', 'octet-stream') 
            
            # To change the payload into encoded form 
            p.set_payload((attachment).read()) 
            
            # encode into base64 
            encoders.encode_base64(p) 
            
            p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
            
            # attach the instance 'p' to instance 'msg' 
            msg.attach(p) 

            if detail[0] == "mini statement":
                with open("mini statement.csv",'w') as file:
                    csv_writer = writer(file)
                    for data in detail[2]:
                        csv_writer.writerow(data)
                    
                filename = "mini statement.csv"
                attachment = open(filename, "rb")
                p = MIMEBase('application', 'octet-stream') 
                p.set_payload((attachment).read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                msg.attach(p)
            
            # creates SMTP session 
            s = smtplib.SMTP('smtp.gmail.com', 587) 
            
            # start TLS for security 
            s.starttls() 
            
            # Authentication 
            s.login(fromaddr, "project@atm123") 
            
            # Converts the Multipart msg into a string 
            text = msg.as_string() 
            
            # sending the mail 
            s.sendmail(fromaddr, toaddr, text) 

            print("mail sent")
            
            # terminating the session 
            s.quit()

            if(os.path.exists("mini statement.csv")):
                os.remove("mini statement.csv")

