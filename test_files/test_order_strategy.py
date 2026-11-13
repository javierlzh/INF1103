import ast
import inspect
import textwrap
import unittest
from unittest.mock import Mock

from discount_strategy import DiscountStrategy
from order import Order
from product_factory import ProductFactory
from supplier import Supplier


class OrderStrategyTests(unittest.TestCase):
    def test_total_is_calculated_through_the_strategy(self) -> None:
        supplier = Supplier("S1", "Supplier", "s@example.com")
        product = ProductFactory.create("physical", "P1", "Book", 10.0, 5, supplier, weight=0.5)
        strategy = Mock(spec=DiscountStrategy)
        strategy.apply.return_value = 23.0
        order = Order("O1", strategy)
        order.add_order_line(product, 3)
        self.assertEqual(order.calculate_total(), 23.0)
        strategy.apply.assert_called_once_with(30.0)

    def test_calculate_total_has_no_discount_selection_branches(self) -> None:
        source = textwrap.dedent(inspect.getsource(Order.calculate_total))
        nodes = ast.walk(ast.parse(source))
        self.assertFalse(any(isinstance(node, (ast.If, ast.IfExp, ast.Match)) for node in nodes))


if __name__ == "__main__":
    unittest.main(verbosity=2)
