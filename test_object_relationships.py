import gc
import unittest
import weakref
from unittest.mock import patch

from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from order_line import OrderLine
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

    def test_association_products_share_the_existing_supplier(self) -> None:
        self.assertIs(self.physical.get_supplier(), self.supplier)
        self.assertIs(self.digital.get_supplier(), self.supplier)

    def test_association_deleting_supplier_variable_preserves_reference(self) -> None:
        # Prediction: products keep the supplier alive through their references.
        supplier_ref = weakref.ref(self.supplier)
        del self.supplier
        gc.collect()
        self.assertIsNotNone(supplier_ref())
        self.assertIs(self.physical.get_supplier(), supplier_ref())
        self.assertEqual(self.digital.get_supplier().get_name(), "ABC Supplies")

    def test_association_supplier_survives_product_deletion(self) -> None:
        product_ref = weakref.ref(self.physical)
        del self.physical
        gc.collect()
        self.assertIsNone(product_ref())
        self.assertEqual(self.supplier.get_supplier_id(), "S001")

    def test_aggregation_transfer_preserves_product_identity(self) -> None:
        inventory_a = Inventory()
        inventory_b = Inventory()
        inventory_a.add_product(self.physical)
        self.assertIs(inventory_a.find_product("P001"), self.physical)
        inventory_a.remove_product("P001")
        self.assertIsNone(inventory_a.find_product("P001"))
        self.assertEqual(self.physical.get_name(), "Book")
        inventory_b.add_product(self.physical)
        self.assertIs(inventory_b.find_product("P001"), self.physical)

    def test_aggregation_inventory_deletion_preserves_products(self) -> None:
        inventory = Inventory()
        inventory.add_product(self.physical)
        inventory_ref = weakref.ref(inventory)
        del inventory
        gc.collect()
        self.assertIsNone(inventory_ref())
        self.assertEqual(self.physical.get_price(), 10.0)

    def test_inventory_accepts_both_product_subclasses(self) -> None:
        inventory = Inventory()
        for product in (self.physical, self.digital):
            inventory.add_product(product)
            inventory.update_stock(product.get_product_id(), 20)
            self.assertEqual(product.get_stock(), 20)
            self.assertIs(inventory.find_product(product.get_product_id()), product)
        self.assertEqual(inventory.get_all_products(), (self.physical, self.digital))

    def test_find_product_returns_existing_object_or_none(self) -> None:
        inventory = Inventory()
        inventory.add_product(self.physical)
        self.assertIs(inventory.find_product("P001"), self.physical)
        self.assertIsNone(inventory.find_product("missing"))
        inventory.remove_product("P001")
        self.assertIsNone(inventory.find_product("P001"))

    def test_order_line_references_existing_product_and_calculates_subtotal(self) -> None:
        line = OrderLine(self.physical, 3)
        self.assertIs(line.get_product(), self.physical)
        self.assertEqual(line.get_quantity(), 3)
        self.assertAlmostEqual(line.calculate_subtotal(), 30.0)
        del line
        self.assertEqual(self.physical.get_price(), 10.0)

    def test_composition_orders_create_distinct_lines_for_one_product(self) -> None:
        # Prediction: one shared Product, two different OrderLine objects.
        order_a = Order("O001")
        order_b = Order("O002")
        with patch("order.OrderLine", wraps=OrderLine) as create_line:
            order_a.add_order_line(self.physical, 2)
            order_b.add_order_line(self.physical, 3)
            self.assertEqual(create_line.call_count, 2)
        # Private storage is inspected only to verify line identity/ownership.
        line_a = order_a._Order__order_lines[0]
        line_b = order_b._Order__order_lines[0]
        self.assertIsNot(line_a, line_b)
        self.assertIs(line_a.get_product(), self.physical)
        self.assertIs(line_b.get_product(), self.physical)
        self.assertEqual(order_a.get_order_lines(), [(self.physical, 2, 20.0)])
        self.assertEqual(order_b.get_order_lines(), [(self.physical, 3, 30.0)])

    def test_composition_removing_line_releases_it_but_preserves_product(self) -> None:
        order = Order("O001")
        order.add_order_line(self.physical, 2)
        line_ref = weakref.ref(order._Order__order_lines[0])
        order.remove_order_line(0)
        gc.collect()
        self.assertIsNone(line_ref())
        self.assertEqual(order.get_order_lines(), [])
        self.assertEqual(self.physical.get_name(), "Book")

    def test_composition_order_deletion_releases_lines_not_products(self) -> None:
        order = Order("O001")
        order.add_order_line(self.physical, 2)
        line_ref = weakref.ref(order._Order__order_lines[0])
        del order
        gc.collect()
        self.assertIsNone(line_ref())
        self.assertEqual(self.physical.get_name(), "Book")

    def test_order_total_uses_line_subtotals(self) -> None:
        order = Order("O001")
        self.assertEqual(order.calculate_total(), 0.0)
        order.add_order_line(self.physical, 2)
        order.add_order_line(self.digital, 3)
        self.assertAlmostEqual(order.calculate_total(), 32.0)
        with patch.object(OrderLine, "calculate_subtotal", return_value=7.5):
            self.assertAlmostEqual(order.calculate_total(), 15.0)
        order.remove_order_line(0)
        self.assertAlmostEqual(order.calculate_total(), 12.0)

    def test_order_line_snapshot_does_not_expose_internal_collection(self) -> None:
        order = Order("O001")
        order.add_order_line(self.physical, 2)
        snapshot = order.get_order_lines()
        snapshot.clear()
        self.assertEqual(order.get_order_lines(), [(self.physical, 2, 20.0)])

if __name__ == "__main__":
    unittest.main(verbosity=2)
