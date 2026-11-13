import unittest

from order import Order
from order_line import OrderLine
from product_factory import ProductFactory
from supplier import Supplier


class InvalidValuesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier: Supplier = Supplier("S1", "Supplier", "s@example.com")

    def test_factory_rejects_invalid_price_and_stock(self) -> None:
        for kind in ("physical", "digital"):
            for price, stock in [(0.0, 0), (-1.0, 0), (float("nan"), 0), (float("inf"), 0), (10.0, -1), (10.0, 1.5)]:
                with self.subTest(kind=kind, price=price, stock=stock):
                    with self.assertRaises(ValueError):
                        ProductFactory.create(kind, "P1", "Item", price, stock, self.supplier, weight=0.5, download_size=2.0)

    def test_stock_updates_preserve_last_valid_value(self) -> None:
        for kind in ("physical", "digital"):
            product = ProductFactory.create(kind, "P1", "Item", 10.0, 5, self.supplier, weight=0.5, download_size=2.0)
            for invalid in (-1, 1.5):
                with self.subTest(kind=kind, stock=invalid):
                    with self.assertRaises(ValueError):
                        product.update_stock(invalid)
                    self.assertEqual(product.get_stock(), 5)
            product.update_stock(0)
            self.assertEqual(product.get_stock(), 0)

    def test_invalid_line_does_not_change_order(self) -> None:
        product = ProductFactory.create("physical", "P1", "Book", 10.0, 0, self.supplier, weight=0.5)
        order = Order("O1")
        order.add_order_line(product, 1)
        for quantity in (0, -1, 1.5):
            with self.subTest(quantity=quantity):
                with self.assertRaises(ValueError):
                    OrderLine(product, quantity)
                with self.assertRaises(ValueError):
                    order.add_order_line(product, quantity)
                self.assertEqual(order.get_order_lines(), [(product, 1, 10.0)])


if __name__ == "__main__":
    unittest.main(verbosity=2)
