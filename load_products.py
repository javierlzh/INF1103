import csv

from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Report and skip invalid rows, and always report when loading finishes."""
    try:
        file = open(path, newline="", encoding="utf-8-sig")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header, including when the file is empty.
            for row_number, row in enumerate(reader, start=2):
                try:
                    if len(row) != 5:
                        raise ValueError("Each row must contain five columns.")
                    product_type, product_id, name, price, stock_quantity = (
                        value.strip() for value in row
                    )
                    product = ProductFactory.create(
                        product_type,
                        product_id,
                        name,
                        float(price),
                        int(stock_quantity),
                        supplier,
                        weight=0.0,
                        download_size=0.0,
                    )
                    inventory.add_product(product)
                except ValueError as error:
                    print(f"Skipping row {row_number}: {error}")
                else:
                    loaded += 1
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


if __name__ == "__main__":
    inventory = Inventory()
    supplier = Supplier("S001", "ABC Supplies", "abc@example.com")
    load_products("products.csv", inventory, supplier)
