import random

# --- DATA STORAGE ---
food_menu = {
    "Samosa Chaat": 3.50,
    "Gulab Jamun Cheesecake": 3.00,
    "Pistachio and Chocolate Cake": 3.80,
    "Baklava": 3.00,
    "Rose Kunafa": 4.00
}

drinks_menu = {
    "Arabic Coffee": 2.50,
    "Karak Chai": 2.00,
    "Pink Chai": 3.50,
    "Mint Tea": 1.50,
    "Mango Lassi": 4.00,
    "Chai Latte": 3.50,
    "Garam Chocolate": 3.50
}

specials_menu = {}


highlighted_books = {
    "The Mountains Echoed": {"price": 3.00, "stock": 3},
    "The Kite Runner": {"price": 3.00, "stock": 3},
    "Thousand Splendid Suns": {"price": 3.00, "stock": 3},
    "The Little Shop in Kabul": {"price": 3.00, "stock": 3}
}

# --- CLASSES ---
class Customer:
    def __init__(self, name, address, is_student=False):
        self.name = name
        self.address = address
        self.is_student = is_student

# --- AUTHENTICATION ---
def register_user(role):
    username = input("Create a username: ")
    password = input("Create a password: ")
    filename = "customers.txt" if role == "customer" else "employees.txt"
    with open(filename, "a") as file:
        file.write(f"{username},{password}\n")
    print("Registration successful.")
    return username

def login_user(role):
    filename = "customers.txt" if role == "customer" else "employees.txt"
    username = input("Username: ")
    password = input("Password: ")
    try:
        with open(filename, "r") as file:
            for line in file:
                stored_user, stored_pass = line.strip().split(",")
                if stored_user == username and stored_pass == password:
                    print(f"Welcome, {username}!")
                    return username
    except FileNotFoundError:
        pass
    print("Invalid credentials.")
    return None

# --- RUMI QUOTES ---
def get_rumi_quote():
    quotes = [
        "'Don't grieve. Anything you lose comes round in new form.'- Rumi",
        "'Let yourself be silently drawn by the strange pull of what you really love.'- Rumi",
        "'Try not to resist the changes that come your way. Instead, embrace them.- Rumi'",
        "'You were born with wings, why prefer to crawl through life?'- Rumi",
        "'Set your life on fire. Seek those who fan your flames.'- Rumi"
    ]
    return random.choice(quotes)

# --- DISPLAY FUNCTIONS ---
def display_menu(menu, title):
    print(f"\n{title}:")
    for item, price in menu.items():
        print(f" - {item}: £{price:.2f}")

def display_books():
    print("\nBooks Available:")
    for book, data in highlighted_books.items():
        print(f" - {book} (Stock: {data['stock']}): £{data['price']:.2f}")

def display_specials():
    if specials_menu:
        print("\n Specials:")
        for item, price in specials_menu.items():
            print(f" - {item}: £{price:.2f}")
    else:
        print("No specials available today.")

# --- EMPLOYEE FUNCTIONS ---
def add_special():
    item = input("Enter special name: ")
    try:
        price = float(input("Enter price: "))
        specials_menu[item] = price
        print(f"Special '{item}' added.")
    except ValueError:
        print("Invalid price.")

def remove_special():
    item = input("Enter name of special to remove: ")
    if item in specials_menu:
        del specials_menu[item]
        print("Special removed.")
    else:
        print("Not found.")

def restock_book():
    book = input("Enter book title to restock: ")
    if book in highlighted_books:
        highlighted_books[book]['stock'] += 1
        print(f"Stock for '{book}' is now {highlighted_books[book]['stock']}.")
    else:
        print("Book not found.")

def employee_menu():
    while True:
        print("\nEmployee Menu:")
        print("1. Add Special")
        print("2. Remove Special")
        print("3. Restock Book")
        print("4. View Specials")
        print("5. Back to Main Menu")
        choice = input("Choose an option: ")
        if choice == "1":
            add_special()
        elif choice == "2":
            remove_special()
        elif choice == "3":
            restock_book()
        elif choice == "4":
            display_specials()
        elif choice == "5":
            break
        else:
            print("Invalid option.")

