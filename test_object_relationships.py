import unittest

from inventory import Inventory
from order import Order
from product import Product
from product_factory import ProductFactory
from supplier import Supplier


class ObjectRelationshipTests(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier: Supplier = Supplier(
            "S001", "ABC Supplies", "abc@example.com"
        )

        self.physical: Product = ProductFactory.create_product(
            "physical", "P001", "Book", 10.0, 5, self.supplier,
            weight=0.5,
        )

        self.digital: Product = ProductFactory.create_product(
            "digital", "D001", "Ebook", 4.0, 10, self.supplier,
            download_size=2.0,
        )