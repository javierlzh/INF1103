import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import main
from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier


class LoadProductsMenuTests(unittest.TestCase):
    def test_menu_loads_csv_and_reuses_supplier(self) -> None:
        inventory = Inventory()
        supplier = Supplier("S1", "Supplier", "supplier@example.com")
        inventory.add_product(ProductFactory.create('physical', 'P0', 'Existing', 10.0, 1, 0.0, supplier))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "products.csv"
            path.write_text(
                "product_type,product_id,name,price,stock_quantity\n"
                "digital,D1,Editor,20,3\n"
                "service,S2,Invalid,10,1\n"
                "physical,P1,Lamp,25,2\n", encoding="utf-8"
            )
            with patch("main.FileHandling.load_inventory", return_value=(inventory, "loaded")):
                with patch("main.FileHandling.save_inventory", return_value=True):
                    with patch("builtins.input", side_effect=["8", str(path), "S1", "6"]):
                        with redirect_stdout(io.StringIO()) as output:
                            main.Main().run()
        self.assertIn("2 products loaded.", output.getvalue())
        self.assertIn("Skipping row 3", output.getvalue())
        self.assertIn("Load attempt finished.", output.getvalue())
        for product_id in ("D1", "P1"):
            product = inventory.find_product(product_id)
            self.assertIsNotNone(product)
            assert product is not None
            self.assertIs(product.get_supplier(), supplier)

    def test_missing_csv_returns_to_menu(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            missing = str(Path(directory) / "missing.csv")
            with patch("main.FileHandling.load_inventory", return_value=(Inventory(), "not_found")):
                with patch("main.FileHandling.save_inventory", return_value=True):
                    with patch("builtins.input", side_effect=["8", missing, "S1", "Supplier", "s@example.com", "6"]):
                        with redirect_stdout(io.StringIO()) as output:
                            main.Main().run()
        self.assertIn("Products file not found", output.getvalue())
        self.assertIn("Load attempt finished.", output.getvalue())
        self.assertIn("Terminated.", output.getvalue())


if __name__ == "__main__":
    unittest.main()