# --- CUSTOMER EXPERIENCE ---
def search_books():
    cart_item = None
    while True:
        search = input("Search for a book: ").lower()
        found = False
        
        # Search in highlighted books
        for book, data in highlighted_books.items():
            if search in book.lower():
                print(f"Found in Highlighted: {book} (£{data['price']:.2f}, Stock: {data['stock']})")
                add = input("Would you like to add it to your cart? (yes/no): ").lower()
                if add == 'yes':
                    cart_item = (book, data['price'])
                found = True
        
        # If not found in highlighted books, search in the catalog (books.txt)
        if not found:
            try:
                with open('books.txt', 'r') as file:
                    for line in file:
                        # Each line should be in the format "book title, price"
                        catalog_book, catalog_price = line.strip().split(',')
                        if search in catalog_book.lower():
                            try:
                                catalog_price = float(catalog_price)  # Ensure it's a valid price
                                print(f"Found in Catalog: {catalog_book} (£{catalog_price:.2f})")
                                add = input("Would you like to add it to your cart? (yes/no): ").lower()
                                if add == 'yes':
                                    cart_item = (catalog_book, catalog_price)
                                found = True
                                break
                            except ValueError:
                                print(f"Invalid price for '{catalog_book}' in catalog.")
            except FileNotFoundError:
                print("No catalog file found.")

        if not found:
            retry = input("No results. Search again? (yes/no): ").lower()
            if retry != 'yes':
                return None
        else:
            break
    return cart_item

# --- ORDERING ---
def take_order():
    cart = []
    total = 0
    while True:
        item = input("Add item to your cart (or type 'done'): ")
        if item.lower() == 'done':
            break
        if item in food_menu:
            cart.append((item, food_menu[item]))  # Stores the item and its price as a tuple
            total += food_menu[item]
            print(f"Added '{item}' to your order.Total so far: £{total:.2f}")
        elif item in drinks_menu:
            cart.append((item, drinks_menu[item]))  # Stores the item and its price as a tuple
            total += drinks_menu[item]
            print(f"Added '{item}' to your order.Total so far: £{total:.2f}")
        elif item in specials_menu:
            cart.append((item, specials_menu[item]))  # Stores the item and its price as a tuple
            total += specials_menu[item]
            print(f"Added '{item}' to your order.Total so far: £{total:.2f}")
        elif item in highlighted_books:
            if highlighted_books[item]['stock'] > 0:
                cart.append((item, highlighted_books[item]['price']))  # Stores the item and its price as a tuple
                total += highlighted_books[item]['price']
                highlighted_books[item]['stock'] -= 1
                print(f"Added '{item}' to your order.Total so far: £{total:.2f}")
            else:
                print("Sorry, out of stock.")
        else:
            print("Item not found.")
    return cart, total

# --- CUSTOMER MENU ---
def customer_menu():
    print(f"\nWelcome to Chapters & Chai! - Where every sip tells a story, and every page opens a new adventure... \n{get_rumi_quote()}")
   
    name = input("Your name: ")
    address = input("Your address: ")
    is_student = input("Are you a student? (yes/no): ").lower() == 'yes'
    delivery = input("Are you dining in or requesting delivery? ").lower()
    customer = Customer(name, address, is_student)

    display_books()
    display_menu(food_menu, "Food Menu")
    display_menu(drinks_menu, "Drinks Menu")
    display_specials()

    cart, total = take_order()

    search_more = input("Would you like to search for a book to add? (yes/no): ").lower()
    if search_more == 'yes':
        book = search_books()
        if book:
            cart.append(book)  # If the book is found in catalog or highlighted
            total += book[1]  # Add the price from the book tuple

    if is_student:
        total *= 0.85
        print("\nYour 15% Student Discount has been added to your order summary:")

    print("\n--- Order Summary ---")
    for item, price in cart:  # This prints each item and its price
        print(f" - {item}: £{price:.2f}")
    print(f"Total: £{total:.2f}")

    file_name = "delivery_orders.txt" if delivery == "delivery" else "dinein_orders.txt"
    with open(file_name, "a") as file:
        file.write(f"Customer: {customer.name}, Address: {customer.address}\n")
        for item, price in cart:  # This writes each item and its price to the file
            file.write(f" - {item}: £{price:.2f}\n")
        file.write(f"Total: £{total:.2f}\n\n")

# --- MAIN MENU ---
while True:
    print("\nChapters & Chai Main Menu:")
    print("1. Customer")
    print("2. Employee")
    print("3. Exit")
    choice = input("Choose: ")

    if choice == "1":
        action = input("Login or Register? ").lower()
        if action == 'register':
            register_user("customer")
        elif action == 'login':
            if login_user("customer"):
                customer_menu()
    elif choice == "2":
        action = input("Login or Register? ").lower()
        if action == 'register':
            register_user("employee")
        elif action == 'login':
            if login_user("employee"):
                employee_menu()
    elif choice == "3":
        print("Thank you for visiting Chapters & Chai!")
        break
    else:
        print("Invalid option.")


