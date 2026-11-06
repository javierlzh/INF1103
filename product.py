"""
Product module containing the abstract base class Product and the Product Registry.
"""

from abc import ABC, abstractmethod

from supplier import Supplier

class Product(ABC):
    """Abstract base class representing a generic product in inventory."""
    
    # Registry dictionary to store product types dynamically
    _registry = {}

    @classmethod
    def register_product_type(cls, product_type):
        """Decorator or method to register a subclass."""
        def decorator(subclass):
            cls._registry[product_type] = subclass
            return subclass
        return decorator

    @classmethod
    def create_from_dict(cls, item):
        """Polymorphic factory: instantiates the correct subclass from a dict."""
        product_type = item.get("type")
        if product_type not in cls._registry:
            raise ValueError(f"Unknown product type: {product_type}")
        return cls._registry[product_type].from_dict(item)

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier = None):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock
        self.__supplier: Supplier = supplier  # Optional association with a Supplier

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def get_supplier(self):
        return self.__supplier

    def display_information(self):
        return f"ID: {self.get_product_id()} | Name: {self.get_name()} | Price: ${self.get_price():.2f} | Stock: {self.get_stock()}"

    def to_dict(self):
        return {
            "id": self.get_product_id(),
            "name": self.get_name(),
            "price": self.get_price(),
            "stock": self.get_stock()
        }

    def update_stock(self, new_stock: int):
        if new_stock < 0:
            return False
        self.__stock = new_stock
        return True

    @abstractmethod
    def get_fulfilment_info(self: str):
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, item):
        """Each product knows how to build itself from dictionary data."""
        pass

    @classmethod
    @abstractmethod
    def get_ui_inputs(cls, product_id, name, price, stock, read_number_func):
        """Each product knows what specific UI prompts it needs."""
        pass