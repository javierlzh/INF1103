from abc import ABC, abstractmethod
from math import isfinite
from collections.abc import Callable
from typing import TypeVar

from product_data import ProductData
from read_number import ReadNumber
from supplier import Supplier

_ProductType = TypeVar("_ProductType", bound="Product")

class Product(ABC):
    """Abstract base class representing a generic product in inventory."""
    
    # Registry dictionary to store product types dynamically
    _registry: dict[str, type["Product"]] = {}

    @classmethod
    def register_product_type(cls, product_type: str) -> Callable[[type[_ProductType]], type[_ProductType]]:
        """Decorator or method to register a subclass."""
        def decorator(subclass: type[_ProductType]) -> type[_ProductType]:
            cls._registry[product_type] = subclass
            return subclass
        return decorator

    @classmethod
    def create_from_dict(cls, item: ProductData, suppliers: dict[str, Supplier] | None = None) -> 'Product':
        """Polymorphic factory: instantiates the correct subclass from a dict."""
        product_type = item.get("type")
        if product_type is None or product_type not in cls._registry:
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
        if not isinstance(product_id, str) or not product_id.strip():
            raise ValueError("Product ID cannot be empty.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name cannot be empty.")
        if type(price) not in (int, float) or not isfinite(price) or price <= 0:
            raise ValueError("Price must be greater than zero.")
        if type(stock) is not int:
            raise ValueError("Stock must be a whole number.")
        if stock < 0:
            raise ValueError("Stock cannot be negative.")
        if not isinstance(supplier, Supplier):
            raise ValueError("Product requires a Supplier object.")
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
        supplier = self.get_supplier()
        return (
            f"ID: {self.get_product_id()} | Name: {self.get_name()} "
            f"| Price: ${self.get_price():.2f} | Stock: {self.get_stock()} "
            f"| Supplier ID: {supplier.get_supplier_id()} "
            f"| Supplier: {supplier.get_name()} "
            f"| Contact Email: {supplier.get_contact_email()}"
        )

    def to_dict(self) -> ProductData:
        return {
            "id": self.get_product_id(),
            "name": self.get_name(),
            "price": self.get_price(),
            "stock": self.get_stock(),
            "supplier": self.get_supplier().to_dict()
        }

    def update_stock(self, quantity: int) -> None:
        """Set stock to quantity. Raise ValueError for negative stock."""
        if type(quantity) is not int:
            raise ValueError("Stock must be a whole number.")
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = quantity

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, item: ProductData, supplier: Supplier) -> 'Product':
        """Each product knows how to build itself from dictionary data."""
        pass

    @classmethod
    @abstractmethod
    def get_ui_inputs(cls, product_id: str, name: str, price: float, stock: int, read_number_func: ReadNumber, supplier: Supplier) -> 'Product':
        """Each product knows what specific UI prompts it needs."""
        pass
