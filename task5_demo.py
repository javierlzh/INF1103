from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier
from inventory import Inventory


def main() -> None:
    supplier = Supplier(
        "S001", "ABC Supplies", "abc@example.com"
    )

    products: list[Product] = [
        PhysicalProduct("P001", "Book", 10.0, 5, 0.5, supplier),
        DigitalProduct("D001", "Ebook", 5.0, 10, 2.0, supplier),
    ]

    for product in products:
        Inventory.show_product_details(product)

        assert product.update_stock(20) is True
        assert product.get_stock() == 20

        print(f"Updated stock: {product.get_stock()}\n")

    print("LSP demonstration passed for both product types.")


if __name__ == "__main__":
    main()

# Raising NotImplementedError in DigitalProduct.update_stock() violates 
# LSP because Product promises stock updates. Here, digital stock 
# represents available licences, so inheriting the parent implementation is
# appropriate. If digital products have no stock, stock management should 
# move to a separate abstraction for products that support it.