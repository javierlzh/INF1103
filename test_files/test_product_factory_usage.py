import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import persistence
from inventory import Inventory
from test_files.csv_test_helper import load_products
from product_factory import ProductFactory
from supplier import Supplier
from main import Main


class ProductFactoryUsageTests(unittest.TestCase):
    def test_ui_calls_factory_for_each_supported_type(self) -> None:
        for kind, extra in [("physical", "0.5"), ("digital", "2.0"), ("subscription", "Monthly")]:
            with self.subTest(kind=kind):
                inventory = Inventory()
                answers = ["2", kind, "P1", "Item", "10", "2", "S1", "Supplier", "s@example.com", extra, "6"]
                with patch("builtins.input", side_effect=answers), redirect_stdout(io.StringIO()):
                    method = "create_subscription" if kind == "subscription" else "create"
                    with patch.object(ProductFactory, method, wraps=getattr(ProductFactory, method)) as create:
                        with patch("file_handling.persistence.load_inventory", return_value=(inventory, "loaded")):
                            with patch("file_handling.persistence.save_inventory", return_value=True):
                                Main().run()
                        create.assert_called_once()
                        if kind != "subscription":
                            self.assertEqual(create.call_args.args[0], kind)
                self.assertIsNotNone(inventory.find_product("P1"))

    def test_csv_loader_calls_factory(self) -> None:
        supplier = Supplier("S1", "Supplier", "s@example.com")
        with TemporaryDirectory() as folder:
            path = Path(folder) / "products.csv"
            path.write_text("product_type,product_id,name,price,stock_quantity\nphysical,P1,Book,10,2\n", encoding="utf-8")
            inventory = Inventory()
            with patch.object(ProductFactory, "create", wraps=ProductFactory.create) as create:
                with redirect_stdout(io.StringIO()):
                    load_products(str(path), inventory, supplier)
                create.assert_called_once()
            self.assertIs(inventory.find_product("P1").get_supplier(), supplier)

    def test_json_loader_calls_factory_and_reuses_supplier(self) -> None:
        supplier = Supplier("S1", "Supplier", "s@example.com")
        products = [
            ProductFactory.create('physical', 'P1', 'Book', 10.0, 2, 0.5, supplier),
            ProductFactory.create('digital', 'D1', 'Ebook', 5.0, 2, 2.0, supplier),
            ProductFactory.create_subscription('S1', 'Plan', 8.0, 2, 'Monthly', supplier),
        ]
        with TemporaryDirectory() as folder:
            path = Path(folder) / "inventory.json"
            path.write_text(json.dumps([product.to_dict() for product in products]), encoding="utf-8")
            with patch.object(persistence, "INVENTORY_FILE", str(path)):
                with patch.object(ProductFactory, "create", wraps=ProductFactory.create) as create:
                    with patch.object(ProductFactory, "create_subscription", wraps=ProductFactory.create_subscription) as subscription:
                        inventory, status = persistence.load_inventory()
                        self.assertEqual(create.call_count, 2)
                        subscription.assert_called_once()
            self.assertEqual(status, "loaded")
            self.assertEqual(inventory.to_list(), [product.to_dict() for product in products])
            loaded = inventory.get_all_products()
            self.assertTrue(all(product.get_supplier() is loaded[0].get_supplier() for product in loaded))


if __name__ == "__main__":
    unittest.main(verbosity=2)
