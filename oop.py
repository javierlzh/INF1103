"""
INF1103 Week 8 - Inventory Manager (OOP)
"""

import json
import math

INVENTORY_FILE = "inventory.json"

# ---------------------------------------------------------------
# Product class: stores and manages one product
# ---------------------------------------------------------------
class Product:
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock

    def display_information(self):
        return f"ID: {self.product_id} | Name: {self.name} | Price: ${self.price:.2f} | Stock: {self.stock}"

    def to_dict(self):  # Convert to a dict so json can save it.
        return {
            "id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock
        }

    def update_stock(self, new_stock):
        if new_stock < 0:
            return False
        self.__stock = new_stock
        return True

# ---------------------------------------------------------------
# Inventory class: manages a collection of Product objects 
# ---------------------------------------------------------------
class Inventory:
    """Represents one product and manages its own state."""
    def __init__(self):
        self.__inventory = []

    def to_list(self):
        return [product.to_dict() for product in self.__inventory]

    def display_all(self):
        print("\nCurrent Inventory")
        print("-" * 48)
        if len(self.__inventory) == 0:
            print("No products in inventory.")
        for p in self.__inventory:
            print(p.display_information())
        print("-" * 48)

    def search_product(self, product_id):
        for product in self.__inventory:
            if product.product_id == product_id:
                return product
        return None
    
    def add_product(self, product):
        """Add a Product. Returns False if its ID already exists."""
        if self.search_product(product.product_id) is not None:
            return False
        self.__inventory.append(product)
        return True

    def update_stock(self, product_id, new_stock):
        """Set stock to new_stock. Returns False if new_stock is negative."""
        product = self.search_product(product_id)
        if product is None:
            return False
        return product.update_stock(new_stock)

def save_inventory(inventory):
    try:
        with open(INVENTORY_FILE, "w") as file:
            json.dump(inventory.to_list(), file, indent=4)
        return True
    except OSError:
        return False

def is_valid_item(item):
    if not isinstance(item, dict):
        return False
    for key in ("id", "name", "price", "stock"):
        if key not in item:
            return False
    return (isinstance(item["id"], str) and item["id"].strip() != ""
            and isinstance(item["name"], str) 
            and isinstance(item["price"], (int, float)) and item["price"] >= 0
            and isinstance(item["stock"], int) and item["stock"] >= 0)

def load_inventory():
    inventory = Inventory()
    status = "loaded"
    try:
        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)                    # a list of dicts
        if not isinstance(data, list):
            raise ValueError("Top level of the file must be a list.")
        for item in data:
            if not is_valid_item(item):
                raise ValueError("Invalid product entry.")
            product = Product(item["id"], item["name"], item["price"], item["stock"])
            if not inventory.add_product(product):
                status = "duplicates"
    except FileNotFoundError:
        status = "not_found"
    except (OSError, ValueError):
        inventory = Inventory()
        status = "error"
    return inventory, status

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
            if not math.isfinite(value) or value < 0:
                print("Value cannot be negative or infinite. Try again.")
            else:
                return value
        except ValueError:
            print(f"Invalid input. Please enter a valid {number_type.__name__}.")

def ui_add_product(inventory):
    print("\nAdd New Product")
    while True:
        product_id = input("Product ID (or 'q' to go back): ").strip()

        if product_id.lower() == "q":
            return  # back to the menu
        elif product_id == "":
            print("\nProduct ID cannot be empty.\n")
        elif inventory.search_product(product_id) is not None:
            print("\nProduct ID already exists.\n")
        else:
            break

    name = input("Product Name: ").strip()
    price = read_number("Price: ", float)
    stock = read_number("Stock Quantity: ", int)

    if inventory.add_product(Product(product_id, name, price, stock)):
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

        product = inventory.search_product(product_id)
        if product is None:
            print("\nProduct not found.\n")
        else:
            break

    print("\nProduct Found:")
    print(f"Name: {product.name}")
    print(f"Current Stock: {product.stock}")

    new_stock = read_number("\nNew Stock Quantity: ", int)
    if inventory.update_stock(product_id, new_stock):
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

        product = inventory.search_product(product_id)
        if product is None:
            print("\nProduct not found.\n")
        else:
            break

    print("\nProduct Found")
    print("-" * 48)
    print(f"ID: {product.product_id}")
    print(f"Name: {product.name}")
    print(f"Price: ${product.price:.2f}")
    print(f"Stock: {product.stock}")
    print("-" * 48)


def main():
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
    elif status == "duplicates":
        print(f"\n{INVENTORY_FILE} found.")
        print("Inventory loaded, but duplicate product IDs were skipped.")
    else:
        print(f"\nError reading {INVENTORY_FILE}. Starting with empty inventory.")
    
    print_menu()
    while not exit_program:
        option = input("\nEnter option: ").strip()
    
        if option == "1":
            inventory.display_all()
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

if __name__ == "__main__":
    main()