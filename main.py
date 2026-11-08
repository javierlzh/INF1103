"""
Main application runner module.
"""

from persistence import load_inventory, save_inventory, INVENTORY_FILE
from ui import print_menu, ui_add_product, ui_update_stock, ui_search_product


def main() -> None:
    """Main execution loop for the Inventory Management System."""
    exit_program: bool = False
    print("=" * 44)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 44)
    
    inventory, status = load_inventory()
    if status == "loaded":
        print(f"\n{INVENTORY_FILE} found. Inventory loaded successfully.")
    elif status == "not_found":
        print(f"\n{INVENTORY_FILE} not found. Starting with empty inventory.")
    elif status == "duplicates":
        print(f"\n{INVENTORY_FILE} found. Duplicate product IDs were skipped.")
    else:
        print(f"\nError reading {INVENTORY_FILE}. Starting with empty inventory.")
    
    print_menu()
    while not exit_program:
        option: str = input("\nEnter option: ").strip()
    
        if option == "1":
            inventory.display_all()
        elif option == "2":
            ui_add_product(inventory)
        elif option == "3":
            ui_update_stock(inventory)
        elif option == "4":
            ui_search_product(inventory)
        elif option == "5":
            if save_inventory(inventory):
                print(f"\nInventory saved successfully to {INVENTORY_FILE}.")
            else:
                print("\nFailed to save inventory.")
        elif option == "6":
            save_inventory(inventory)
            print("\nThank you for using Inventory Management System. Terminated.")
            exit_program = True
        else:
            print("\nInvalid option. Please enter 1-6.")


if __name__ == "__main__":
    main()