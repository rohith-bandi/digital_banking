import re
import json
import account
import admin


def validpassword(p):
    if len(p)>=8 and len(p)<=15 and re.search("[A-Z]",p) and re.search("[a-z]",p) and re.search("[0-9]",p) and re.search("[@#*$]",p):
        if not re.search("\s",p):
            return True
        else:
            return False
    else:
        return False

    
def register():
    try:
        with open("usersdetails.json","r+") as f:
            jdic=json.load(f)
            id=len(jdic)+1
            while 1:
                username=input("Enter your Username:")
                for i in jdic:
                    if jdic[i]["Username"]==username :
                        print("Username already exist")
                        break
                else:
                    break    
            instructor()
            while 1:
                password=input("Enter your Password:")
                if validpassword(password)==False:
                    print("Invalid Password")
                else:
                    break
            while 1:    
                cpassword=input("Confirm password:")
                if password==cpassword:
                    while 1:
                        name=input("Enter your name:")
                        if re.search(r"^[a-zA-Z]+$",name):
                            break
                        else:
                            print("Name should contain only alphabets")
                    dic={id:{"Username":username,"Password":password,"Name":name,"Account_number":None,"Admin/User":"User"}}
                    jdic.update(dic)
                    f.seek(0)
                    json.dump(jdic,f) 
                    print("Registered successfully")
                    break    
                else:
                    print("Password not matched")
    except:
        print("File doesn't exist")

                
def login():
    flag=0
    flag1=0
    try:
        with open("usersdetails.json","r") as f:
            jdic=json.load(f)
            for j in range(3):
                username=input("Enter your Username:")
                for i in jdic:
                    if jdic[i]["Username"]==username:
                        flag=1
                        break
                else:
                    print("Username not exist")
                if(flag==1):
                    break
                if i==2:
                    return False
            if flag==1:
                for j in range(3):
                    Password=input("Enter your Password:")
                    for i in jdic:
                        if jdic[i]["Password"]==Password and jdic[i]["Username"]==username:
                            flag1=1
                            break
                    else:
                        print("Password is incorrect")
                    if(flag1==1):
                        break
                    if i==2:
                        return False
                if flag==1 and flag1==1:
                    print("Logined Successfulluy")
                    return username
    except:
         print("File doen't exist")

         
def admin1(username):
    try:
        with open ("usersdetails.json","r") as js:
            ud = json.load(js)
            for i in ud.values():
                if (i["Admin/User"]=="User" and i["Username"]==username):
                        return "user"
                if(i["Admin/User"]=="Admin" and i["Username"]==username):
                        return "admin"
    except:
        print("File doesn't exist")
                
def  instructor():
    print("\nPassword should contain at least 8 characters and at most 15 characters")
    print("Password should contain at least 1 uppercase and 1 special character")
    print("Password should contain lowercase and digits\n")

    
print("************************************")
print("       WELCOME TO THE RSS BANK      ")
print("************************************\n")
    
while 1:
    print("1.REGISTER OR 2.LOGIN")
    x=input("Enter your option:")
    if x=="1":
        register()
        print("\n\n\n")
        continue      
    elif x=="2":

        k=login()

        if(k!=False):
            if(admin1(k)=="user"):
                account.display(k)
            if(admin1(k)=="admin"):
                print("Welcome to the admin page!")
                admin.display()
            print("\n\n\n")    
        else:
            print("\n\n\n")
            continue
        break
    else:
        print("Enter correct option")    