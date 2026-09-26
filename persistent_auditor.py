MAX_CAPACITY = 500
TAX_RATE = 0.1  # Example tax rate of 10%
INVENTORY_FILE = "inventory.txt"

def get_valid_input():
       invalid_count = 0
       while True:
           stock_quantity = input("Enter stock quantity: ")

           if stock_quantity == 'quit':
               return 'quit', invalid_count
           elif stock_quantity == '':
                print("Input cannot be empty. Please enter a valid number.")
                invalid_count += 1
           elif stock_quantity.isdigit():
               return int(stock_quantity), invalid_count
           else:
               print("Invalid input. Please enter a valid number.")
               invalid_count += 1

def process_delivery(current_total, new_value):
        new_total = current_total + new_value
        return new_total

def calculate_tax(amount):
        tax_rate = 0.1  # Example tax rate of 10%
        tax_amount = amount * tax_rate
        return tax_amount

def generate_report(total_units, failed_attempts):
        print("-------------------")
        print("Total units processed: ", total_units)
        print("Number of Failed/Rejected Entries: ", failed_attempts)

def load_inventory():
        try:
            with open(INVENTORY_FILE, 'r') as file:
                lines = file.readlines()
                inventory = int(lines[0].strip())

                if len(lines) > 1 and lines[1].strip() != '':
                    transaction_history = [int(x) for x in lines[1].strip().split(',')]
                else:
                    transaction_history = []

                return inventory, transaction_history
        except FileNotFoundError:
            return 0, []  # If the file doesn't exist, start with 0 inventory and empty transaction history
        except ValueError:
            print("Error: Inventory file is corrupted. Starting with 0 inventory.")
            return 0, []

def save_inventory(inventory, transaction_history):
        with open(INVENTORY_FILE, 'w') as file:
            file.write(str(inventory) + "\n")
            file.write(",".join(str(t) for t in transaction_history))

def main():
        inventory, transaction_history = load_inventory()
        total_units = 0
        failed_entries = 0
        exit_program = False

        while True:
              stock_quantity, invalid_count = get_valid_input()
              failed_entries += invalid_count

              if stock_quantity == 'quit':
                break
              elif inventory + stock_quantity > MAX_CAPACITY:
                    print(f"Delivery rejected: adding {stock_quantity} would exceed max capacity of {MAX_CAPACITY}. Current inventory: {inventory}")
                    failed_entries += 1
              else:
                    inventory = process_delivery(inventory, stock_quantity)
                    transaction_history.append(stock_quantity)
                    tax = calculate_tax(stock_quantity)
                    total_units += 1
                    print(f"Delivery of {stock_quantity} accepted. Tax: {tax}. New inventory total: {inventory}")

        save_inventory(inventory, transaction_history)
        generate_report(total_units, failed_entries)
        print("Final inventory count: ", inventory)
        print("--------------------")

if __name__ == "__main__":
        main()
