import requests
from tabulate import tabulate

BASE_URL = "http://127.0.0.1:8000"

def print_menu():
    print("1. Get all accounts")
    print("2. Add a new account")
    print("3. Update an account")
    print("4. Delete an account")
    print("5. Get all groups")
    print("6. Add a new group")
    print("7. Update a group")
    print("8. Delete a group")
    print("9. Get all account groups")
    print("10. Add a new account group")
    print("11. Update an account group")
    print("12. Delete an account group")
    print("0. Exit")

def get_all_accounts():
    response = requests.get(f"{BASE_URL}/accounts")
    accounts_data = response.json()
    if accounts_data.get('accounts'):
        accounts_table = tabulate(accounts_data['accounts'], headers="keys", tablefmt="grid")
        print(accounts_table)
    else:
        print("No accounts found.")


def add_account():
    login = input("Enter login: ")
    password = input("Enter password: ")
    data = {"login": login, "password": password}
    response = requests.post(f"{BASE_URL}/accounts/add", json=data)
    print(response.json())

def update_account():
    account_id = input("Enter account ID to update: ")
    login = input("Enter new login: ")
    password = input("Enter new password: ")
    data = {"login": login, "password": password}
    response = requests.put(f"{BASE_URL}/accounts/update/{account_id}", json=data)
    print(response.json())

def delete_account():
    account_id = input("Enter account ID to delete: ")
    response = requests.delete(f"{BASE_URL}/accounts/delete/{account_id}")
    print(response.json())

# Add similar functions for other CRUD operations

def run_console_app():
    while True:
        print_menu()
        choice = input("Enter your choice (0-12): ")

        if choice == "0":
            break
        elif choice == "1":
            get_all_accounts()
        elif choice == "2":
            add_account()
        elif choice == "3":
            update_account()
        elif choice == "4":
            delete_account()
        # Add similar conditions for other menu options
        else:
            print("Invalid choice. Please enter a number between 0 and 12.")

# Uncomment the line below if you want the console app to run automatically when this module is imported
run_console_app()