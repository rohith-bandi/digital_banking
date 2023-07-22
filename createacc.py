import json
import re
import random
from datetime import date
import smtplib
import datetime

def otp():
    otp=""
    for i in range(4):
        otp=otp+str(random.randint(0,9))
    return otp

def sendmail(email): 
    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("kmitbank22@gmail.com","tjugnsdzocyvlnsh")
    from_addr = "kmitbank22@gmail.com"
    to_addr = email
    subj = "OTP"
    otp1=otp()
    message_text = "To continue the process please enter the following otp\n\n"+otp1
    date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )
    msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % ( from_addr, to_addr, subj, date, message_text )
    s.sendmail("kmitbank22@gmail.com",email,msg)
    s.quit()
    print("Sent Email")
    otp2=input("Enter otp: ")
    if(otp1==otp2):
        return True
    else:
        print("Wrong OTP , please Try again!")
        return False

def validemail(x):
    pattern = r"^[\w.-]+@[\w.-]+.\w+$"
    mat=re.search(pattern,x)
    if mat:
        return True
    else:
        return False
    
def checkacc(username):
    try:
        with open ("usersdetails.json","r") as js:
            ud = json.load(js)
        
            for i in ud.values():
            
                if (i["Admin/User"]=="User" and i["Username"]==username and i["Account_number"]==None):
                    return False
                
            
            return True
    except:
        print("File doesn't exist")
                
def validdob(x):
    if  re.search("[0-9]{2}[/][0-9]{2}[/][0-9]{4}",x)==None:
        return False 
    y=[int(i) for i in x.split('/')]
    if y[1]>0 and y[1]<13 and y[2]>0 and y[2]<=2023:
        l=[31,28,31,30,31,30,31,31,30,31,30,31]
        if (y[2]%400==0) or (y[2]%100==0 and y[2]%4==0):
            l[1]=29
        if y[0]>0 and y[0]<=l[y[1]-1]:
            return True
        else:
            return False
    else:
        return False

def check_existence(acc):
    try:
        with open ("usersdetails.json","r") as js:
            ud = json.load(js)
            for i in ud.values():
                if ( i["Admin/User"]=="User" and i["Account_number"]==acc):
                    return False
            return True
    except:
        print("File doesn't exist")

def account_numb():
    acc="KMIT"
    while(1):
        for i in range(5):
            acc=acc+str(random.randint(0,9))
        if(check_existence(acc)):
            break
        else:
            acc="KMIT"
    return acc

def validage(x):
    today = date.today()
    y=[int(i) for i in x.split('/')]
    return today.year - y[2] - ((today.month, today.day) < (y[1], y[0]))
def acc_form(username):
    print("Please Enter the following details")
    for i in range(3):
        first_name=input("Enter your First name: ")
        if re.search(r"^[a-zA-Z]+$",first_name):
            break
        else:
            print("first_name should contain only aplhabets")
            if i==2:
                return 0
    for i in range(3):
        last_name=input("Enter your Last name: ")
        if re.search(r"^[a-zA-Z]+$",last_name):
            break
        else:
            print("last_name should contain only aplhabets")
            if i==2:
                return 0       
    DOB=input("Enter your Date of Birth in the form(DD/MM/YYYY): ")
    for i in range(3):
        if not validdob(DOB):
            print("Please enter valid Date of Birth")
            DOB=input("Enter your Date of Birth in the form(DD/MM/YYYY): ")
            if i==2:
                return 0
        else:
            if validage(DOB)<18:
                print("The user age is below 18 not applicable for bank account creation")
                return False
    for i in range(3):        
        gender=input("Please enter your gender(M/F): ")
        if gender=="M" or gender=="F":
            break
        else:
            print("Choose M(Male) or F(Female)")
            if i==2:
                return 0
    for i in range(3):
        aadhar=input("Enter your aadhar number: ")
        if len(aadhar)==12 and re.search("[\d]{12}",aadhar):
            break
        else:
            print("Aadhar should contain only 12 digits")
            if i==2:
                return 0
    email=input("Enter your email id: ")
    while(True):
        if not validemail(email):
            print("Please enter valid Email id")
            email=input("Enter your email id: ")
        else:
            
            print("Please enter 1 to confirm your email id:")
            opt=int(input())
            if opt==1:
                break
            else:
                email=input("Enter your email id: ")



    print("An otp will be sent to your mail. Please enter the otp to create a bank account")
    if(sendmail(email)):
        balance=int(input("Enter the min balance for first deposit:(1000-4000)"))
        while(True):
            if balance>4000 or balance<1000:
                print("Invalid Balance amount! please try again.")
                balance=int(input("Enter the min balance for first deposit:(1000-4000):"))
            else:
                print("You have a minimum balance of :",balance)
                break
            
        try:
            with open ("usersdetails.json","r+") as js:
                ud = json.load(js)
                for k,i in ud.items():
                    if (i["Username"]==username):
                        ud[k]["first_name"]=first_name
                        ud[k]["last_name"] = last_name
                        ud[k]["gender"]    = gender
                        ud[k]["aadhar"]   = str(aadhar)
                        ud[k]["emailid"]     = email

                        ud[k]["DOB"] = DOB
                        ud[k]["Balance"]=balance
                        acc=account_numb()
                        ud[k]["Account_number"]=acc
                        js.seek(0) 
                        json.dump(ud,js)
            print("Your account has been succesfully created!!")
            print("Your username: ",username)
            print("Your account number: ",acc)
        except:
            print("File doesn't exist")


