import unittest

from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from physical_product import PhysicalProduct
from supplier import Supplier


class ObjectRelationshipTests(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier: Supplier = Supplier("S001", "ABC Supplies", "abc@example.com")
        self.physical: PhysicalProduct = PhysicalProduct(
            "P001", "Book", 10.0, 5, 0.5, self.supplier
        )
        self.digital: DigitalProduct = DigitalProduct(
            "D001", "Ebook", 4.0, 10, 2.0, self.supplier
        )

    def test_association_supplier_and_products_are_independent(self) -> None:
        # Section 2.2: both products reference the independently created supplier.
        self.assertIs(self.physical.get_supplier(), self.supplier)
        self.assertIs(self.digital.get_supplier(), self.supplier)
        self.assertIsNot(self.physical, self.supplier)

        # Prediction: deleting the supplier variable leaves the references intact.
        del self.supplier
        self.assertIs(self.physical.get_supplier(), self.digital.get_supplier())
        self.assertEqual(self.physical.get_supplier().get_name(), "ABC Supplies")
        self.assertEqual(self.digital.get_supplier().get_contact_email(), "abc@example.com")
        self.physical.get_supplier().display_information()
        self.digital.get_supplier().display_information()

        supplier = self.physical.get_supplier()
        del self.physical
        self.assertEqual(supplier.get_supplier_id(), "S001")

    def test_aggregation_product_transfers_between_inventories(self) -> None:
        # Section 3.2: the product exists before either inventory is created.
        inventory_a = Inventory()
        inventory_b = Inventory()
        inventory_a.add_product(self.physical)
        self.assertIs(inventory_a.find_product("P001"), self.physical)

        # Prediction: removing the reference does not destroy our product.
        inventory_a.remove_product("P001")
        self.assertIsNone(inventory_a.find_product("P001"))
        self.assertEqual(self.physical.get_name(), "Book")
        inventory_b.add_product(self.physical)
        self.assertIs(inventory_b.find_product("P001"), self.physical)
        print("Aggregation: the same Product remains usable in Inventory B.")

    def test_composition_order_manages_lines_not_products(self) -> None:
        # Section 4.3: create the lines through Order, using two products.
        order_a = Order("O001")
        order_a.add_order_line(self.physical, 2)
        order_a.add_order_line(self.digital, 3)
        self.assertEqual(order_a.get_order_lines(), [
            (self.physical, 2, 20.0), (self.digital, 3, 12.0)
        ])
        self.assertAlmostEqual(order_a.calculate_total(), 32.0)
        for product, quantity, subtotal in order_a.get_order_lines():
            print(f"{product.get_name()} x {quantity}: ${subtotal:.2f}")
        print(f"Order total: ${order_a.calculate_total():.2f}")

        # Prediction: two orders create distinct lines for the same product.
        order_b = Order("O002")
        order_b.add_order_line(self.physical, 1)
        # Private storage is inspected only to compare actual line identities.
        self.assertIsNot(order_a._Order__order_lines[0], order_b._Order__order_lines[0])
        self.assertIs(order_a.get_order_lines()[0][0], order_b.get_order_lines()[0][0])

        order_a.remove_order_line(0)
        self.assertEqual(order_a.get_order_lines(), [(self.digital, 3, 12.0)])
        self.assertAlmostEqual(order_a.calculate_total(), 12.0)
        self.assertEqual(self.physical.get_name(), "Book")
        del order_a
        self.assertEqual(self.digital.get_name(), "Ebook")


if __name__ == "__main__":
    unittest.main(verbosity=2)
