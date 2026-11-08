"""
DigitalProduct module containing downloadable items.
"""

from product import Product
from supplier import Supplier
import typing


@Product.register_product_type("digital")
class DigitalProduct(Product):
    """Represents a digital product that has a download size and no physical shipping."""

    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size: float = download_size

    def get_download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> str:
        product_info = super().display_information()
        return f"{product_info} | Download Size: {self.get_download_size()}MB"

    def get_fulfilment_info(self) -> str:
        return f"Digital product. No shipping required. Download Size: {self.get_download_size()}MB"

    def to_dict(self) -> dict[str, str | float | int]:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.get_download_size()
        return data

    @classmethod
    def from_dict(cls, item: dict[str, typing.Any]):
        """Instantiate a DigitalProduct from a dictionary."""
        return cls(
            item["id"], item["name"], item["price"],
            item["stock"], item["download_size"], item.get("supplier")
        )

    @classmethod
    def get_ui_inputs(cls, product_id: str, name: str, price: float, stock: int, read_number_func: typing.Callable[..., float]) -> 'DigitalProduct':
        """Prompt user for digital-specific inputs and return a DigitalProduct instance."""
        download_size = read_number_func("Download Size (MB): ", float)
        return cls(product_id, name, price, stock, download_size)