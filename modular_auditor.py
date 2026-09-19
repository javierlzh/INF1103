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

def main():
        inventory = 0;
        total_units = 0;
        failed_entries = 0;

        while True:
              stock_quantity, invalid_count = get_valid_input()
              failed_entries += invalid_count

              if stock_quantity == 'quit':
                break
              else:
                    inventory = process_delivery(inventory, stock_quantity)
                    tax = calculate_tax(stock_quantity)
                    total_units += 1
                    print(f"Delivery of {stock_quantity} accepted. Tax: {tax}. New inventory total: {inventory}")

        generate_report(total_units, failed_entries)
        print("Final inventory count: ", inventory)
        print("--------------------")

if __name__ == "__main__":
        main()