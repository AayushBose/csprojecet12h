import mysql.connector
import os

# ============== LOGIN/SIGNUP FUNCTIONS ==============

USERS_FILE = "users.txt"
ADMINS_FILE = "admins.txt"

def load_users():
    """Load all users from users.txt file."""
    users = {}
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split(",")
                        if len(parts) == 3:
                            username, userid, password = parts
                            users[username] = {"userid": int(userid), "password": password}
        except Exception as e:
            print(f"Error loading users: {e}")
    return users

def save_users(users):
    """Save all users to users.txt file."""
    try:
        with open(USERS_FILE, "w") as f:
            for username, data in users.items():
                f.write(f"{username},{data['userid']},{data['password']}\n")
    except Exception as e:
        print(f"Error saving users: {e}")

def signup():
    """Handle user signup."""
    print("\n========== SIGNUP ==========")
    users = load_users()
    
    username = input("Enter username: ").strip()
    if username in users:
        print("Username already exists! Please try another.")
        return None
    
    password = input("Enter password: ").strip()
    
    # Generate a new userid (simple approach: max existing + 1)
    userid = max([data["userid"] for data in users.values()], default=10) + 1
    
    users[username] = {"userid": userid, "password": password}
    save_users(users)
    
    print(f"Signup successful! Username: {username}, UserID: {userid}")
    return userid, username

def login():
    """Handle user login."""
    print("\n========== LOGIN ==========")
    users = load_users()
    
    username = input("Enter username: ").strip()
    if username not in users:
        print("Username not found. Exiting...")
        return None
    
    max_attempts = 3
    for attempt in range(max_attempts):
        password = input("Enter password: ").strip()
        if password == users[username]["password"]:
            userid = users[username]["userid"]
            print(f"Login successful! Welcome, {username}!")
            return userid, username
        else:
            remaining = max_attempts - attempt - 1
            if remaining > 0:
                print(f"Wrong password. Try again. ({remaining} attempts left)")
            else:
                print("Too many failed attempts. Exiting...")
                return None
    
    return None

# ============== ADMIN LOGIN/SIGNUP FUNCTIONS ==============

