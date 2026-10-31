"""
PhysicalProduct module containing physical inventory items.
"""

from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    """Represents a physical product that requires shipping and has weight."""

    def __init__(self, product_id, name, price, stock, weight, shipping_rate=0.5):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight
        self.__shipping_rate = shipping_rate

    @property
    def weight(self):
        return self.__weight

    @property
    def shipping_rate(self):
        return self.__shipping_rate

    def display_information(self):
        product_info = super().display_information()
        return f"{product_info} | Weight: {self.weight}kg"

    def get_fulfilment_info(self):
        return f"Physical product. Shipping required. Weight: {self.weight}kg"

    def calculate_shipping_cost(self):
        # Uses a dynamic instance attribute instead of a hardcoded magic number
        return self.weight * self.shipping_rate

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.weight
        data["shipping_rate"] = self.shipping_rate
        return data