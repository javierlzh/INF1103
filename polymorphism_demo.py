from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier


def main() -> None:
    supplier = Supplier(
        "S001", "ABC Supplies", "abc@example.com"
    )

    products: list[Product] = [
    PhysicalProduct("P001", "Book", 10.0, 5, 0.5, supplier),
    DigitalProduct("D001", "Ebook", 5.0, 10, 2.0, supplier),
]

    for product in products:
        print(product.display_information())
        print(product.get_fulfilment_info())

        assert product.update_stock(20) is True
        assert product.get_stock() == 20

        print(f"Updated stock: {product.get_stock()}\n")

    print("Polymorphism demonstration passed for both product types.")


if __name__ == "__main__":
    main()

