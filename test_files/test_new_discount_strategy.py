import unittest

from order import Order
from product_factory import ProductFactory
from supplier import Supplier
from test_files.half_price_discount import HalfPriceDiscount


class NewDiscountStrategyTests(unittest.TestCase):
    def test_new_strategy_works_without_changing_order(self) -> None:
        supplier = Supplier("S1", "Supplier", "s@example.com")
        product = ProductFactory.create("digital", "D1", "Ebook", 20.0, 5, supplier, download_size=2.0)
        order = Order("O1", HalfPriceDiscount())
        order.add_order_line(product, 3)
        self.assertEqual(order.calculate_total(), 30.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