def load_admins():
    """Load all admins from admins.txt file."""
    admins = {}
    if os.path.exists(ADMINS_FILE):
        try:
            with open(ADMINS_FILE, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split(",")
                        if len(parts) == 3:
                            username, adminid, password = parts
                            admins[username] = {"adminid": int(adminid), "password": password}
        except Exception as e:
            print(f"Error loading admins: {e}")
    return admins

def save_admins(admins):
    """Save all admins to admins.txt file."""
    try:
        with open(ADMINS_FILE, "w") as f:
            for username, data in admins.items():
                f.write(f"{username},{data['adminid']},{data['password']}\n")
    except Exception as e:
        print(f"Error saving admins: {e}")

def admin_login():
    """Handle admin login."""
    print("\n========== ADMIN LOGIN ==========")
    admins = load_admins()
    
    username = input("Enter admin username: ").strip()
    if username not in admins:
        print("Admin username not found. Exiting...")
        return None
    
    max_attempts = 3
    for attempt in range(max_attempts):
        password = input("Enter admin password: ").strip()
        if password == admins[username]["password"]:
            adminid = admins[username]["adminid"]
            print(f"Admin login successful! Welcome, {username}!")
            return adminid, username
        else:
            remaining = max_attempts - attempt - 1
            if remaining > 0:
                print(f"Wrong password. Try again. ({remaining} attempts left)")
            else:
                print("Too many failed attempts. Exiting...")
                return None
    
    return None

def admin_signup():
    """Handle admin signup (with a master password check for security)."""
    print("\n========== ADMIN SIGNUP ==========")
    master_pwd = input("Enter master password (for admin registration): ").strip()
    if master_pwd != "Pass@123":  # Simple check; should be hashed in production
        print("Invalid master password. Access denied.")
        return None
    
    admins = load_admins()
    
    username = input("Enter admin username: ").strip()
    if username in admins:
        print("Admin username already exists! Please try another.")
        return None
    
    password = input("Enter admin password: ").strip()
    
    # Generate a new adminid (simple approach: max existing + 1)
    adminid = max([data["adminid"] for data in admins.values()], default=100) + 1
    
    admins[username] = {"adminid": adminid, "password": password}
    save_admins(admins)
    
    print(f"Admin signup successful! Username: {username}, AdminID: {adminid}")
    return adminid, username

# ============== PRODUCT MANAGEMENT FUNCTIONS (ADMIN) ==============

def view_product_table(cursor):
    """Display all products in the PRODUCT table."""
    print("\n========== CURRENT PRODUCT INVENTORY ==========")
    try:
        cursor.execute("SELECT * FROM PRODUCT")
        products = cursor.fetchall()
        
        if not products:
            print("No products found in the table.")
            return
        
        print("{:<10} {:<25} {:<10} {:<10}".format("ProductId", "Name", "Quantity", "Price"))
        print("-" * 60)
        for row in products:
            print("{:<10} {:<25} {:<10} {:<10}".format(row[0], row[1], row[2], row[3]))
        print("-" * 60)
    except Exception as e:
        print(f"Error viewing products: {e}")

def add_product_to_table(cursor, conn):
    """Add a new product to the PRODUCT table."""
    print("\n========== ADD NEW PRODUCT ==========")
    try:
        product_id = int(input("Enter Product ID: ").strip())
        name = input("Enter Product Name: ").strip()
        quantity = int(input("Enter Quantity: ").strip())
        price = float(input("Enter Price: ").strip())
        
        # Check if product already exists
        cursor.execute("SELECT * FROM PRODUCT WHERE ProductId = %s", (product_id,))
        if cursor.fetchone():
            print(f"Error: Product with ID {product_id} already exists.")
            return
        
        cursor.execute(
            "INSERT INTO PRODUCT (ProductId, Name, Quantity, Price) VALUES (%s, %s, %s, %s)",
            (product_id, name, quantity, price)
        )
        conn.commit()
        print(f"✓ Product '{name}' (ID: {product_id}) added successfully!")
    except ValueError:
        print("Error: Invalid input. Please enter correct data types (ID: int, Name: string, Quantity: int, Price: float).")
    except Exception as e:
        print(f"Error adding product: {e}")

def delete_product_from_table(cursor, conn):
    """Delete a product from the PRODUCT table."""
    print("\n========== DELETE PRODUCT ==========")
    try:
        product_id = int(input("Enter Product ID to delete: ").strip())
        
        # Check if product exists
        cursor.execute("SELECT Name FROM PRODUCT WHERE ProductId = %s", (product_id,))
        result = cursor.fetchone()
        
        if not result:
            print(f"Error: Product with ID {product_id} not found.")
            return
        
        product_name = result[0]
        confirm = input(f"Are you sure you want to delete '{product_name}' (ID: {product_id})? (yes/no): ").strip().lower()
        
        if confirm != "yes":
            print("Deletion cancelled.")
            return
        
        cursor.execute("DELETE FROM PRODUCT WHERE ProductId = %s", (product_id,))
        conn.commit()
        print(f"✓ Product '{product_name}' (ID: {product_id}) deleted successfully!")
    except ValueError:
        print("Error: Invalid input. Please enter a valid Product ID (integer).")
    except Exception as e:
        print(f"Error deleting product: {e}")

def update_product_column(cursor, conn):
    """Update a specific column in a product record."""
    print("\n========== UPDATE PRODUCT ==========")
    try:
        product_id = int(input("Enter Product ID to update: ").strip())
        
        # Check if product exists
        cursor.execute("SELECT * FROM PRODUCT WHERE ProductId = %s", (product_id,))
        result = cursor.fetchone()
        
        if not result:
            print(f"Error: Product with ID {product_id} not found.")
            return
        
        print("\nWhat would you like to update?")
        print("1. Product Name")
        print("2. Quantity")
        print("3. Price")
        
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == "1":
            new_name = input("Enter new Product Name: ").strip()
            cursor.execute("UPDATE PRODUCT SET Name = %s WHERE ProductId = %s", (new_name, product_id))
            conn.commit()
            print(f"✓ Product name updated to '{new_name}'")
        elif choice == "2":
            new_quantity = int(input("Enter new Quantity: ").strip())
            cursor.execute("UPDATE PRODUCT SET Quantity = %s WHERE ProductId = %s", (new_quantity, product_id))
            conn.commit()
            print(f"✓ Product quantity updated to {new_quantity}")
        elif choice == "3":
            new_price = float(input("Enter new Price: ").strip())
            cursor.execute("UPDATE PRODUCT SET Price = %s WHERE ProductId = %s", (new_price, product_id))
            conn.commit()
            print(f"✓ Product price updated to {new_price}")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Error: Invalid input. Please enter correct data types.")
    except Exception as e:
        print(f"Error updating product: {e}")

def admin_menu(cursor, conn):
    """Admin menu for managing products."""
    while True:
        print("\n========== ADMIN MENU ==========")
        print("1. View all products")
        print("2. Add new product")
        print("3. Update product")
        print("4. Delete product")
        print("5. Logout")
        
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == "1":
            view_product_table(cursor)
        elif choice == "2":
            add_product_to_table(cursor, conn)
        elif choice == "3":
            update_product_column(cursor, conn)
        elif choice == "4":
            delete_product_from_table(cursor, conn)
        elif choice == "5":
            print("Logging out from admin account. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# ============== USER CART FUNCTIONS ==============

def display_products(cursor, title="Product Table"):
    """Display all products for users."""
    cursor.execute("SELECT * FROM PRODUCT")
    products = cursor.fetchall()
    print(title)
    print("{:<10} {:<25} {:<10} {:<10}".format("ProductId", "Name", "Quantity", "Price"))
    for row in products:
        print("{:<10} {:<25} {:<10} {:<10}".format(row[0], row[1], row[2], row[3]))
    print()

def cart_operations(cursor, conn):
    """Handle add/remove/checkout and return the final cart dict."""
    display_products(cursor, "Product Table Before Cart Operations:")
    cart = {}

    while True:
        action = input("Type 'add' to add, 'remove' to remove, 'view' to view cart, 'checkout' to finish: ").lower()
        if action == 'checkout':
            break

        if action == 'view':
            if not cart:
                print("Your cart is empty.")
            else:
                print("\nCurrent cart contents:")
                print("{:<10} {:<30} {:<10} {:<10} {:<10}".format("ProductId", "Name", "Quantity", "Price", "Subtotal"))
                cart_total = 0
                for pid, qty in cart.items():
                    cursor.execute("SELECT Name, Price FROM PRODUCT WHERE ProductId = %s", (pid,))
                    res = cursor.fetchone()
                    if res:
                        name, price = res
                        subtotal = price * qty
                        cart_total += subtotal
                        print("{:<10} {:<30} {:<10} {:<10} {:<10}".format(pid, name, qty, price, subtotal))
                    else:
                        print("{:<10} {:<30} {:<10}".format(pid, "<deleted>", qty))
                print(f"Total: {cart_total}\n")
            continue

        # for add/remove, prompt for product and quantity
        try:
            item_num = int(input("Enter ProductId: "))
            quantity = int(input("Enter quantity: "))
        except ValueError:
            print("Please enter valid integers for ProductId and quantity.")
            continue

        # Fetch product to check stock
        cursor.execute("SELECT Quantity FROM PRODUCT WHERE ProductId=%s", (item_num,))
        result = cursor.fetchone()
        if not result:
            print("Invalid ProductId!")
            continue
        stock = result[0]

        if action == 'add':
            if quantity > stock:
                print("Not enough stock!")
            else:
                cart[item_num] = cart.get(item_num, 0) + quantity
                cursor.execute(
                    "UPDATE PRODUCT SET Quantity = Quantity - %s WHERE ProductId = %s",
                    (quantity, item_num)
                )
                conn.commit()
                print(f"Added {quantity} of ProductId {item_num} to cart.")
        elif action == 'remove':
            if item_num in cart and cart[item_num] >= quantity:
                cart[item_num] -= quantity
                if cart[item_num] == 0:
                    del cart[item_num]
                cursor.execute(
                    "UPDATE PRODUCT SET Quantity = Quantity + %s WHERE ProductId = %s",
                    (quantity, item_num)
                )
                conn.commit()
                print(f"Removed {quantity} of ProductId {item_num} from cart.")
            else:
                print("Item not in cart or quantity to remove is invalid.")
        else:
            print("Unknown action. Use 'add', 'remove', 'view' or 'checkout'.")

    display_products(cursor, "Product Table After Cart Operations:")
    return cart

def update_orders(cursor, conn, userid, username, cart):
    """Persist the user's cart to the ORDERS table (insert or update)."""
    if not cart:
        print("\nCart is empty. No order to insert/update.")
        return

    # Calculate total amount
    total_amount = 0
    for item_id, qty in cart.items():
        cursor.execute("SELECT Price FROM PRODUCT WHERE ProductId = %s", (item_id,))
        result = cursor.fetchone()
        if result:
            price = result[0]
            total_amount += price * qty

    cart_str = ",".join([f"{item_id}:{qty}" for item_id, qty in cart.items()])
    Pno = input("Enter your phone number: ").strip()

    cursor.execute("SELECT * FROM ORDERS WHERE Userid = %s", (userid,))
    result = cursor.fetchone()

    print(f"Prepared cart string: {cart_str}")
    print(f"Prepared total amount: {total_amount}")

    if result:
        cursor.execute(
            "UPDATE ORDERS SET item_quantity = %s, total_amount = %s, Pno = %s WHERE Userid = %s",
            (cart_str, total_amount, Pno, userid)
        )
        print("Cart updated for existing user.")
    else:
        cursor.execute(
            "INSERT INTO ORDERS (Userid, Username, Pno, item_quantity, total_amount) VALUES (%s, %s, %s, %s, %s)",
            (userid, username, Pno, cart_str, total_amount)
        )
        print("New order added for user.")

    conn.commit()
    print("Order saved to ORDERS table successfully!")

# ============== MAIN PROGRAM ==============

print("Welcome to Shopping Cart System!")
print("1. User Login/Signup")
print("2. Admin Login/Signup")
role_choice = input("Choose (1/2): ").strip()

if role_choice == "2":
    # Admin path
    print("\n1. Admin Login")
    print("2. Admin Signup")
    admin_choice = input("Enter choice (1/2): ").strip()
    
    if admin_choice == "1":
        result = admin_login()
    elif admin_choice == "2":
        result = admin_signup()
    else:
        print("Invalid choice. Exiting.")
        exit()
    
    if result is None:
        exit()
    
    adminid, admin_username = result
    
    # Connect to MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pass@123",
        database="Shopping")
    
    cursor = conn.cursor()
    
    try:
        admin_menu(cursor, conn)
    finally:
        cursor.close()
        conn.close()

elif role_choice == "1":
    # User path
    print("\n1. User Login")
    print("2. User Signup")
    user_choice = input("Enter choice (1/2): ").strip()
    
    if user_choice == "1":
        result = login()
    elif user_choice == "2":
        result = signup()
    else:
        print("Invalid choice. Exiting.")
        exit()
    
    if result is None:
        exit()
    
    userid, username = result
    
    # Connect to MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pass@123",
        database="Shopping")
    
    cursor = conn.cursor()
    
    try:
        cart = cart_operations(cursor, conn)
        update_orders(cursor, conn, userid, username, cart)
    finally:
        cursor.close()
        conn.close()
else:
    print("Invalid choice. Exiting.")
    exit()
