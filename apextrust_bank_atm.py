"""
APEXTRUST BANK ATM System
=========================
Banking Beyond Limits.

A beginner-friendly simulation of a Nigerian bank ATM.

Features:
    - Login with username and 4-digit PIN (3 attempts, then the account locks)
    - Balance enquiry, deposit, withdrawal (daily limit), transfer
    - Airtime purchase and bill payment
    - Mini statement, full transaction history, printable receipt
    - Account information and PIN change
    - SMS alert simulation after every successful transaction

Demo login details:
    Username : Abr01   (not case-sensitive)
    PIN      : 1234

Run with:  python apextrust_bank_atm.py
"""

import math
from builtins import print
from datetime import datetime

# ---------------------------------------------------------------------------
# 1. CONSTANTS (values that never change while the program runs)
# ---------------------------------------------------------------------------
BANK_NAME = "APEXTRUST BANK"
BANK_SLOGAN = "Banking Beyond Limits."
CURRENCY = "₦"
MAX_LOGIN_ATTEMPTS = 3
DAILY_WITHDRAWAL_LIMIT = 500_000
MIN_AIRTIME_AMOUNT = 50
LINE_WIDTH = 60

NETWORKS = ["MTN", "Airtel", "Glo", "9mobile"]
BILL_TYPES = ["Electricity", "DSTV", "GOTV", "Water", "Internet"]

# ---------------------------------------------------------------------------
# 2. DATA STORAGE (kept in memory while the program runs)
# ---------------------------------------------------------------------------
# One registered user. In a real system this would live in a database.
account = {
    "username": "Abr01",
    "pin": "1234",
    "account_name": "Abdurrahman Kuye",
    "account_number": "0123456789",
    "account_type": "Savings",
    "balance": 250_000_000.00,
}

# Every transaction is saved here as a dictionary.
transactions = []


# ---------------------------------------------------------------------------
# 3. SMALL HELPER FUNCTIONS (reused all over the program)
# ---------------------------------------------------------------------------
def money(amount):
    """Format a number as Naira, e.g. 1500 -> ₦1,500.00"""
    return f"{CURRENCY}{amount:,.2f}"


def current_date():
    """Return today's date as text, e.g. 14-Nov-2026."""
    return datetime.now().strftime("%d-%b-%Y")


def current_time():
    """Return the current time as text, e.g. 11:02:45 AM."""
    return datetime.now().strftime("%I:%M:%S %p")


def print_title(title):
    """Print a boxed section title so every screen looks consistent."""
    print("\n" + "=" * LINE_WIDTH)
    print(title.center(LINE_WIDTH))
    print("=" * LINE_WIDTH)


def get_amount(prompt):
    """
    Keep asking until the user types a valid positive amount.
    Returns the amount as a float, or None if the user types 'c' to cancel.
    """
    while True:
        text = input(prompt).strip().replace(",", "")
        if text.lower() == "c":
            print("Operation cancelled.")
            return None
        try:
            amount = float(text)
        except ValueError:
            print("Invalid amount. Please enter numbers only (or 'c' to cancel).")
            continue
        if not math.isfinite(amount):
            print("Invalid amount. Please enter a real number.")
        elif amount <= 0:
            print("Amount must be greater than zero.")
        else:
            return round(amount, 2)


