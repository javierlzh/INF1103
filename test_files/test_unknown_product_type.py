import unittest

from product_factory import ProductFactory
from supplier import Supplier


class UnknownProductTypeTests(unittest.TestCase):
    def test_unknown_type_reports_its_name(self) -> None:
        supplier = Supplier("S1", "Supplier", "s@example.com")
        with self.assertRaisesRegex(ValueError, "Unknown product type: service"):
            ProductFactory.create("service", "X1", "Installation", 30.0, 5, supplier)


if __name__ == "__main__":
    unittest.main(verbosity=2)
