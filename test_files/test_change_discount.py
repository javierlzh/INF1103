import unittest

from bulk_discount import BulkDiscount
from no_discount import NoDiscount
from order import Order
from percentage_discount import PercentageDiscount
from product_factory import ProductFactory
from student_disocunt import StudentDiscount
from supplier import Supplier


class ChangeDiscountTests(unittest.TestCase):
    def test_existing_order_can_change_strategy(self) -> None:
        supplier = Supplier("S1", "Supplier", "s@example.com")
        product = ProductFactory.create('physical', 'P1', 'Book', 20.0, 10, 0.5, supplier)
        order = Order("O1")
        order.add_order_line(product, 5)
        original_lines = order.get_order_lines()
        self.assertEqual(order.calculate_total(), 100.0)
        for strategy, expected in [
            (PercentageDiscount(20), 80.0),
            (StudentDiscount(), 95.0),
            (BulkDiscount(100, 15), 85.0),
            (BulkDiscount(100.01, 15), 100.0),
            (NoDiscount(), 100.0),
        ]:
            with self.subTest(strategy=type(strategy).__name__, expected=expected):
                order.set_discount(strategy)
                self.assertAlmostEqual(order.calculate_total(), expected)
                self.assertEqual(order.get_order_lines(), original_lines)

    def test_bulk_discount_uses_inclusive_order_total_threshold(self) -> None:
        strategy = BulkDiscount(200, 20)
        self.assertEqual(strategy.apply(199.99), 199.99)
        self.assertEqual(strategy.apply(200), 180)
        self.assertEqual(strategy.apply(250), 230)

    def test_lab_example_switches_from_bulk_to_percentage(self) -> None:
        supplier = Supplier("S1", "Supplier", "s@example.com")
        product = ProductFactory.create('physical', 'P1', 'Book', 50.0, 10, 0.5, supplier)
        order = Order("O1", BulkDiscount(200, 20))
        order.add_order_line(product, 5)
        self.assertEqual(order.calculate_total(), 230.0)
        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225.0)

    def test_student_discount_takes_five_percent(self) -> None:
        self.assertEqual(StudentDiscount().apply(250), 237.5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
