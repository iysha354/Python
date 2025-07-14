import csv
import hashlib
import random
from datetime import datetime

ACCOUNTS_FILE = 'banking.csv'
TRANSACTIONS_FILE = 'transactions.csv'


def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()


def generate_account_number():
    return str(random.randint(10000000, 99999999))


def save_account(data):
    with open(ACCOUNTS_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)


def save_transaction(account_number, type_, amount):
    with open(TRANSACTIONS_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([account_number, type_, amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])


def load_accounts():
    try:
        with open(ACCOUNTS_FILE, newline='') as file:
            return list(csv.reader(file))
    except FileNotFoundError:
        return []


def load_transactions():
    try:
        with open(TRANSACTIONS_FILE, newline='') as file:
            return list(csv.reader(file))
    except FileNotFoundError:
        return []


def register():
    username = input("Create username: ")
    pin = input("Create 4-digit PIN: ")
    secret_q = input("Enter your secret question: ")
    secret_ans = input("Enter answer: ")
    account_number = generate_account_number()

    save_account([
        account_number,
        username,
        hash_text(pin),
        secret_q,
        hash_text(secret_ans),
        "0.00",  # balance
        "customer"
    ])
    print(f" Account created! Your account number is: {account_number}")


def login():
    account_number = input("Enter your account number: ")
    pin = input("Enter your PIN: ")

    for acc in load_accounts():
        if acc[0] == account_number and acc[2] == hash_text(pin):
            print(f"Welcome {acc[1]}!")
            return acc
    print("Login failed.")
    return None


def customer_menu(account):
    while True:
        print("\n Customer Menu")
        print("1. Withdraw Cash")
        print("2. Deposit Cash")
        print("3. Add Transaction (Purchase/Refund)")
        print("4. Mini Statement")
        print("5. View Balance")
        print("6. Transfer Funds")
        print("7. Money Manager (Streamlit)")
        print("8. Logout")

        choice = input("Choose option: ")
        if choice == '1':
            withdraw_cash(account)
        elif choice == '2':
            deposit_cash(account)
        elif choice == '3':
            add_transaction(account)
        elif choice == '4':
            mini_statement(account)
        elif choice == '5':
            view_balance(account)
        elif choice == '6':
            transfer_funds(account)
        elif choice == '7':
            print(" Run: streamlit run money_manager.py")
        elif choice == '8':
            break


def admin_menu():
    while True:
        print("\n Admin Menu")
        print("1. View All Accounts")
        print("2. Total Cash in Bank")
        print("3. Close Account")
        print("4. Logout")

        choice = input("Choose option: ")
        if choice == '1':
            view_all_accounts()
        elif choice == '2':
            total_cash()
        elif choice == '3':
            close_account()
        elif choice == '4':
            break


def update_account_balance(account_number, new_balance):
    accounts = load_accounts()
    for acc in accounts:
        if acc[0] == account_number:
            acc[5] = f"{new_balance:.2f}"
    with open(ACCOUNTS_FILE, mode='w', newline='') as file:
        csv.writer(file).writerows(accounts)


def withdraw_cash(account):
    amount = float(input("Enter amount to withdraw (max £100): "))
    if amount > 100:
        print("Withdrawal limit is £100.")
        return
    balance = float(account[5])
    if amount > balance:
        print("Insufficient balance.")
        return
    new_balance = balance - amount
    update_account_balance(account[0], new_balance)
    save_transaction(account[0], "withdrawal", -amount)
    print(f" Withdrawn £{amount:.2f}. New Balance: £{new_balance:.2f}")


def deposit_cash(account):
    amount = float(input("Enter amount to deposit: "))
    balance = float(account[5])
    new_balance = balance + amount
    update_account_balance(account[0], new_balance)
    save_transaction(account[0], "deposit", amount)
    print(f" Deposited £{amount:.2f}. New Balance: £{new_balance:.2f}")


def add_transaction(account):
    type_ = input("Enter type (purchase/refund): ").lower()
    amount = float(input("Enter amount: "))
    if type_ == "purchase":
        amount = -abs(amount)
    elif type_ == "refund":
        amount = abs(amount)
    else:
        print("Invalid type.")
        return

    balance = float(account[5])
    new_balance = balance + amount
    update_account_balance(account[0], new_balance)
    save_transaction(account[0], type_, amount)
    print(f" Transaction recorded. New Balance: £{new_balance:.2f}")


def mini_statement(account):
    transactions = [t for t in load_transactions() if t[0] == account[0]]
    print("\n Last 5 Transactions:")
    for row in transactions[-5:]:
        print(f"{row[1]} | £{row[2]} | {row[3]}")


def view_balance(account):
    print(f" Current Balance: £{account[5]}")


def transfer_funds(account):
    target_acc = input("Enter recipient account number: ")
    amount = float(input("Enter amount to transfer: "))
    accounts = load_accounts()

    sender_balance = float(account[5])
    if sender_balance < amount:
        print(" Insufficient funds.")
        return

    found = False
    for acc in accounts:
        if acc[0] == target_acc and acc[6] == "customer":
            acc[5] = str(float(acc[5]) + amount)
            found = True

    if found:
        for acc in accounts:
            if acc[0] == account[0]:
                acc[5] = str(sender_balance - amount)
        with open(ACCOUNTS_FILE, mode='w', newline='') as file:
            csv.writer(file).writerows(accounts)
        save_transaction(account[0], f"transfer_to_{target_acc}", -amount)
        save_transaction(target_acc, f"transfer_from_{account[0]}", amount)
        print(f" £{amount:.2f} transferred to {target_acc}.")
    else:
        print("Account not found.")


def view_all_accounts():
    for acc in load_accounts():
        print(f"Acc: {acc[0]} | User: {acc[1]} | Balance: £{acc[5]}")


def total_cash():
    total = sum(float(acc[5]) for acc in load_accounts() if acc[6] == "customer")
    print(f"Total cash in bank: £{total:.2f}")


def close_account():
    acc_num = input("Enter account number to close: ")
    accounts = load_accounts()
    updated = [acc for acc in accounts if acc[0] != acc_num]
    with open(ACCOUNTS_FILE, mode='w', newline='') as file:
        csv.writer(file).writerows(updated)
    print("Account closed.")


def main():
    print("Welcome to Khan Bank")
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose option: ")
        if choice == '1':
            register()
        elif choice == '2':
            user = login()
            if user:
                if user[6] == "admin":
                    admin_menu()
                else:
                    customer_menu(user)
        elif choice == '3':
            break


if __name__ == "__main__":
    main()
