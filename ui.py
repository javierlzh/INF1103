"""
UI module handling console menus, prompts, and user inputs.
"""

import math
from physical_product import PhysicalProduct
from digital_product import DigitalProduct


def print_menu():
    """Display the main application menu."""
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def read_number(prompt, number_type=float):
    """Prompt until a non-negative number of number_type is entered."""
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
    """Interactive UI flow to add a new product to the inventory."""
    print("\nAdd New Product")

    while True:
        product_type = input("Product Type (physical/digital) (or 'q' to go back): ").strip().lower()
        if product_type == "q":
            return
        elif product_type in ("physical", "digital"):
            break
        print("\nInvalid product type. Please enter 'physical' or 'digital'.\n")

    while True:
        product_id = input("Product ID (or 'q' to go back): ").strip()
        if product_id.lower() == 'q':
            return
        elif inventory.search_product(product_id) is not None:
            print("\nProduct ID already exists.\n")
        elif product_id != "":
            break

    while True:
        name = input("Product name (or 'q' to go back): ").strip()
        if name.lower() == 'q':
            return
        elif name != "":
            break

    price = read_number("Price: ", float)
    stock = read_number("Stock Quantity: ", int)

    if product_type == "physical":
        weight = read_number("Weight (kg): ", float)
        product = PhysicalProduct(product_id, name, price, stock, weight)
    else:
        download_size = read_number("Download Size (MB): ", float)
        product = DigitalProduct(product_id, name, price, stock, download_size)

    if inventory.add_product(product):
        print("\nProduct added successfully!")
    else:
        print("\nFailed to add product.")


def ui_update_stock(inventory):
    """Interactive UI flow to update product stock."""
    print("\nUpdate Stock")
    while True:
        product_id = input("Enter Product ID (or 'q' to go back): ").strip()
        if product_id.lower() == "q":
            return
        product = inventory.search_product(product_id)
        if product is not None:
            break
        print("\nProduct not found.\n")

    print(f"\nProduct Found: {product.name} (Current Stock: {product.stock})")
    new_stock = read_number("\nNew Stock Quantity: ", int)
    if inventory.update_stock(product_id, new_stock):
        print("\nStock updated successfully!")
    else:
        print("\nStock update failed.")


def ui_search_product(inventory):
    """Interactive UI flow to search and display a product."""
    print("\nSearch Product")
    while True:
        product_id = input("Enter Product ID (or 'q' to go back): ").strip()
        if product_id.lower() == "q":
            return
        product = inventory.search_product(product_id)
        if product is not None:
            break
        print("\nProduct not found.\n")

    print("\n" + "-" * 48)
    print(product.display_information())
    print("-" * 48)