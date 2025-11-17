import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pass@123",
    database="Shopping")

cursor = conn.cursor()

# Display PRODUCT table
cursor.execute("SELECT * FROM PRODUCT")
products = cursor.fetchall()
print("Product Table Before Cart Operations:")
# Print header row with fixed widths
print("{:<10} {:<25} {:<10} {:<10}".format("ProductId", "Name", "Quantity", "Price"))
# Print all rows with same fixed widths
for row in products:
    print("{:<10} {:<25} {:<10} {:<10}".format(row[0], row[1], row[2], row[3]))

# Initialize empty cart
cart = {}

# Main cart operation loop
while True:
    action = input("Type 'add' to add, 'remove' to remove, 'checkout' to finish: ").lower()
    if action == 'checkout':
        break
    item_num = int(input("Enter ProductId: "))
    quantity = int(input("Enter quantity: "))
    
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

# Display PRODUCT table after operations
cursor.execute("SELECT * FROM PRODUCT")
products = cursor.fetchall()
print("\nProduct Table After Cart Operations:")
# Print headers first for clarity
# Print header row with fixed widths
print("{:<10} {:<25} {:<10} {:<10}".format("ProductId", "Name", "Quantity", "Price"))

# Print all rows with same fixed widths
for row in products:
    print("{:<10} {:<25} {:<10} {:<10}".format(row[0], row[1], row[2], row[3]))





cursor.close()
conn.close()


import mysql.connector

# Connect to your database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pass@123",
    database="Shopping"
)
cursor = conn.cursor() 

# Use the `cart` populated earlier by user interactions.
# Do not overwrite it with an example cart. If it's empty, skip order update.
if not cart:
    print("Cart is empty. No order to insert/update.")
else:
    # Calculate total amount
    total_amount = 0
    for item_id, qty in cart.items():
        cursor.execute("SELECT Price FROM PRODUCT WHERE ProductId = %s", (item_id,))
        result = cursor.fetchone()
        if result:
            price = result[0]
            total_amount += price * qty

    # Format cart as item:quantity string
    cart_str = ",".join([f"{item_id}:{qty}" for item_id, qty in cart.items()])

    # Prepare data (replace with real user data as needed)
    Userid = 11
    Username = "Keshav"
    Pno = 9812345677

    # Check if user already has an entry in ORDERS
    cursor.execute("SELECT * FROM ORDERS WHERE Userid = %s", (Userid,))
    result = cursor.fetchone()

    # Debug: show what will be written
    print(f"Prepared cart string: {cart_str}")
    print(f"Prepared total amount: {total_amount}")

    if result:
        # User exists: update their order
        cursor.execute(
            "UPDATE ORDERS SET item_quantity = %s, total_amount = %s WHERE Userid = %s",
            (cart_str, total_amount, Userid)
        )
        print("Cart updated for existing user.")
    else:
        # User does not exist: create new order
        cursor.execute(
            "INSERT INTO ORDERS (Userid, Username, Pno, item_quantity, total_amount) VALUES (%s, %s, %s, %s, %s)",
            (Userid, Username, Pno, cart_str, total_amount)
        )
        print("New order added for user.")

    conn.commit()
    cursor.close()
    conn.close()
