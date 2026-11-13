"""Order creation and discount selection through the main application menu."""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import main
from inventory import Inventory
from order import Order
from product_factory import ProductFactory
from supplier import Supplier
from ui import ui_create_order, ui_order_discount


class OrderMenuTests(unittest.TestCase):
    def setUp(self) -> None:
        supplier = Supplier("S1", "Supplier", "s@example.com")
        self.inventory: Inventory = Inventory()
        self.inventory.add_product(ProductFactory.create('physical', 'P1', 'Book', 20.0, 10, 0.5, supplier))

    def test_option_seven_creates_order_and_switches_discounts(self) -> None:
        answers = ["7", "O1", "P1", "5", "done", "1", "20", "2", "3", "100", "15", "", "q", "6"]
        output = io.StringIO()
        with patch("main.FileHandling.load_inventory", return_value=(self.inventory, "loaded")):
            with patch("main.FileHandling.save_inventory", return_value=True), patch("builtins.input", side_effect=answers):
                with redirect_stdout(output):
                    main.Main().run()
        for expected in ("Order total: $80.00", "Order total: $95.00", "Order total: $85.00", "Order total: $100.00", "Terminated."):
            self.assertIn(expected, output.getvalue())

    def test_invalid_order_inputs_are_retried(self) -> None:
        answers = ["", "O1", "done", "missing", "P1", "abc", "0", "2", "done", "invalid", "1", "101", "0", "q"]
        output = io.StringIO()
        with patch("builtins.input", side_effect=answers), redirect_stdout(output):
            ui_create_order(self.inventory)
        for expected in ("Order ID cannot be empty", "Add at least one product", "Product not found", "Quantity must be greater than zero", "between 0 and 100", "Order total: $40.00"):
            self.assertIn(expected, output.getvalue())

    def test_empty_inventory_and_cancel_return_to_caller(self) -> None:
        with patch("builtins.input") as prompt, redirect_stdout(io.StringIO()):
            ui_create_order(Inventory())
            prompt.assert_not_called()
        for answers in (["q"], ["O1", "q"]):
            with patch("builtins.input", side_effect=answers), redirect_stdout(io.StringIO()):
                ui_create_order(self.inventory)

    def test_invalid_bulk_discount_preserves_current_strategy(self) -> None:
        order = Order("O1")
        order.add_order_line(self.inventory.get_all_products()[0], 1)
        with patch("builtins.input", side_effect=["3", "1", "25", "q"]):
            with redirect_stdout(io.StringIO()) as output:
                ui_order_discount(order)
        self.assertIn("Discount amount cannot exceed the total", output.getvalue())
        self.assertEqual(order.calculate_total(), 20.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