def debit(username):
    if(not checkacc(username)):
        print("You dont have a bank account please create bank account.")
    else:
        
        from_accno=getacc(username)
        to_accno=input("Enter the account number of the other person: ")
        if(not check_existence(to_accno)):
            try:
                with open ("usersdetails.json","r+") as js:
                    ud = json.load(js)
                    amount=float(input('Enter the Amount to be Debited : '))
                    if amount>getbalance(username):
                            print("Insufficient Balance!")
                            return 0
                    else:
                        for i in ud.values():
                            if i["Username"]==username:
                                bal=getbalance(username)
                                e=i["emailid"]
                                break
                        for i in ud.values():
                            if i["Admin/User"]=="User":
                                if i["Account_number"]==to_accno:
                                     u=i["Username"]
                                     cbal=getbalance(u)
                                     y=i["emailid"]
                                     break
                        print("Please enter the otp to continue the process")            
                        x=sendmail(e)
                        if x==True:
                            mailfortransaction(e,amount,"debit",bal)
                            mailfortransaction(y,amount,"credit",cbal)
                            for i in ud.values():
                                if(i["Admin/User"]=="User" and i['Account_number']==to_accno):
                                    i['Balance']=amount+int(i['Balance'])
                                if(i["Admin/User"]=="User" and (from_accno)==str(i['Account_number'])):
                                    i['Balance']=int(i['Balance'])-amount

                            js.seek(0)
                            json.dump(ud,js)
                            with open ("transaction_details.json","r+") as js1:
                                ud1=json.load(js1)
                                id=len(ud1)+1
                                date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )
                                ud2={id:{"From_acc":from_accno,"To_acc":to_accno,"Amount":amount,"Date":date}}
                                ud1.update(ud2)
                                js1.seek(0)
                                json.dump(ud1,js1)
                        else:
                            return 0
            except: 
                print("File doesn't exist")
                return 0
                            
        else:
            print("Invalid account number")
        
def getacc(username):
    try:
        with open ("usersdetails.json","r") as js:
            ud = json.load(js)
        
            for i in ud.values():
            
                if (i["Admin/User"]=="User" and i["Username"]==username):
                    if(i["Account_number"]==None):
                        print("You dont have an account please create an account")

                        return 0
                    else:
                        return i["Account_number"]
            else:
                print("Invalid username")
                return 1
                    
    except:
        print("File doesn't exist")
        
def get(acc_no):
    try:
        with open ("usersdetails.json","r") as js:
            ud = json.load(js)
            for i in ud.values():
                if(i["Admin/User"]=="User" and i["Account_number"]==acc_no):
                    return i["Username"]
            return "Bank"
    except:
        print("File doesn't exist")
    
            
def getbalance(username):
    try:
        with open ("usersdetails.json","r") as js:
            ud = json.load(js)
            for i in ud.values():
                if (i["Admin/User"]=="User" and i["Username"]==username):
                    if(i["Account_number"]==None):
                        print("You dont have an account please create an account")
                        return None
                    else:
                        return i["Balance"],i["Account_number"]
    except:
        print("File doesn't exist")
        


def viewtrans(username):
    acc=getacc(username)
    if(acc!=0):
        flag=0
        with open ("transaction_details.json","r") as js1:
            ud1=json.load(js1)
            for i in ud1.values():
                if(i["From_acc"]==acc or i["To_acc"]==acc):
                    print("From: ",i["From_acc"]," - ",get(i["From_acc"]),"  To: ",i["To_acc"]," - ",get(i["To_acc"])," Amount: ",int(i["Amount"])," Date: ",i["Date"])
                    flag=1    
            if(flag==0):
                print("\nNo Transactions found\n")

def mailfortransaction(email,amount,x,y):
    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("kmitbank22@gmail.com","tjugnsdzocyvlnsh")
    from_addr = "kmitbank22@gmail.com"
    to_addr = email
    subj = "Amount_Transaction"
    message_text = "Your account is "+x+" with the amount of "+str(amount)+" and available balance rupees is "+str(y-amount)
    date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )
    msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % ( from_addr, to_addr, subj, date, message_text )
    s.sendmail("kmitbank22@gmail.com",email,msg)
    s.quit()
    print("Sent Email")

