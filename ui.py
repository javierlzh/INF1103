import math
from typing import overload
from product import Product
from inventory import Inventory
from supplier import Supplier

def print_menu() -> None:
    """Display the main application menu."""
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


@overload
def read_number(prompt: str, number_type: type[int]) -> int: ...


@overload
def read_number(prompt: str, number_type: type[float] = float) -> float: ...


def read_number(prompt: str, number_type: type[int] | type[float] = float) -> int | float:
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


def ui_add_product(inventory: Inventory) -> None:
    """Interactive UI flow to add any registered product to the inventory polymorphically."""
    print("\nAdd New Product")

    # Dynamically fetch available product types from our registry (e.g., physical, digital, subscription)
    valid_types = list(Product._registry.keys())
    type_prompt = f"Product Type ({'/'.join(valid_types)}) (or 'q' to go back): "

    while True:
        product_type = input(type_prompt).strip().lower()
        if product_type == "q":
            return
        elif product_type in valid_types:
            break
        print(f"\nInvalid product type. Please enter one of: {', '.join(valid_types)}.\n")

    while True:
        product_id = input("Product ID (or 'q' to go back): ").strip()
        if product_id.lower() == 'q':
            return
        elif inventory.find_product(product_id) is not None:
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

    supplier_id = input("Supplier ID: ").strip()
    supplier: Supplier | None = None
    for existing_product in inventory.get_all_products():
        existing_supplier = existing_product.get_supplier()
        if existing_supplier.get_supplier_id() == supplier_id:
            supplier = existing_supplier
            break
    if supplier is None:
        supplier_name = input("Supplier name: ").strip()
        supplier_email = input("Supplier contact email: ").strip()
        if not all((supplier_id, supplier_name, supplier_email)):
            print("Supplier details cannot be empty.")
            return
        supplier = Supplier(supplier_id, supplier_name, supplier_email)

    product_class = Product._registry[product_type]
    product = product_class.get_ui_inputs(product_id, name, price, stock, read_number, supplier)

    try:
        inventory.add_product(product)
    except ValueError as error:
        print(f"\nFailed to add product: {error}")
    else:
        print("\nProduct added successfully!")


def ui_update_stock(inventory: Inventory) -> None:
    """Interactive UI flow to update product stock."""
    print("\nUpdate Stock")
    while True:
        product_id = input("Enter Product ID (or 'q' to go back): ").strip()
        if product_id.lower() == "q":
            return
        product = inventory.find_product(product_id)
        if product is not None:
            break
        print("\nProduct not found.\n")

    print(f"\nProduct Found: {product.get_name()} (Current Stock: {product.get_stock()})")
    product.get_supplier().display_information()
    new_stock = read_number("\nNew Stock Quantity: ", int)
    try:
        inventory.update_stock(product_id, int(new_stock))
    except (KeyError, ValueError) as error:
        print(f"\nStock update failed: {error}")
    else:
        print("\nStock updated successfully!")


def ui_search_product(inventory: Inventory) -> None:
    """Interactive UI flow to search and display a product."""
    print("\nSearch Product")
    while True:
        product_id = input("Enter Product ID (or 'q' to go back): ").strip()
        if product_id.lower() == "q":
            return
        product = inventory.find_product(product_id)
        if product is not None:
            break
        print("\nProduct not found.\n")

    print("\n" + "-" * 48)
    print(product.display_information())
    print("-" * 48)
