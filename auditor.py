inventory = 0 
failed_entries = 0

while inventory < 500:
    stock_quantity = input("Enter stock quantity: ")
    if stock_quantity == 'quit':
        break
    quantity = int(stock_quantity)
