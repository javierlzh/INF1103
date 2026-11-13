from math import isfinite
from typing import cast

from product import Product
from product_data import ProductData
from read_number import ReadNumber
from can_be_shipped import CanBeShipped
from supplier import Supplier

@Product.register_product_type("physical")
class PhysicalProduct(Product, CanBeShipped):
    """Represents a physical product that requires shipping and has weight."""

    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if type(weight) not in (int, float) or not isfinite(weight) or weight < 0:
            raise ValueError("Weight must be a finite, nonnegative number.")
        self.__weight: float = weight

    def get_weight(self) -> float:
        return self.__weight

    def display_information(self) -> str:
        product_info = super().display_information()
        return f"{product_info} | Weight: {self.get_weight()}kg"

    def get_fulfilment_info(self) -> str:
        return f"Physical product. Shipping required. Weight: {self.get_weight()}kg"

    def calculate_shipping_cost(self) -> float:
        return self.get_weight() * 0.5

    def to_dict(self) -> ProductData:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.get_weight()
        return data

    @classmethod
    def from_dict(cls, item: ProductData, supplier: Supplier) -> 'PhysicalProduct':
        from product_factory import ProductFactory

        if "weight" not in item:
            raise ValueError("Physical product requires weight.")
        return cast(PhysicalProduct, ProductFactory.create('physical', item['id'], item['name'], item['price'], item['stock'], item['weight'], supplier))

    @classmethod
    def get_ui_inputs(cls, product_id: str, name: str, price: float, stock: int, read_number_func: ReadNumber, supplier: Supplier) -> 'PhysicalProduct':
        from product_factory import ProductFactory

        weight = read_number_func("Weight (kg): ", float)
        return cast(PhysicalProduct, ProductFactory.create('physical', product_id, name, price, stock, weight, supplier))
