from product import Product
from product_factory import ProductFactory
from supplier import Supplier
from inventory import Inventory


def main() -> None:
    supplier = Supplier(
        "S001", "ABC Supplies", "abc@example.com"
    )

    products: list[Product] = [
        ProductFactory.create('physical', 'P001', 'Book', 10.0, 5, 0.5, supplier),
        ProductFactory.create('digital', 'D001', 'Ebook', 5.0, 10, 2.0, supplier),
    ]

    for product in products:
        Inventory.show_product_details(product)

        assert product.update_stock(20) is None
        assert product.get_stock() == 20

        print(f"Updated stock: {product.get_stock()}\n")

    print("LSP demonstration passed for both product types.")


if __name__ == "__main__":
    main()
