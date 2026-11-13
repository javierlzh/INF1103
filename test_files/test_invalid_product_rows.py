import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory

from inventory import Inventory
from load_products import load_products
from supplier import Supplier


class InvalidProductRowsTests(unittest.TestCase):
    def test_sample_rows_load_three_products_in_order(self) -> None:
        csv_text = (
            "product_type,product_id,name,price,stock_quantity\n"
            "physical,P001,Desk Lamp,25.00,10\n"
            "digital,D001,Photo Editor,49.90,100\n"
            "service,S001,Installation,30.00,5\n"
            "physical,P002,Office Chair,abc,3\n"
            "physical,P003,Monitor Stand,39.50,7\n"
        )
        supplier = Supplier("S1", "Supplier", "s@example.com")
        inventory = Inventory()
        with TemporaryDirectory() as folder:
            path = Path(folder) / "products.csv"
            path.write_text(csv_text, encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                load_products(str(path), inventory, supplier)
        self.assertEqual([product.get_product_id() for product in inventory.get_all_products()], ["P001", "D001", "P003"])
        self.assertEqual(output.getvalue().splitlines(), [
            "Skipping row 4: Unknown product type: service",
            "Skipping row 5: could not convert string to float: 'abc'",
            "3 products loaded.",
            "Load attempt finished.",
        ])


if __name__ == "__main__":
    unittest.main(verbosity=2)
