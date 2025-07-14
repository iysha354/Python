import datetime
import os

# ------------------- Data Structures -------------------
users = []
events = []
signups = []
current_user = None
REWARD_MILESTONES = [5, 10, 20]  # hours

# ------------------- Classes -------------------
class User:
    def __init__(self, name, email, password, role, volunteer_type=None):
        self.name = name
        self.email = email
        self.password = password
        self.role = role  # 'admin' or 'volunteer'
        self.volunteer_type = volunteer_type
        self.total_hours = 0

class Event:
    def __init__(self, name, date, description):
        self.id = len(events) + 1
        self.name = name
        self.date = date
        self.description = description
        self.team_lead = None
        self.cancelled = False

class Signup:
    def __init__(self, user_email, event_id):
        self.user_email = user_email
        self.event_id = event_id
        self.hours_logged = 0
        self.cancelled = False
        self.cancel_reason = ""

# ------------------- File Operations -------------------
def load_users():
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 4:
                    name, email, password, role = parts[:4]
                    volunteer_type = parts[4] if role == "volunteer" else None
                    users.append(User(name, email, password, role, volunteer_type))

def save_user(user):
    with open("users.txt", "a") as f:
        line = f"{user.name}|{user.email}|{user.password}|{user.role}|{user.volunteer_type or ''}\n"
        f.write(line)

# ------------------- Auth Functions -------------------
def register():
    print("Register New User")
    name = input("Name: ")
    email = input("Email: ")
    password = input("Password: ")
    role = input("Role (admin/volunteer): ").strip().lower()
    volunteer_type = None

    if role == "volunteer":
        volunteer_type = input("Are you a cook or host? ").strip().lower()

    user = User(name, email, password, role, volunteer_type)
    users.append(user)
    save_user(user)
    print(f"User '{name}' registered as {role}.")

def login():
    global current_user
    print("Login")
    email = input("Email: ")
    password = input("Password: ")

    for user in users:
        if user.email == email and user.password == password:
            current_user = user
            print(f"Welcome, {user.name}!")
            return True

    print("Login failed.")
    return False

# ------------------- Event Functions -------------------
def create_event():
    name = input("Event name: ")
    date = input("Event date (YYYY-MM-DD): ")
    desc = input("Description: ")
    event = Event(name, date, desc)
    events.append(event)
    print("Event created.")

def cancel_event():
    view_events()
    eid = int(input("Enter Event ID to cancel: "))
    for event in events:
        if event.id == eid:
            event.cancelled = True
            print("Event cancelled.")

def assign_team_lead():
    view_events()
    eid = int(input("Event ID to assign a lead: "))
    email = input("Volunteer email: ")
    for e in events:
        if e.id == eid:
            e.team_lead = email
            print(f"Assigned {email} as team lead for {e.name}. (Simulated alert sent)")

def view_events():
    print("\nUpcoming Events:")
    for e in events:
        status = "CANCELLED" if e.cancelled else "ACTIVE"
        print(f"[{e.id}] {e.name} - {e.date} - {status}")
        print(f"   Description: {e.description}")
        if e.team_lead:
            print(f"   Team Lead: {e.team_lead}")

# ------------------- Volunteer Menu -------------------
def volunteer_menu():
    while True:
        print("\nVolunteer Menu")
        print("1. View Events")
        print("2. Sign Up for Event")
        print("3. Log Hours")
        print("4. Cancel Sign-up")
        print("5. Redeem Reward")
        print("6. Logout")

        choice = input("Select: ")

        if choice == "1":
            view_events()

        elif choice == "2":
            view_events()
            eid = int(input("Enter Event ID: "))
            if any(s.user_email == current_user.email and s.event_id == eid for s in signups):
                print("Already signed up.")
            else:
                signups.append(Signup(current_user.email, eid))
                print("Signed up successfully.")

        elif choice == "3":
            for s in signups:
                if s.user_email == current_user.email and not s.cancelled:
                    print(f"Event ID {s.event_id}: {s.hours_logged} hours")
            eid = int(input("Event ID to log hours for: "))
            hours = int(input("Hours to log: "))
            for s in signups:
                if s.user_email == current_user.email and s.event_id == eid:
                    s.hours_logged += hours
                    current_user.total_hours += hours
                    print("Hours logged.")

        elif choice == "4":
            eid = int(input("Event ID to cancel signup for: "))
            for s in signups:
                if s.user_email == current_user.email and s.event_id == eid:
                    s.cancelled = True
                    s.cancel_reason = input("Reason for cancellation: ")
                    print("Signup cancelled.")
                    break

        elif choice == "5":
            for milestone in REWARD_MILESTONES:
                if current_user.total_hours >= milestone:
                    print(f"🎉 You’ve earned a reward for {milestone} hours!")

        elif choice == "6":
            break

# ------------------- Admin Menu -------------------
def admin_menu():
    while True:
        print("\nAdmin Menu")
        print("1. Create Event")
        print("2. Cancel Event")
        print("3. Assign Team Lead")
        print("4. View Events")
        print("5. Logout")
        choice = input("Select: ")

        if choice == "1":
            create_event()
        elif choice == "2":
            cancel_event()
        elif choice == "3":
            assign_team_lead()
        elif choice == "4":
            view_events()
        elif choice == "5":
            break

# ------------------- Main Program -------------------
def main():
    load_users()
    print("Volunteer Management System")

    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose: ")

        if choice == "1":
            register()
        elif choice == "2":
            if login():
                if current_user.role == "admin":
                    admin_menu()
                else:
                    volunteer_menu()
        elif choice == "3":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
