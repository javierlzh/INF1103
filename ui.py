import math
from typing import overload
from inventory import Inventory
from bulk_discount import BulkDiscount
from discount_strategy import DiscountStrategy
from no_discount import NoDiscount
from order import Order
from percentage_discount import PercentageDiscount
from student_disocunt import StudentDiscount

def print_menu() -> None:
    """Display the main application menu."""
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("7. Create Order and Apply Discount")
    print("8. Load Products from CSV")
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


def ui_order_discount(order: Order) -> None:
    """Choose or change the strategy used to calculate an existing order."""
    lines = order.get_order_lines()
    subtotal = sum(line_subtotal for _, _, line_subtotal in lines)
    while True:
        print("\nDiscount options")
        print("0. No discount (default)")
        print("1. Percentage discount")
        print("2. Student discount (5%)")
        print("3. Bulk discount")
        print("q. Finish order and return to the main menu")
        choice = input("Choose discount (Enter for no discount): ").strip().lower()
        if choice == "q":
            return
        try:
            strategy: DiscountStrategy
            if choice in ("", "0"):
                strategy = NoDiscount()
            elif choice == "1":
                percentage = read_number("Discount percentage (0-100): ", float)
                strategy = PercentageDiscount(percentage)
            elif choice == "2":
                strategy = StudentDiscount()
            elif choice == "3":
                threshold = read_number("Minimum order total for bulk discount ($): ", float)
                amount = read_number("Bulk discount amount ($): ", float)
                strategy = BulkDiscount(threshold, amount)
            else:
                print("Please choose 0, 1, 2, 3 or q.")
                continue
            # Validate before changing the order's current strategy.
            strategy.apply(subtotal)
            order.set_discount(strategy)
            total = order.calculate_total()
        except ValueError as error:
            print(f"Could not apply discount: {error}")
            continue
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Discount: ${subtotal - total:.2f}")
        print(f"Order total: ${total:.2f}")


def ui_create_order(inventory: Inventory) -> None:
    """Build an order from existing products and display discounted totals."""
    if not inventory.get_all_products():
        print("Add products to the inventory before creating an order.")
        return
    while True:
        order_id = input("Order ID (or 'q' to cancel): ").strip()
        if order_id.lower() == "q":
            return
        try:
            order = Order(order_id)
        except ValueError as error:
            print(error)
        else:
            break

    inventory.display_all()
    while True:
        product_id = input("Product ID ('done' to review order, 'q' to cancel): ").strip()
        if product_id.lower() == "q":
            return
        if product_id.lower() == "done":
            if order.get_order_lines():
                break
            print("Add at least one product before reviewing the order.")
            continue
        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found. Please enter an existing product ID.")
            continue
        while True:
            quantity = read_number("Order quantity: ", int)
            try:
                order.add_order_line(product, quantity)
            except ValueError as error:
                print(error)
            else:
                print(f"Added {product.get_name()} x {quantity}.")
                break

    print(f"\nOrder {order.get_order_id()}")
    for product, quantity, subtotal in order.get_order_lines():
        print(f"{product.get_name()} x {quantity}: ${subtotal:.2f}")
    print(f"Order total (no discount): ${order.calculate_total():.2f}")
    ui_order_discount(order)
