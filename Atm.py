import datetime

class Users:

    def __init__(self, user_id, pin):
        self.user_id = user_id
        self.pin = pin
        self.balance = 0
        self.transaction_history = []

    def check_balance(self):
        return f"Balance: {self.balance}"

    def authenticate_account(self, user_id, pin):
        return self.user_id == user_id and self.pin == pin

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            transaction = Deposit(amount)
            self.transaction_history.append(transaction)

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            transaction = Withdrawal(amount)
            self.transaction_history.append(transaction)
        else:
            print("Insufficient Balance")

    def transfer(self, recipient_id, amount, atm):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            recipient = atm.users.get(recipient_id)
            if recipient:
                recipient.balance += amount
                transaction = Transfer(recipient_id, amount)
                self.transaction_history.append(transaction)
                return f"Transferred {amount} to {recipient_id} successfully"
            else:
                return "Recipient ID not found."
        else:
            return "Invalid amount or insufficient funds."

    def get_transaction_history(self):
        return self.transaction_history

class Transaction:

    def __init__(self, amount):
        self.amount = amount
        self.date = datetime.datetime.now()

    def __str__(self):
        return f"{self.amount}-{self.date}"

class Deposit(Transaction):

    def __str__(self):
        return f"Deposit-{super().__str__()}"

class Withdrawal(Transaction):

    def __str__(self):
        return f"Withdrawal-{super().__str__()}"

class Transfer(Transaction):

    def __init__(self, recipient_id, amount):
        self.recipient_id = recipient_id
        super().__init__(amount)

    def __str__(self):
        return f"Transfer to {self.recipient_id} - {super().__str__()}"

class ATM:

    def __init__(self):
        self.users = {}

    def create_account(self, user_id, pin):
        if user_id not in self.users:
            self.users[user_id] = Users(user_id, pin)
            return "Account Created Successfully"
        return "User already exists."

    def authenticate_account(self, user_id, pin):
        if user_id in self.users:
            user = self.users[user_id]
            if user.authenticate_account(user_id, pin):
                return user
        return None

def Main():
    atm = ATM()

    while True:
        print("\n1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = int(input("Please Select an Option: "))
        if choice == 1:
            user_id = input("Enter the user id: ")
            pin = input("Enter the pin: ")
            res = atm.create_account(user_id, pin)
            print(res)
        elif choice == 2:
            user_id = input("Enter the user id: ")
            pin = input("Enter the pin: ")
            user = atm.authenticate_account(user_id, pin)
            if user:
                print(f"Welcome {user.user_id}!!")
                while True:
                    print("\n1. Check Balance")
                    print("2. Deposit")
                    print("3. Withdrawal")
                    print("4. Transfer")
                    print("5. Transaction History")
                    print("6. Exit")
                    option = int(input("Enter the option: "))
                    if option == 1:
                        res = user.check_balance()
                        print(res)
                    elif option == 2:
                        amount = float(input("Enter the amount to deposit: "))
                        user.deposit(amount)
                        print(f"Deposited {amount}rs. Successfully")
                    elif option == 3:
                        amount = float(input("Enter the amount to withdraw: "))
                        user.withdraw(amount)
                        print(f"Withdrew {amount}rs.")
                    elif option == 4:
                        recipient_id = input("Enter the recipient user id: ")
                        amount = float(input("Enter the amount to transfer: "))
                        result = user.transfer(recipient_id, amount, atm)
                        print(result)
                    elif option == 5:
                        history = user.get_transaction_history()
                        for i in history:
                            print(i)
                    elif option == 6:
                        print("Logout Successfully!!")
                        break
                    else:
                        print("Wrong option...")
            else:
                print("Account not found")
        elif choice == 3:
            print("Thanks for using the ATM. Have a Good day...")
            break
        else:
            print("Wrong Choice...")

Main()
