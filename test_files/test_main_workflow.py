import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from inventory import Inventory
from main import Main


class MainWorkflowTests(unittest.TestCase):
    def test_add_display_update_find_and_save(self) -> None:
        inventory = Inventory()
        answers = [
            "2", "physical", "P1", "Lamp", "25", "2",
            "S1", "Supplier", "s@example.com", "1.5",
            "1", "3", "P1", "4", "4", "P1", "5", "6",
        ]
        with patch("file_handling.persistence.load_inventory", return_value=(inventory, "loaded")):
            with patch("file_handling.persistence.save_inventory", return_value=True) as save:
                with patch("builtins.input", side_effect=answers), redirect_stdout(io.StringIO()) as output:
                    Main().run()
        product = inventory.find_product("P1")
        self.assertIsNotNone(product)
        assert product is not None
        self.assertEqual(product.get_stock(), 4)
        self.assertIn("Shipping required", output.getvalue())
        self.assertIn("Stock updated successfully", output.getvalue())
        self.assertEqual(save.call_count, 2)
        save.assert_called_with(inventory)

    def test_failed_save_keeps_menu_open_until_retry_succeeds(self) -> None:
        with patch("file_handling.persistence.load_inventory", return_value=(Inventory(), "not_found")):
            with patch("file_handling.persistence.save_inventory", side_effect=[False, True]) as save:
                with patch("builtins.input", side_effect=["6", "6"]), redirect_stdout(io.StringIO()) as output:
                    Main().run()
        self.assertEqual(save.call_count, 2)
        self.assertIn("Please try saving again before exiting", output.getvalue())
        self.assertIn("Terminated", output.getvalue())

    def test_failed_load_can_exit_without_saving(self) -> None:
        with patch("file_handling.persistence.load_inventory", return_value=(Inventory(), "error")):
            with patch("file_handling.persistence.save_inventory") as save:
                with patch("builtins.input", side_effect=["q"]), redirect_stdout(io.StringIO()) as output:
                    Main().run()
        save.assert_not_called()
        self.assertIn("inventory file was preserved", output.getvalue())


if __name__ == "__main__":
    unittest.main()
