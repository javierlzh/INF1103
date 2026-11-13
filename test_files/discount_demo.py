from bulk_discount import BulkDiscount
from discount_strategy import DiscountStrategy
from no_discount import NoDiscount
from order import Order
from percentage_discount import PercentageDiscount
from product_factory import ProductFactory
from student_disocunt import StudentDiscount
from supplier import Supplier


def main() -> None:
    supplier = Supplier("S001", "ABC Supplies", "abc@example.com")
    book = ProductFactory.create('physical', 'P001', 'Book', 25.0, 10, 0.5, supplier)
    ebook = ProductFactory.create('digital', 'D001', 'Ebook', 15.0, 10, 2.0, supplier)
    order = Order("O001")
    order.add_order_line(book, 3)
    order.add_order_line(ebook, 3)

    for product, quantity, subtotal in order.get_order_lines():
        print(f"{product.get_name()} x {quantity}: ${subtotal:.2f}")
    assert order.calculate_total() == 120.0
    print(f"Default NoDiscount: ${order.calculate_total():.2f}")

    strategies: list[tuple[str, DiscountStrategy, float]] = [
        ("20% percentage discount", PercentageDiscount(20), 96.0),
        ("5% student discount", StudentDiscount(), 114.0),
        ("$15 bulk discount at an order total of $100", BulkDiscount(100, 15), 105.0),
        ("Bulk threshold of $200 on a $120 order", BulkDiscount(200, 15), 120.0),
        ("Reset to NoDiscount", NoDiscount(), 120.0),
    ]
    original_lines = order.get_order_lines()
    for label, strategy, expected_total in strategies:
        order.set_discount(strategy)
        total = order.calculate_total()
        assert abs(total - expected_total) < 0.000001
        assert order.get_order_lines() == original_lines
        print(f"{label}: ${total:.2f}")

    print("Discount demonstration passed.")


if __name__ == "__main__":
    main()
