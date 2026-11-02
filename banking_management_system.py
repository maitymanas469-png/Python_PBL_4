"""Banking Management System PBL: demonstrates functions and Python packages.

This is a small educational, command-line simulation. It is not real banking
software and must not be used to store real financial or personal information.
"""

import json
import math
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).with_name("bank_accounts.json")


def load_accounts():
    """Load account records from the local JSON file, if it exists."""
    if not DATA_FILE.exists():
        return {}

    with DATA_FILE.open("r", encoding="utf-8") as file:
        accounts = json.load(file)

    if not isinstance(accounts, dict):
        raise ValueError("The account data file has an invalid format.")
    return accounts


def save_accounts(accounts):
    """Save records safely by writing a temporary file and replacing the old one."""
    temporary_file = DATA_FILE.with_suffix(".tmp")
    with temporary_file.open("w", encoding="utf-8") as file:
        json.dump(accounts, file, indent=4)
    temporary_file.replace(DATA_FILE)


def generate_account_number(accounts):
    """Generate a simple unique account number for this demonstration."""
    next_number = 100001
    while str(next_number) in accounts:
        next_number += 1
    return str(next_number)


def add_transaction(account, transaction_type, amount):
    """Add a dated transaction entry to an account's transaction history."""
    account["transactions"].append(
        {
            "type": transaction_type,
            "amount": round(amount, 2),
            "balance": round(account["balance"], 2),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )


def create_account(accounts):
    """Create an account and return its new account number."""
    name = input("Enter account holder name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return None

    account_number = generate_account_number(accounts)
    accounts[account_number] = {
        "name": name,
        "balance": 0.0,
        "transactions": [],
    }
    add_transaction(accounts[account_number], "Account opened", 0.0)
    save_accounts(accounts)

    print("Account created successfully.")
    print("Your account number is:", account_number)
    return account_number


def find_account(accounts, account_number):
    """Return an account if the supplied account number exists."""
    account = accounts.get(account_number)
    if account is None:
        print("Account not found. Please check the account number.")
    return account


def deposit(accounts):
    """Deposit a positive amount into an existing account."""
    account_number = input("Enter account number: ").strip()
    account = find_account(accounts, account_number)
    if account is None:
        return

    try:
        amount = float(input("Enter amount to deposit: "))
    except ValueError:
        print("Please enter a valid numeric amount.")
        return

    if not math.isfinite(amount) or amount <= 0:
        print("Enter a finite amount greater than zero.")
        return

    account["balance"] = round(account["balance"] + amount, 2)
    add_transaction(account, "Deposit", amount)
    save_accounts(accounts)
    print(f"Deposit successful. Current balance: Rs. {account['balance']:.2f}")


def withdraw(accounts):
    """Withdraw money if the amount is positive and funds are sufficient."""
    account_number = input("Enter account number: ").strip()
    account = find_account(accounts, account_number)
    if account is None:
        return

    try:
        amount = float(input("Enter amount to withdraw: "))
    except ValueError:
        print("Please enter a valid numeric amount.")
        return

    if not math.isfinite(amount) or amount <= 0:
        print("Enter a finite amount greater than zero.")
    elif amount > account["balance"]:
        print("Insufficient balance. Transaction cancelled.")
    else:
        account["balance"] = round(account["balance"] - amount, 2)
        add_transaction(account, "Withdrawal", amount)
        save_accounts(accounts)
        print(f"Withdrawal successful. Current balance: Rs. {account['balance']:.2f}")


def check_balance(accounts):
    """Display the holder name and current account balance."""
    account_number = input("Enter account number: ").strip()
    account = find_account(accounts, account_number)
    if account is not None:
        print("Account holder:", account["name"])
        print(f"Available balance: Rs. {account['balance']:.2f}")


def show_transactions(accounts):
    """Display all recorded transactions for an account."""
    account_number = input("Enter account number: ").strip()
    account = find_account(accounts, account_number)
    if account is None:
        return

    print(f"\nTransaction history for {account['name']} ({account_number})")
    if not account["transactions"]:
        print("No transactions recorded.")
        return

    for item in account["transactions"]:
        print(
            f"{item['date']} | {item['type']} | "
            f"Rs. {item['amount']:.2f} | Balance: Rs. {item['balance']:.2f}"
        )


def show_menu():
    print("\n========== BANKING MANAGEMENT SYSTEM ==========")
    print("1. Create account")
    print("2. Deposit money")
    print("3. Withdraw money")
    print("4. Check balance")
    print("5. View transaction history")
    print("0. Exit")


def main():
    """Load data and run the banking menu."""
    try:
        accounts = load_accounts()
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print("Could not load account data:", error)
        print("Please check the bank_accounts.json file before running again.")
        return

    actions = {
        "1": create_account,
        "2": deposit,
        "3": withdraw,
        "4": check_balance,
        "5": show_transactions,
    }

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "0":
            print("Thank you for using the Banking Management System.")
            break
        elif choice in actions:
            try:
                actions[choice](accounts)
            except OSError as error:
                print("Could not save account data:", error)
        else:
            print("Invalid choice. Please select an option from the menu.")


if __name__ == "__main__":
    main()
