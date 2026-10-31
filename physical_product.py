"""
PhysicalProduct module containing physical inventory items.
"""

from product import Product
from can_be_shipped import CanBeShipped

@Product.register_product_type("physical")
class PhysicalProduct(Product, CanBeShipped):
    """Represents a physical product that requires shipping and has weight."""

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    @property
    def weight(self):
        return self.__weight

    def display_information(self):
        product_info = super().display_information()
        return f"{product_info} | Weight: {self.weight}kg"

    def get_fulfilment_info(self):
        return f"Physical product. Shipping required. Weight: {self.weight}kg"

    def calculate_shipping_cost(self):
        return self.weight * 0.5

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.weight
        return data

    @classmethod
    def from_dict(cls, item):
        return cls(
            item["id"], item["name"], item["price"],
            item["stock"], item["weight"]
        )

    @classmethod
    def get_ui_inputs(cls, product_id, name, price, stock, read_number_func):
        weight = read_number_func("Weight (kg): ", float)
        return cls(product_id, name, price, stock, weight)