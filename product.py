"""
Product module containing the abstract base class Product and the Product Registry.
"""

from abc import ABC, abstractmethod

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

    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock

    def display_information(self):
        return f"ID: {self.product_id} | Name: {self.name} | Price: ${self.price:.2f} | Stock: {self.stock}"

    def to_dict(self):
        return {
            "id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock
        }

    def update_stock(self, new_stock):
        if new_stock < 0:
            return False
        self.__stock = new_stock
        return True

    @abstractmethod
    def get_fulfilment_info(self):
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