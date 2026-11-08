"""
Product module containing the abstract base class Product and the Product Registry.
"""

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from supplier import Supplier

class Product(ABC):
    """Abstract base class representing a generic product in inventory."""
    
    # Registry dictionary to store product types dynamically
    _registry: dict[str, type["Product"]] = {}

    @classmethod
    def register_product_type(cls, product_type: str) -> Callable[[type["Product"]], type["Product"]]:
        """Decorator or method to register a subclass."""
        def decorator(subclass: type["Product"]) -> type["Product"]:
            cls._registry[product_type] = subclass
            return subclass
        return decorator

    @classmethod
    def create_from_dict(cls, item: dict[str, Any], suppliers: dict[str, Supplier] | None = None) -> 'Product':
        """Polymorphic factory: instantiates the correct subclass from a dict."""
        product_type = item.get("type")
        if product_type not in cls._registry:
            raise ValueError(f"Unknown product type: {product_type}")
        supplier_data = item.get("supplier")
        if not isinstance(supplier_data, dict):
            raise ValueError(f"Product {item.get('id')} needs supplier details.")
        supplier = Supplier.from_dict(supplier_data)
        if suppliers is not None:
            supplier_id = supplier.get_supplier_id()
            if supplier_id in suppliers:
                if suppliers[supplier_id].to_dict() != supplier.to_dict():
                    raise ValueError(f"Conflicting details for supplier {supplier_id}.")
                supplier = suppliers[supplier_id]
            else:
                suppliers[supplier_id] = supplier
        return cls._registry[product_type].from_dict(item, supplier)

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier) -> None:
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def display_information(self) -> str:
        return f"ID: {self.get_product_id()} | Name: {self.get_name()} | Price: ${self.get_price():.2f} | Stock: {self.get_stock()}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.get_product_id(),
            "name": self.get_name(),
            "price": self.get_price(),
            "stock": self.get_stock(),
            "supplier": self.get_supplier().to_dict()
        }

    def update_stock(self, new_stock: int) -> bool:
        if new_stock < 0:
            return False
        self.__stock = new_stock
        return True

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, item: dict[str, Any], supplier: Supplier) -> 'Product':
        """Each product knows how to build itself from dictionary data."""
        pass

    @classmethod
    @abstractmethod
    def get_ui_inputs(cls, product_id: str, name: str, price: float, stock: int, read_number_func: Callable[..., int | float], supplier: Supplier) -> 'Product':
        """Each product knows what specific UI prompts it needs."""
        pass
