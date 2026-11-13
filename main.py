from persistence import load_inventory, save_inventory, INVENTORY_FILE
from ui import print_menu, ui_add_product, ui_update_stock, ui_search_product, ui_create_order


def main() -> None:
    """Main execution loop for the Inventory Management System."""
    exit_program: bool = False
    print("=" * 44)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 44)
    
    inventory, status = load_inventory()
    while status == "error":
        print(f"\nCould not load {INVENTORY_FILE}.")
        print("Correct the file and retry, or exit to preserve the saved data.")
        recovery = input("Enter 'r' to retry or 'q' to exit: ").strip().lower()
        if recovery == "r":
            inventory, status = load_inventory()
        elif recovery == "q":
            print("Exited. The inventory file was preserved.")
            return
        else:
            print("Please enter 'r' or 'q'.")
    if status == "loaded":
        print(f"\n{INVENTORY_FILE} found. Inventory loaded successfully.")
    elif status == "not_found":
        print(f"\n{INVENTORY_FILE} not found. Starting with empty inventory.")
    elif status == "duplicates":
        print(f"\n{INVENTORY_FILE} found. Duplicate product IDs were skipped.")
    
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
            if save_inventory(inventory):
                print("\nThank you for using Inventory Management System. Terminated.")
                exit_program = True
            else:
                print("\nFailed to save inventory. Please try saving again before exiting.")
        elif option == "7":
            ui_create_order(inventory)
        else:
            print("\nInvalid option. Please enter 1-7.")


if __name__ == "__main__":
    main()
