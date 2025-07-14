# Work Social Budget Tracker with Per-Employee Budgets
from datetime import datetime

# -------------------- File Paths --------------------
users_file = "users.txt"
expenses_file = "expenses.txt"
pending_expenses_file = "pending_expenses.txt"

# -------------------- Default Budget Template --------------------
# All new employees get this monthly budget per category
default_budget = {
    "lunch": 100.0,
    "transport": 50.0,
    "accommodation": 100.0,
    "other": 50.0
}

department_budget = {
    "Marketing":1000,
    "Sales":1000,
    "Recruitment":1000,
    "Finance":1000,
    "HR":1000
}

# -------------------- Load & Save Functions --------------------
def load_users():
    """Loads all users from the users file."""
    users = {}
    try:
        with open(users_file, "r") as f:
            for line in f:
                username, password, role, department = line.strip().split(",")
                users[username] = {
                    "password": password,
                    "role": role,
                    "department": department
                }
    except FileNotFoundError:
        pass
    return users

def save_user(username, password, role, department):
    """Saves a new user to the file and sets up their default budget if employee."""
    with open(users_file, "a") as f:
        f.write(f"{username},{password},{role},{department}\n")
    if role == "employee":
        employee_budgets[username] = default_budget.copy()

# Dictionary to hold in-memory employee budgets
employee_budgets = {}

# -------------------- Expense File Handling --------------------
def load_expenses(filepath):
    """Loads all expenses from a given file."""
    try:
        with open(filepath, "r") as f:
            return [eval(line.strip()) for line in f]
    except FileNotFoundError:
        return []

def save_expenses(filepath, data):
    """Saves a list of expenses to a file."""
    with open(filepath, "w") as f:
        for entry in data:
            f.write(str(entry) + "\n")

# -------------------- Authentication --------------------
def register():
    """Handles user registration."""
    print("\nRegister")
    username = input("Username: ").strip()
    users = load_users()

    if username in users:
        print("User already exists.")
        return

    password = input("Password: ").strip()
    role = input("Role (employee/manager): ").strip().lower()
    if role not in ["employee", "manager"]:
        print("Invalid role.")
        return

    department = input("Department: ").strip()
    save_user(username, password, role, department)
    print("Registered successfully.")

def login():
    """Handles user login."""
    print("\nLogin")
    users = load_users()
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    user = users.get(username)
    if user and user["password"] == password:
        return username, user["role"], user["department"]
    else:
        print("Login failed.")
        return None, None, None

# -------------------- Expense Management --------------------
def add_expense(username, role, department, expenses, pending_expenses):
    """Adds a new expense, checks against budget, and sends for approval if needed."""
    category = input("Category (lunch, transport, accommodation, other): ").lower()
    event = input("Event details: ")
    amount = float(input("Amount: "))
    date = datetime.today().strftime('%Y-%m-%d')

    entry = {
        "user": username,
        "role": role,
        "department": department,
        "category": category,
        "amount": amount,
        "event": event,
        "date": date
    }

    if role == "manager":
        expenses.append(entry)
        save_expenses(expenses_file, expenses)
        print("Expense added.")
        return

    # For employees, enforce budget limits
    personal_budget = employee_budgets.get(username, default_budget.copy())
    limit = personal_budget.get(category)
    if limit is None:
        print("Invalid category. Sent to manager for approval.")
        pending_expenses.append(entry)
        save_expenses(pending_expenses_file, pending_expenses)
        return

    spent = sum(e["amount"] for e in expenses if e["user"] == username and e["category"] == category)
    if spent + amount <= limit:
        expenses.append(entry)
        save_expenses(expenses_file, expenses)
        print("Expense approved.")
    else:
        print("Over budget — sent to manager for approval.")
        pending_expenses.append(entry)
        save_expenses(pending_expenses_file, pending_expenses)

def view_personal_expenses(username, expenses):
    """Displays all expenses for the logged-in employee."""
    print(f"\nYour Expenses, {username}:")
    for e in expenses:
        if e["user"] == username:
            print(f"- {e['date']} | {e['category']} | £{e['amount']:.2f} | {e['event']}")

