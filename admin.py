import json
import datetime
import click

def deposit(acc_no, amount):
    try:
        with open("usersdetails.json", "r+") as js:
            ud = json.load(js)
            for i in ud.values():
                if i["Admin/User"] == "User" and i["Account_number"] == acc_no:
                    i["Balance"] += amount
                    js.seek(0)
                    json.dump(ud, js)
                    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                    add_transaction(acc_no, "Admin", amount, date)
                    print("Amount has been deposited")
                    break
    except Exception as e:
        print(f"Error: {str(e)}")

def withdrawal(acc_no, amount):
    try:
        with open("usersdetails.json", "r+") as js:
            ud = json.load(js)
            for i in ud.values():
                if i["Admin/User"] == "User" and i["Account_number"] == acc_no:
                    if amount > i["Balance"]:
                        print("Not enough Balance")
                    else:
                        i["Balance"] -= amount
                        js.seek(0)
                        json.dump(ud, js)
                        date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                        add_transaction("Admin", acc_no, amount, date)
                        print("Amount has been withdrawn")
                    break
    except Exception as e:
        print(f"Error: {str(e)}")

def add_transaction(from_acc, to_acc, amount, date):
    try:
        with open("transaction_details.json", "r+") as js1:
            ud1 = json.load(js1)
            id = len(ud1) + 1
            ud2 = {id: {"From_acc": from_acc, "To_acc": to_acc, "Amount": amount, "Date": date}}
            ud1.update(ud2)
            js1.seek(0)
            json.dump(ud1, js1)
    except Exception as e:
        print(f"Error: {str(e)}")

def get(acc_no):
    try:
        with open("usersdetails.json", "r") as js:
            ud = json.load(js)
            for i in ud.values():
                if i["Admin/User"] == "User" and i["Account_number"] == acc_no:
                    return i["Username"]
            return "Bank"
    except Exception as e:
        print(f"Error: {str(e)}")

def getacc(username):
    try:
        with open("usersdetails.json", "r") as js:
            ud = json.load(js)
            for i in ud.values():
                if i["Admin/User"] == "User" and i["Username"] == username:
                    if i["Account_number"] is None:
                        print("You don't have an account, please create an account")
                        return 0
                    else:
                        return i["Account_number"]
    except Exception as e:
        print(f"Error: {str(e)}")

def viewtrans():
    try:
        with open("transaction_details.json", "r") as js1:
            ud1 = json.load(js1)
            if not ud1:
                print("No transactions yet")
            else:
                for i in ud1.values():
                    print("From: ", i["From_acc"], " - ", get(i["From_acc"]),
                          "  To: ", i["To_acc"], " - ", get(i["To_acc"]), " Amount: ", int(i["Amount"]), " Date: ", i["Date"])
    except Exception as e:
        print(f"Error: {str(e)}")

def bankbalance():
    try:
        with open("usersdetails.json", "r") as f:
            ud = json.load(f)
            total_balance = sum(i["Balance"] for i in ud.values() if i["Admin/User"] == "User" and i["Account_number"] is not None)
            return total_balance
    except Exception as e:
        print(f"Error: {str(e)}")

@click.command()
def main():
    while True:
        print("\nEnter an option")
        print("1. Deposit")
        print("2. Withdrawal")
        print("3. View transactions")
        print("4. View bank balance")
        print("5. View the feedback of users")
        print("6. Exit")
        opt = click.prompt("Enter an option", type=int)

        if opt == 1:
            username = click.prompt("Enter the account name")
            amount = click.prompt("Enter amount to be deposited", type=int)
            k = getacc(username)
            if k != 0:
                deposit(k, amount)

        elif opt == 2:
            username = click.prompt("Enter the account name")
            amount = click.prompt("Enter amount to be withdrawn", type=int)
            k = getacc(username)
            if k != 0:
                withdrawal(k, amount)

        elif opt == 3:
            viewtrans()

        elif opt == 4:
            bal = bankbalance()
            print(f"\nThe total bank balance available is: {bal} rupees")

        elif opt == 5:
            try:
                with open("feedback.txt", "r") as f:
                    print(f.read())
            except Exception as e:
                print(f"Error: {str(e)}")

        elif opt == 6:
            break

        else:
            print('Invalid option')

if __name__ == "__main__":
    main()
