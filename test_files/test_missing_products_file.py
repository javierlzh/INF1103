import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory

from inventory import Inventory
from test_files.csv_test_helper import load_products
from supplier import Supplier


class MissingProductsFileTests(unittest.TestCase):
    def test_missing_file_reports_failure_and_finishes(self) -> None:
        supplier = Supplier("S1", "Supplier", "s@example.com")
        inventory = Inventory()
        with TemporaryDirectory() as folder:
            path = str(Path(folder) / "missing.csv")
            output = io.StringIO()
            with redirect_stdout(output):
                result = load_products(path, inventory, supplier)
            self.assertIsNone(result)
            self.assertEqual(output.getvalue().splitlines(), [
                f"Products file not found: {path}", "Load attempt finished."
            ])
        self.assertEqual(inventory.get_all_products(), ())


if __name__ == "__main__":
    unittest.main(verbosity=2)