def view_department_summary(department, expenses):
    """Shows total department spend by category."""
    print(f"\nSummary for {department}")
    category_totals = {}
    for e in expenses:
        if e["department"] == department:
            cat = e["category"]
            category_totals[cat] = category_totals.get(cat, 0) + e["amount"]
    for cat, amt in category_totals.items():
        print(f"- {cat}: £{amt:.2f}")

    total_spent = sum(category_totals.values())
    budget = department_budget.get(department)
    
    if budget is not None:
        print(f"Total spent: £{total_spent:.2f}")
        print(f"Budget: £{budget:.2f}")
        remaining = budget - total_spent
        print(f"Remaining budget: £{remaining:.2f}")
    else:
        print("No budget set for this department.")

def view_employee_spend(expenses):
    """Shows each employee's total spend."""
    print("\nEmployee Spend Summary")
    totals = {}
    for e in expenses:
        if e.get("role") == "employee":
            user = e["user"]
            totals[user] = totals.get(user, 0) + e["amount"]
    for user, total in totals.items():
        print(f"- {user}: £{total:.2f}")

def view_employee_expense_details(expenses):
    """Shows detailed breakdown of each employee's expenses."""
    print("\nEmployee Expense Details")
    details = {}
    for e in expenses:
        if e.get("role") == "employee":
            details.setdefault(e["user"], []).append(e)
    for user, entries in details.items():
        print(f"\n{user}:")
        for e in entries:
            print(f"- {e['date']} | {e['category']} | £{e['amount']:.2f} | {e['event']}")

def approve_expenses(expenses, pending_expenses):
    """Allows a manager to approve pending expenses."""
    if not pending_expenses:
        print("No pending expenses.")
        return
    for i, e in enumerate(pending_expenses):
        print(f"{i+1}. {e['user']} | {e['category']} | £{e['amount']} | {e['event']}")
    for i in range(len(pending_expenses)):
        choice = input(f"Approve {i+1}? (y/n): ").lower()
        if choice == 'y':
            expenses.append(pending_expenses[i])
    pending_expenses.clear()
    save_expenses(expenses_file, expenses)
    save_expenses(pending_expenses_file, pending_expenses)
    print("Approvals complete.")

# -------------------- Menus --------------------
def employee_menu(username, role, department):
    while True:
        print("\nEmployee Menu")
        print("1. Add Expense")
        print("2. View My Expenses")
        print("3. Logout")
        choice = input("Choose: ")
        if choice == '1':
            add_expense(username, role, department, load_expenses(expenses_file), load_expenses(pending_expenses_file))
        elif choice == '2':
            view_personal_expenses(username, load_expenses(expenses_file))
        elif choice == '3':
            break

def manager_menu(username, department):
    while True:
        print("\nManager Menu")
        print("1. Add Expense")
        print("2. View Dept Summary")
        print("3. View Employee Spend")
        print("4. View Employee Expense Details")
        print("5. Approve Expenses")
        print("6. Logout")
        choice = input("Choose: ")
        if choice == '1':
            add_expense(username, "manager", department, load_expenses(expenses_file), load_expenses(pending_expenses_file))
        elif choice == '2':
            view_department_summary(department, load_expenses(expenses_file))
        elif choice == '3':
            view_employee_spend(load_expenses(expenses_file))
        elif choice == '4':
            view_employee_expense_details(load_expenses(expenses_file))
        elif choice == '5':
            approve_expenses(load_expenses(expenses_file), load_expenses(pending_expenses_file))
        elif choice == '6':
            break

# -------------------- App Entry Point --------------------
def main():
    while True:
        print("\nWork Social Budget Tracker")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Select: ")
        if choice == '1':
            username, role, department = login()
            if role == 'employee':
                employee_menu(username, role, department)
            elif role == 'manager':
                manager_menu(username, department)
        elif choice == '2':
            register()
        elif choice == '3':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()