def get_text(prompt):
    """Keep asking until the user types something that is not empty."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("This field cannot be empty.")


def get_digits(prompt, length, label):
    """Keep asking until the user types exactly `length` digits."""
    while True:
        text = input(prompt).strip()
        if text.isdigit() and len(text) == length:
            return text
        print(f"Invalid {label}. It must be exactly {length} digits.")


def choose_from_list(options, title):
    """Show a numbered list and return the option the user picks."""
    print(f"\n{title}")
    for number, option in enumerate(options, start=1):
        print(f"  {number}. {option}")
    while True:
        choice = input(f"Select (1-{len(options)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print("Invalid choice. Please pick a number from the list.")


def has_enough_balance(amount):
    """Check that the balance can cover `amount`; print a message if not."""
    if amount > account["balance"]:
        print(f"\nInsufficient funds. Your balance is {money(account['balance'])}.")
        return False
    return True


# ---------------------------------------------------------------------------
# 4. TRANSACTION RECORDING AND SMS ALERT
# ---------------------------------------------------------------------------
def send_sms_alert(direction, amount):
    """Simulate the SMS a customer receives after a transaction."""
    print("\n" + "-" * LINE_WIDTH)
    print("SMS ALERT".center(LINE_WIDTH))
    print("-" * LINE_WIDTH)
    print(f"{direction} Alert")
    print(f"Amount  : {money(amount)}")
    print(f"Balance : {money(account['balance'])}")
    print(f"Date    : {current_date()}")
    print(f"Time    : {current_time()}")
    print("-" * LINE_WIDTH)


def record_transaction(tx_type, amount, direction):
    """
    Update the balance, save the transaction in the history list and
    send an SMS alert. `direction` is either "Credit" or "Debit".
    This one function is used by every feature that moves money.
    """
    # Update the balance first
    if direction == "Credit":
        account["balance"] += amount
    else:
        account["balance"] -= amount

    # Save the transaction
    transactions.append({
        "date": current_date(),
        "time": current_time(),
        "type": tx_type,
        "amount": amount,
        "direction": direction,
        "balance": account["balance"],
        "status": "Successful",
    })

    send_sms_alert(direction, amount)


# ---------------------------------------------------------------------------
# 5. LOGIN SYSTEM
# ---------------------------------------------------------------------------
def welcome_screen():
    """Show the welcome banner."""
    print("\n" + "=" * LINE_WIDTH)
    print(f"WELCOME TO {BANK_NAME.upper()}".center(LINE_WIDTH))
    print(BANK_SLOGAN.center(LINE_WIDTH))
    print("=" * LINE_WIDTH)


def login():
    """
    Ask for username and PIN. The user gets three attempts.
    Returns True if login succeeds, False if the account gets locked.
    """
    for attempt in range(1, MAX_LOGIN_ATTEMPTS + 1):
        print(f"\nLogin attempt {attempt} of {MAX_LOGIN_ATTEMPTS}")

        username = get_text("Enter username: ")
        pin = input("Enter 4-digit PIN: ").strip()

        # The username is not case-sensitive, so we lowercase BOTH sides
        # before comparing. The PIN must match exactly.
        if username.lower() == account["username"].lower() and pin == account["pin"]:
            print(f"\nLogin successful. Welcome, {account['account_name']}!")
            return True

        remaining = MAX_LOGIN_ATTEMPTS - attempt
        if remaining > 0:
            # We do not say which one was wrong (safer for the customer)
            print(f"Incorrect username or PIN. {remaining} attempt(s) left.")

    # Three wrong attempts: lock the account
    print_title("ACCOUNT LOCKED")
    print("Too many incorrect attempts. Your account has been locked.")
    print(f"Please visit your nearest {BANK_NAME.title()} branch or call customer care.")
    return False


# ---------------------------------------------------------------------------
# 6. MAIN MENU
# ---------------------------------------------------------------------------
def show_menu():
    """Print the main menu."""
    print_title("MAIN MENU")
    print("  1.  Balance Enquiry")
    print("  2.  Cash Deposit")
    print("  3.  Cash Withdrawal")
    print("  4.  Transfer Funds")
    print("  5.  Buy Airtime")
    print("  6.  Pay Bills")
    print("  7.  Mini Statement")
    print("  8.  Change PIN")
    print("  9.  View Transaction History")
    print("  10. Print Receipt")
    print("  11. Account Information")
    print("  12. Exit")
    print("=" * LINE_WIDTH)


# ---------------------------------------------------------------------------
# 7. FEATURES (one function per menu option)
# ---------------------------------------------------------------------------
def balance_enquiry():
    """Option 1: show the current balance."""
    print_title("BALANCE ENQUIRY")
    print(f"Available Balance: {money(account['balance'])}")


def cash_deposit():
    """Option 2: add money to the account."""
    print_title("CASH DEPOSIT")
    amount = get_amount("Enter deposit amount (or 'c' to cancel): ")
    if amount is None:
        return False

    record_transaction("Cash Deposit", amount, "Credit")
    print(f"\nDeposit successful. New balance: {money(account['balance'])}")
    return True


def withdrawn_today():
    """Add up all cash withdrawals made today (used for the daily limit)."""
    today = current_date()
    total = 0
    for tx in transactions:
        if tx["type"] == "Cash Withdrawal" and tx["date"] == today:
            total += tx["amount"]
    return total


def cash_withdrawal():
    """Option 3: take money out, respecting balance and daily limit."""
    print_title("CASH WITHDRAWAL")
    left_today = DAILY_WITHDRAWAL_LIMIT - withdrawn_today()
    print(f"Daily limit remaining: {money(left_today)}")

    amount = get_amount("Enter withdrawal amount (or 'c' to cancel): ")
    if amount is None:
        return False

    if amount > left_today:
        print(f"\nDaily withdrawal limit of {money(DAILY_WITHDRAWAL_LIMIT)} exceeded.")
        print(f"You can still withdraw up to {money(left_today)} today.")
        return False
    if not has_enough_balance(amount):
        return False

    record_transaction("Cash Withdrawal", amount, "Debit")
    print("\nPlease take your cash.")
    print(f"Withdrawal successful. New balance: {money(account['balance'])}")
    return True


def transfer_funds():
    """Option 4: send money to another account."""
    print_title("TRANSFER FUNDS")
    recipient_name = get_text("Recipient Name: ")
    recipient_bank = get_text("Recipient Bank: ")
    # Nigerian bank account numbers (NUBAN) have 10 digits
    recipient_account = get_digits("Recipient Account Number (10 digits): ", 10, "account number")
    amount = get_amount("Amount to transfer (or 'c' to cancel): ")
    if amount is None:
        return False

    if not has_enough_balance(amount):
        return False

    record_transaction(f"Transfer to {recipient_name} ({recipient_bank} - {recipient_account})",
                       amount, "Debit")
    print(f"\nTransfer successful. {money(amount)} sent to {recipient_name}.")
    return True


def buy_airtime():
    """Option 5: buy airtime for any phone number."""
    print_title("BUY AIRTIME")
    phone = get_digits("Phone Number (11 digits, e.g. 08012345678): ", 11, "phone number")
    network = choose_from_list(NETWORKS, "Select Network:")

    while True:
        amount = get_amount("Amount (or 'c' to cancel): ")
        if amount is None:
            return False
        if amount < MIN_AIRTIME_AMOUNT:
            print(f"Minimum airtime amount is {money(MIN_AIRTIME_AMOUNT)}.")
        else:
            break

    if not has_enough_balance(amount):
        return False

    record_transaction(f"{network} Airtime ({phone})", amount, "Debit")
    print(f"\nAirtime purchase successful. {money(amount)} {network} airtime sent to {phone}.")
    return True


def pay_bills():
    """Option 6: pay a utility or subscription bill."""
    print_title("PAY BILLS")
    bill = choose_from_list(BILL_TYPES, "Select Bill Type:")
    customer_id = get_text("Customer ID / Meter / Smartcard Number: ")
    amount = get_amount("Amount (or 'c' to cancel): ")
    if amount is None:
        return False

    if not has_enough_balance(amount):
        return False

    record_transaction(f"{bill} Bill ({customer_id})", amount, "Debit")
    print(f"\n{bill} bill payment successful.")
    return True


def print_transaction_rows(tx_list):
    """Print a list of transactions as a table (shared by two features)."""
    print(f"{'Date & Time':<24}{'Type':<30}{'Amount':>15}{'Balance':>15}")
    print("-" * 84)
    for tx in tx_list:
        date_time = f"{tx['date']} {tx['time']}"
        sign = "+" if tx["direction"] == "Credit" else "-"
        amount_text = f"{sign}{money(tx['amount'])}"
        # Cut long descriptions so the table stays tidy
        description = tx["type"][:28]
        print(f"{date_time:<24}{description:<30}{amount_text:>15}{money(tx['balance']):>15}")


def mini_statement():
    """Option 7: account summary plus the last five transactions."""
    print_title("MINI STATEMENT")
    print(f"Username       : {account['username']}")
    print(f"Account Number : {account['account_number']}")
    print(f"Account Name   : {account['account_name']}")
    print(f"Current Balance: {money(account['balance'])}")
    print("\nLast 5 Transactions:")
    if not transactions:
        print("No transactions yet.")
    else:
        print_transaction_rows(transactions[-5:])


def change_pin():
    """Option 8: change the PIN after checking the old one."""
    print_title("CHANGE PIN")
    current_pin = input("Enter current PIN: ").strip()
    if current_pin != account["pin"]:
        print("Incorrect current PIN. PIN not changed.")
        return False

    new_pin = input("Enter new 4-digit PIN: ").strip()
    if not (new_pin.isdigit() and len(new_pin) == 4):
        print("Invalid PIN. It must be exactly 4 digits.")
        return False
    if new_pin == account["pin"]:
        print("New PIN must be different from your current PIN.")
        return False

    confirm_pin = input("Confirm new PIN: ").strip()
    if confirm_pin != new_pin:
        print("PINs do not match. PIN not changed.")
        return False

    account["pin"] = new_pin
    print("\nPIN changed successfully.")
    return True


def view_transaction_history():
    """Option 9: show every transaction."""
    print_title("TRANSACTION HISTORY")
    if not transactions:
        print("No transactions yet.")
    else:
        print_transaction_rows(transactions)
        print(f"\nTotal transactions: {len(transactions)}")


def print_receipt():
    """Option 10: print a receipt for the latest transaction."""
    if not transactions:
        print_title("RECEIPT")
        print("No transactions yet, so there is no receipt to print.")
        return

    latest = transactions[-1]
    print("\n" + "*" * LINE_WIDTH)
    print(BANK_NAME.center(LINE_WIDTH))
    print("TRANSACTION RECEIPT".center(LINE_WIDTH))
    print("*" * LINE_WIDTH)
    print(f"Date             : {latest['date']}")
    print(f"Time             : {latest['time']}")
    print(f"Transaction Type : {latest['type']}")
    print(f"Amount           : {money(latest['amount'])}")
    print(f"Balance          : {money(latest['balance'])}")
    print(f"Status           : {latest['status']}")
    print("*" * LINE_WIDTH)
    print("Thank You for Banking With Us".center(LINE_WIDTH))
    print("*" * LINE_WIDTH)


def account_information():
    """Option 11: show account details."""
    print_title("ACCOUNT INFORMATION")
    print(f"Account Holder Name: {account['account_name']}")
    print(f"Username           : {account['username']}")
    print(f"Account Number     : {account['account_number']}")
    print(f"Account Type       : {account['account_type']}")
    print(f"Current Balance    : {money(account['balance'])}")


# ---------------------------------------------------------------------------
# 8. PROGRAM FLOW
# ---------------------------------------------------------------------------
# Map each menu number to the function that handles it.
# This avoids a very long if/elif chain and keeps main() short.
MENU_ACTIONS = {
    "1": balance_enquiry,
    "2": cash_deposit,
    "3": cash_withdrawal,
    "4": transfer_funds,
    "5": buy_airtime,
    "6": pay_bills,
    "7": mini_statement,
    "8": change_pin,
    "9": view_transaction_history,
    "10": print_receipt,
    "11": account_information,
}


def ask_another_transaction():
    """Ask 'another transaction?' until the user answers Yes or No."""
    while True:
        answer = input("\nDo you want to perform another transaction? (Yes/No): ").strip().lower()
        if answer in ("yes", "y"):
            return True
        if answer in ("no", "n"):
            return False
        print("Please type Yes or No.")


def goodbye():
    """Show the goodbye message."""
    print("\n" + "=" * LINE_WIDTH)
    print(f"Thank you for banking with {BANK_NAME}.".center(LINE_WIDTH))
    print("Please remember to take your card. Goodbye!".center(LINE_WIDTH))
    print("=" * LINE_WIDTH + "\n")


def main():
    """Run the ATM: welcome, login, then the menu loop."""
    welcome_screen()

    if not login():
        return  # account locked, stop the program

    while True:
        show_menu()
        choice = input("Select an option (1-12): ").strip()

        if choice == "12":
            break  # user chose Exit

        action = MENU_ACTIONS.get(choice)
        if action is None:
            # Wrong menu option: show a message and show the menu again
            print("Invalid option. Please enter a number from 1 to 12.")
            continue

        action()

        if not ask_another_transaction():
            break

    goodbye()


# This line makes the program start only when the file is run directly.
if __name__ == "__main__":
    main()
