inventory = 0 
failed_entries = 0

while inventory < 500:
    stock_quantity = input("Enter stock quantity: ")
    if stock_quantity == 'quit':
        break
    quantity = int(stock_quantity)
    if not stock_quantity.isdigit():
            print("Invalid input. Please enter a valid number.")
            failed_entries += 1
            continue
    if quantity < 0:
            print("Invalid input. Quantity cannot be negative.")
            failed_entries += 1
            continue