def feedback(username):
    
    while(True):
        rating=int(input("Enter your rating(0-5) :"))

        if rating<0 or rating>5:
            print("Invalid input,rating should be between 0 to 5.")

        elif rating<=3:
            print("We are sorry that you did not like our service.")
            msg=input("Please enter your feedback: ")
            msg="\n"+username+": rating :"+str(rating)+":"+msg
            with open("feedback.txt","a") as f:
                f.write(msg)
            print("We will verify your feedback and make the required changes to solve the issue!\nThank you!")
            break
        
        else:
            print("Thankyou for giving us positive rating!")
            return 0
    return 0


    
def display(username):
    print()
    print("1.Create an account")
    print("2.View previous transactions")
    print("3.Make a transaction")
    print("4.View Account Balance")
    print("5.Give feedback")
    print("6.Exit")
    print()
    opt=int(input("Enter your option:"))
    if opt==1:
        if(not checkacc(username)):
            acc_form(username)
        else:
            print("You already have an account")
        display(username)
    elif opt==3:
        debit(username)
        display(username)
        
    elif(opt==2):
        while(True):
            print()
            print("1.View all transaction details")
            print("2.View transactions from particular user")
            print("3.View transactions of a particular date")
            print("4.View cash-cash transactions")
            print("5.View account-account transactions")
            print("6.Exit")
            print()
            opt=int(input("Enter an option:"))
            if opt==1:
                viewtrans(username)
            elif opt==4:
                acc=getacc(username)
                if(acc!=0):
                    with open ("transaction_details.json","r") as js:
                        data = json.load(js)
                        for i in data.values():
            
                            if (i["From_acc"]=="Admin" and i["To_acc"]==getacc(username)) or (i["From_acc"]==getacc(username) and i["To_acc"]=="Admin"):
                                print("From: ",i["From_acc"]," - ",get(i["From_acc"]),"  To: ",i["To_acc"]," - ",get(i["To_acc"])," Amount: ",int(i["Amount"])," Date: ",i["Date"])
            elif opt==5:
                acc=getacc(username)
                if(acc!=0):
                    with open ("transaction_details.json","r") as js:
                        data = json.load(js)
                        for i in data.values():
                            if (i["From_acc"]!="Admin" and i["To_acc"]==getacc(username)) or (i["From_acc"]==getacc(username) and i["To_acc"]!="Admin"):
                                print("From: ",i["From_acc"]," - ",get(i["From_acc"]),"  To: ",i["To_acc"]," - ",get(i["To_acc"])," Amount: ",int(i["Amount"])," Date: ",i["Date"])
            elif(opt==2):
                acc=getacc(username)
                if(acc!=0): 
                    flag=0
                    user=input("Enter the username:")
                    with open ("transaction_details.json","r") as js:
                        data = json.load(js)
                        if getacc(user)!=1 and getacc(user)!=0:
                            for i in data.values():

                                if (i["From_acc"]==getacc(user) and i["To_acc"]==getacc(username)) or (i["From_acc"]==getacc(username) and i["To_acc"]==getacc(user)):
                                    print("From: ",i["From_acc"]," - ",get(i["From_acc"]),"  To: ",i["To_acc"]," - ",get(i["To_acc"])," Amount: ",int(i["Amount"])," Date: ",i["Date"])
            elif(opt==3):
                acc=getacc(username)
                if(acc!=0): 


                    date=input("Enter your Date in the form(DD/MM/YYYY): ")
                    k=validdob(date)
                    if(k==False):
                        print("Please enter valid date of birth")
                    else:
                                
                        with open ("transaction_details.json","r") as js:
                            data = json.load(js)
                            flag=0
                            for i in data.values():
                                chk=i["Date"].split()
                                if(i["From_acc"]==getacc(username) or i["To_acc"]==getacc(username)):
                                    if(chk[0]==date):
                                        print("From: ",i["From_acc"]," - ",get(i["From_acc"]),"  To: ",i["To_acc"]," - ",get(i["To_acc"])," Amount: ",int(i["Amount"])," Date: ",i["Date"])
                                        flag=1
                            if(flag==0):
                    
                                print("No transaction on date: ",date)
            elif(opt==6):
                break
            else:
                print("Invalid option")

        display(username)
    elif(opt==4):
        if(getbalance(username)!=None):
            balance,acc=getbalance(username)
            print("Your account number :",acc,"has a Bank balance of:",balance)
        display(username)
    elif(opt==5):
        feedback(username)
        display(username)
    elif(opt==6):
        return 0
    else:
        print("Invalid option")
        display(username)       
