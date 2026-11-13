from math import isfinite
from typing import cast

from product import Product
from product_data import ProductData
from read_number import ReadNumber
from supplier import Supplier


@Product.register_product_type("digital")
class DigitalProduct(Product):
    """Represents a digital product that has a download size and no physical shipping."""

    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if type(download_size) not in (int, float) or not isfinite(download_size) or download_size < 0:
            raise ValueError("Download size must be a finite, nonnegative number.")
        self.__download_size: float = download_size

    def get_download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> str:
        product_info = super().display_information()
        return f"{product_info} | Download Size: {self.get_download_size()}MB"

    def get_fulfilment_info(self) -> str:
        return f"Digital product. No shipping required. Download Size: {self.get_download_size()}MB"

    def to_dict(self) -> ProductData:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.get_download_size()
        return data

    @classmethod
    def from_dict(cls, item: ProductData, supplier: Supplier) -> 'DigitalProduct':
        """Instantiate a DigitalProduct from a dictionary."""
        from product_factory import ProductFactory

        if "download_size" not in item:
            raise ValueError("Digital product requires download size.")
        return cast(DigitalProduct, ProductFactory.create(
            "digital", item["id"], item["name"], item["price"], item["stock"],
            supplier, download_size=item["download_size"],
        ))

    @classmethod
    def get_ui_inputs(cls, product_id: str, name: str, price: float, stock: int, read_number_func: ReadNumber, supplier: Supplier) -> 'DigitalProduct':
        """Prompt user for digital-specific inputs and return a DigitalProduct instance."""
        from product_factory import ProductFactory

        download_size = read_number_func("Download Size (MB): ", float)
        return cast(DigitalProduct, ProductFactory.create(
            "digital", product_id, name, price, stock, supplier,
            download_size=download_size,
        ))
