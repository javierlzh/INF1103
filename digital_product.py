"""
DigitalProduct module containing downloadable items.
"""

from product import Product


class DigitalProduct(Product):
    """Represents a digital product that has a download size and no physical shipping."""

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = download_size

    @property
    def download_size(self):
        return self.__download_size

    def display_information(self):
        product_info = super().display_information()
        return f"{product_info} | Download Size: {self.download_size}MB"

    def get_fulfilment_info(self):
        return f"Digital product. No shipping required. Download Size: {self.download_size}MB"

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.download_size
        return data