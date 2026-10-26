"""
INF1103 Week 5 - Inventory Manager
"""
import json
# Global Constant
INVENTORY_FILE = "inventory.json"


# ---------------------------------------------------------------
# Persistence Functions (no UI prompt and printing)
# ---------------------------------------------------------------
def load_inventory():
    inventory = []
    try:
        with open(INVENTORY_FILE, "r") as file:
            inventory = json.load(file)
        status = "loaded"
    except FileNotFoundError:
        inventory = []
        status = "not_found"
    except (json.JSONDecodeError, OSError):
        inventory = []
        status = "error"
    return inventory, status


def save_inventory(inventory):
    """Save inventory to INVENTORY_FILE. Returns True if successful."""
    try:
        with open(INVENTORY_FILE, "w") as file:
            json.dump(inventory, file, indent=4)
        return True
    except OSError:
        return False


# ---------------------------------------------------------------
# Data Functions (no UI prompt and printing)
# ---------------------------------------------------------------
def search_product(inventory, product_id):
    """Search by product id. Returns the product dict or None."""
    for product in inventory:
        if product["id"] == product_id:
            return product
    return None


def add_product(inventory, product_id, name, price, stock):
    """Add a new product. Returns False if the id already exists."""
    if search_product(inventory, product_id) is not None:
        return False
    inventory.append({
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock
    })
    return True


def update_stock(inventory, product_id, new_stock):
    """Update stock of an existing product. Returns False if not found."""
    product = search_product(inventory, product_id)
    if product is None:
        return False
    product["stock"] = new_stock
    return True


# ---------------------------------------------------------------
# Part of UI
# ---------------------------------------------------------------
def display_all(inventory):
    """Print all products in the inventory."""
    print("\nCurrent Inventory")
    print("-" * 48)
    if len(inventory) == 0:
        print("No products in inventory.")
    for p in inventory:
        print(f"ID: {p['id']} | Name: {p['name']} | "
              f"Price: ${p['price']:.2f} | Stock: {p['stock']}")
    print("-" * 48)


def print_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def read_number(prompt, number_type=float):
    """Prompt until a non-negative number of number_type (int or float) is entered."""
    while True:
        try:
            value = number_type(input(prompt))
            if value < 0:
                print("Value cannot be negative. Try again.")
            else:
                return value
        except ValueError:
            print(f"Invalid input. Please enter a valid {number_type.__name__}.")


def ui_add_product(inventory):
    print("\nAdd New Product")

    # Keep asking until we get a non-empty, unused ID or the user quits
    while True:
        product_id = input("Product ID (or 'q' to go back): ").strip()

        if product_id.lower() == "q":
            return  # back to the menu
        elif product_id == "":
            print("\nProduct ID cannot be empty.\n")
        elif search_product(inventory, product_id) is not None:
            print("\nProduct ID already exists.\n")
        else:
            break

    name = input("Product Name: ").strip()
    price = read_number("Price: ", float)
    stock = read_number("Stock Quantity: ", int)

    if add_product(inventory, product_id, name, price, stock):
        print("\nProduct added successfully!")
    else:
        print("\nFailed to add product.")


def ui_update_stock(inventory):
    print("\nUpdate Stock")

    # Keep asking until a valid ID is entered or the user quits
    while True:
        product_id = input("Enter Product ID (or 'q' to go back): ").strip()

        if product_id.lower() == "q":
            return  # back to the menu

        product = search_product(inventory, product_id)
        if product is None:
            print("\nProduct not found.\n")
        else:
            break

    print("\nProduct Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")

    new_stock = read_number("\nNew Stock Quantity: ", int)
    if update_stock(inventory, product_id, new_stock):
        print("\nStock updated successfully!")
    else:
        print("\nStock update failed.")


def ui_search_product(inventory):
    print("\nSearch Product")

    # Keep asking until a valid ID is entered or the user quits
    while True:
        product_id = input("Enter Product ID (or 'q' to go back): ").strip()

        if product_id.lower() == "q":
            return  # back to the menu

        product = search_product(inventory, product_id)
        if product is None:
            print("\nProduct not found.\n")
        else:
            break

    print("\nProduct Found")
    print("-" * 48)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print("-" * 48)


# ---------------------------------------------------------------
# Manage UI Menu
# ---------------------------------------------------------------
def main():
    """
    Main function to run inventory manager.
    """
    # local variables
    inventory = []
    exit_program = False

    print("=" * 44)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 44)

    inventory, status = load_inventory()
    if status == "loaded":
        print(f"\n{INVENTORY_FILE} found.")
        print("Inventory loaded successfully.")
    elif status == "not_found":
        print(f"\n{INVENTORY_FILE} not found. Starting with empty inventory.")
    else:
        print(f"\nError reading {INVENTORY_FILE}. Starting with empty inventory.")

    print_menu()
    while not exit_program:
        option = input("\nEnter option: ").strip()

        if option == "1":
            display_all(inventory)
        elif option == "2":
            ui_add_product(inventory)
        elif option == "3":
            ui_update_stock(inventory)
        elif option == "4":
            ui_search_product(inventory)
        elif option == "5":
            print("\nSaving inventory...")
            if save_inventory(inventory):
                print(f"Inventory saved successfully to {INVENTORY_FILE}.")
            else:
                print("Failed to save inventory.")
        elif option == "6":
            print("\nSaving inventory before exit...")
            if save_inventory(inventory):
                print("Inventory saved successfully.")
            else:
                print("Failed to save inventory.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            exit_program = True
        else:
            print("\nInvalid option. Please enter 1-6.")


# __name__ (Program Entry Point)
if __name__ == "__main__":
    main()