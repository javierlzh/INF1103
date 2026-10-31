# Global Constants
EXIT_SIGNAL = -99
MAX_CAPACITY = 500
TAX_RATE = 0.1  # Example tax rate of 10%
INVENTORY_FILE = "inventory.txt"

# Inventory item structure
ITEM_FIELDS = {
    "id": 0,
    "name": 1,
    "quantity": 2,
    "transaction_history": 3
}

FIELD_SEPARATOR = ","
HISTORY_SEPARATOR = "|"

def load_inventory():
        # Load inventory from a file. Each line in the file represents an item with its details.
        inventory = []
        try:
            with open(INVENTORY_FILE, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line == '':
                        continue
                    parts = line.split(FIELD_SEPARATOR)
                    item_id = int(parts[0].strip())
                    name = parts[1].strip()
                    quantity = int(parts[2].strip())
 
                    if len(parts) > 3 and parts[3].strip() != '':
                        transaction_history = [int(x) for x in parts[3].strip().split(HISTORY_SEPARATOR)]
                    else:
                        transaction_history = []
 
                    inventory.append([item_id, name, quantity, transaction_history])
        except FileNotFoundError:
            pass  # No file yet — start with an empty inventory
        except (ValueError, IndexError):
            print("Warning: inventory.txt is corrupted or malformed. Starting with an empty inventory.")
            inventory = []
 
        return inventory

def save_inventory(inventory):
        # Save the current inventory to a file. Each item is written in a structured format.
        with open(INVENTORY_FILE, 'w') as file:
            for item in inventory:
                history_str = HISTORY_SEPARATOR.join(str(h) for h in item[ITEM_FIELDS["transaction_history"]])
                file.write(f"{item[ITEM_FIELDS['id']]}{FIELD_SEPARATOR}"
                            f"{item[ITEM_FIELDS['name']]}{FIELD_SEPARATOR}"
                            f"{item[ITEM_FIELDS['quantity']]}{FIELD_SEPARATOR}"
                            f"{history_str}\n")

def display_inventory(inventory):
        # Print all items currently in the inventory.
        print("Current Orders:\n")
        for item in inventory:
            print(f"{item[ITEM_FIELDS['id']]}, {item[ITEM_FIELDS['name']]}, {item[ITEM_FIELDS['quantity']]}")
        print()

def find_item(inventory, name):
        # Search for an item in the inventory by its name (case-insensitive). Returns the item if found, else None.
        for item in inventory:
            if item[ITEM_FIELDS["name"]].strip().lower() == name.strip().lower():
                return item
        return None

def find_item_by_id(inventory, item_id):
        # Search for an item in the inventory by its ID. Returns the item if found, else None.
        for item in inventory:
            if item[ITEM_FIELDS["id"]] == item_id:
                return item
        return None

def get_next_id(inventory):
        # Determine the next available ID for a new item. If the inventory is empty, start with 1001.
        if not inventory:
            return 1001
        return max(item[ITEM_FIELDS["id"]] for item in inventory) + 1
 
 
def get_product_name():
        # Prompt the user to enter a product name and return it after stripping whitespace.
        return input("Enter Product Name: ").strip()

def get_valid_input():
        # Prompt the user for a valid stock quantity. Returns the quantity and the count of invalid attempts.
        invalid_count = 0
        while True:
            quantity_str = input("Enter Quantity: ").strip()
 
            if quantity_str == str(EXIT_SIGNAL):
                return EXIT_SIGNAL, invalid_count
            elif quantity_str.isdigit():
                return int(quantity_str), invalid_count
            else:
                print("Invalid quantity. Please enter a whole number.")
                invalid_count += 1

def process_delivery(item, new_quantity):
        # Update the item's quantity and record the transaction in its history.
        item[ITEM_FIELDS["quantity"]] += new_quantity
        item[ITEM_FIELDS["transaction_history"]].append(new_quantity)
 
 
def calculate_tax(amount, tax_rate):
        # Calculate the tax for a given amount based on the specified tax rate.
        return amount * tax_rate

def display_status(item, valid_quantity, tax_amount):
        # Display the current status of the item after processing a delivery.
        print(f"\n{item[ITEM_FIELDS['id']]},{item[ITEM_FIELDS['name']]},{item[ITEM_FIELDS['quantity']]}")
        print(f"Delivery added: {valid_quantity} units. Tax on this delivery: {tax_amount:.2f}.")
        print(f"Order successfully saved to {INVENTORY_FILE}\n")

def generate_report(inventory, failed_entries):
        # Generate a summary report of the inventory and failed entries.
        total_units = sum(item[ITEM_FIELDS["quantity"]] for item in inventory)
        print("-------------------")
        print("Total Items in Inventory: ", len(inventory))
        print("Total Units Across All Items: ", total_units)
        print("Number of Failed/Rejected Entries: ", failed_entries)
        print("-------------------")
 
 
def main():
        # Load the inventory from the file and display it to the user.
        inventory = load_inventory()
        display_inventory(inventory)
        failed_entries = 0
 
        while True:
            product_name = get_product_name()

            if product_name.lower() == 'quit':
                break

            existing_item = find_item(inventory, product_name)
            quantity, invalid_count = get_valid_input()
            failed_entries += invalid_count

            if quantity == EXIT_SIGNAL:
                break

            if existing_item is not None:
                if existing_item[ITEM_FIELDS["quantity"]] + quantity > MAX_CAPACITY:
                    print(f"Delivery rejected: would exceed max capacity of {MAX_CAPACITY} "
                          f"for {existing_item[ITEM_FIELDS['name']]}.\n")
                    failed_entries += 1
                    continue

                tax = calculate_tax(quantity, TAX_RATE)
                process_delivery(existing_item, quantity)
                display_status(existing_item, quantity, tax)
            else:
                if quantity > MAX_CAPACITY:
                    print(f"Delivery rejected: {quantity} exceeds max capacity of {MAX_CAPACITY}.\n")
                    failed_entries += 1
                    continue

                new_id = get_next_id(inventory)
                new_item = [new_id, product_name, 0, []]
                inventory.append(new_item)

                tax = calculate_tax(quantity, TAX_RATE)
                process_delivery(new_item, quantity)
                display_status(new_item, quantity, tax)
 
            save_inventory(inventory)
 
        save_inventory(inventory)
        generate_report(inventory, failed_entries)

if __name__ == "__main__":
        main()