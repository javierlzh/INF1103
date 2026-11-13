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

        self.physical: Product = ProductFactory.create('physical', 'P001', 'Book', 10.0, 5, 0.5, self.supplier)

        self.digital: Product = ProductFactory.create('digital', 'D001', 'Ebook', 4.0, 10, 2.0, self.supplier)

    def test_association_products_share_an_independent_supplier(self) -> None:
        self.assertIs(self.physical.get_supplier(), self.supplier)
        self.assertIs(self.digital.get_supplier(), self.supplier)
        del self.supplier
        self.assertIs(self.physical.get_supplier(), self.digital.get_supplier())
        self.physical.get_supplier().display_information()
        self.digital.get_supplier().display_information()
        supplier = self.physical.get_supplier()
        del self.physical
        self.assertEqual(supplier.get_name(), "ABC Supplies")

    def test_aggregation_product_transfers_without_being_destroyed(self) -> None:
        inventory_a = Inventory()
        inventory_b = Inventory()
        inventory_a.add_product(self.physical)
        self.assertIs(inventory_a.find_product("P001"), self.physical)
        inventory_a.remove_product("P001")
        self.assertIsNone(inventory_a.find_product("P001"))
        self.assertEqual(self.physical.get_name(), "Book")
        inventory_b.add_product(self.physical)
        self.assertIs(inventory_b.find_product("P001"), self.physical)

    def test_composition_orders_manage_distinct_lines_and_share_products(self) -> None:
        order_a = Order("O001")
        order_a.add_order_line(self.physical, 2)
        order_a.add_order_line(self.digital, 3)
        self.assertEqual(order_a.get_order_lines(), (
            (self.physical, 2, 20.0), (self.digital, 3, 12.0)
        ))
        self.assertAlmostEqual(order_a.calculate_total(), 32.0)
        for product, quantity, subtotal in order_a.get_order_lines():
            print(f"{product.get_name()} x {quantity}: ${subtotal:.2f}")
        print(f"Order total: ${order_a.calculate_total():.2f}")

        order_b = Order("O002")
        order_b.add_order_line(self.physical, 1)
        # Inspect private storage only to verify that the actual lines differ.
        self.assertIsNot(order_a._Order__order_lines[0], order_b._Order__order_lines[0])
        self.assertIs(order_a.get_order_lines()[0][0], order_b.get_order_lines()[0][0])
        order_a.remove_order_line(0)
        self.assertAlmostEqual(order_a.calculate_total(), 12.0)
        self.assertEqual(self.physical.get_name(), "Book")
        del order_a
        self.assertEqual(self.digital.get_name(), "Ebook")


if __name__ == "__main__":
    unittest.main(verbosity=2)
