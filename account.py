import json
import re
import random
import datetime
import smtplib

def otp():
    otp = ""
    for i in range(4):
        otp += str(random.randint(0, 9))
    return otp

def validemail(email):
    # Add your email validation logic here
    # For simplicity, assuming any non-empty string is a valid email
    return bool(email)

def sendmail(email): 
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("kmitbank22@gmail.com", "tjugnsdzocyvlnsh")
    from_addr = "kmitbank22@gmail.com"
    to_addr = email
    subj = "OTP"
    otp1 = otp()
    message_text = f"To continue the process please enter the following OTP\n\n{otp1}"
    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    msg = f"From: {from_addr}\nTo: {to_addr}\nSubject: {subj}\nDate: {date}\n\n{message_text}"
    s.sendmail("kmitbank22@gmail.com", email, msg)
    s.quit()
    print("Sent Email")
    otp2 = input("Enter OTP: ")
    if otp1 == otp2:
        return True
    else:
        print("Wrong OTP, please try again!")
        return False

def acc_form():
    username = input("Enter your Username: ")
    print("Please Enter the following details")
    first_name = input("Enter your First name: ")
    last_name = input("Enter your Last name: ")
    DOB = input("Enter your Date of Birth in the form (DD/MM/YYYY): ")
    gender = input("Please enter your gender (M/F) [default=M]: ") or "M"
    aadhar = input("Enter your Aadhar number: ")
    email = input("Enter your email ID: ")
    while True:
        if not validemail(email):
            print("Please enter a valid Email ID")
            email = input("Enter your email ID: ")
        else:
            print("Please enter 1 to confirm your email ID:")
            opt = input("")
            if opt == "1":
                break
            else:
                email = input("Enter your email ID: ")

    print("An OTP will be sent to your mail. Please enter the OTP to create a bank account")
    if sendmail(email):
        balance = int(input("Enter the min balance for first deposit (1000-4000): "))
        while True:
            if balance > 4000 or balance < 1000:
                print("Invalid balance amount! Please try again.")
                balance = int(input("Enter the min balance for first deposit (1000-4000): "))
            else:
                print("You have a minimum balance of:", balance)
                break

        try:
            with open("usersdetails.json", "r+") as js:
                ud = json.load(js)
                for k, i in ud.items():
                    if i["Username"] == username:
                        ud[k]["first_name"] = first_name
                        ud[k]["last_name"] = last_name
                        ud[k]["gender"] = gender
                        ud[k]["aadhar"] = aadhar
                        ud[k]["emailid"] = email
                        ud[k]["DOB"] = DOB
                        ud[k]["Balance"] = balance
                        acc = account_numb()
                        ud[k]["Account_number"] = acc
                        js.seek(0) 
                        json.dump(ud, js)
            print("Your account has been successfully created!!")
            print("Your username:", username)
            print("Your account number:", acc)
        except Exception as e:
            print("Error:", str(e))
            print("File doesn't exist")

if __name__ == "__main__":
    acc_form()
