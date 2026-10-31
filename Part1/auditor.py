inventory = 0 
failed_entries = 0

while inventory < 500:
    stock_quantity = input("Enter stock quantity: ")
    if stock_quantity == 'quit':
        break
    if not stock_quantity.isdigit():
            print("Invalid input. Please enter a valid number.")
            failed_entries += 1
            continue
    quantity = int(stock_quantity)
    if quantity < 0:
            print("Invalid input. Quantity cannot be negative.")
            failed_entries += 1
            continue
    inventory += quantity
    if inventory > 500:
            print("Inventory limit exceeded. Current inventory: ", inventory)
            break
print ("Total units processed: ", inventory)
print ("Number of Failed/Rejected Entries: ", failed_entries)


