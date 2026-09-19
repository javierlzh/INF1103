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