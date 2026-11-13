from product import Product
from product_data import ProductData


class Inventory:
    """Manages a collection of Product objects."""

    def __init__(self) -> None:
        self.__products: dict[str, Product] = {}

    def to_list(self) -> list[ProductData]:
        """Convert all products in inventory to a list of dictionaries."""
        return [product.to_dict() for product in self.__products.values()]

    def display_all(self) -> None:
        """Display details of all products currently in inventory."""
        print("\nCurrent Inventory")
        print("-" * 48)
        if len(self.__products) == 0:
            print("No products in inventory.")
        for p in self.__products.values():
            print(p.display_information())
        print("-" * 48)

    def get_all_products(self) -> tuple[Product, ...]:
        """Return an immutable collection of product references."""
        return tuple(self.__products.values())

    def find_product(self, product_id: str) -> Product | None:
        """Return the matching product, or None if the ID is not found."""
        return self.__products.get(product_id)

    def add_product(self, product: Product) -> None:
        """Store a product. Raise ValueError for a duplicate ID."""
        if not isinstance(product, Product):
            raise ValueError("Inventory requires a Product object.")
        product_id = product.get_product_id()
        if product_id in self.__products:
            raise ValueError(f"Product {product_id} already exists.")
        self.__products[product_id] = product

    def update_stock(self, product_id: str, quantity: int) -> None:
        """Set stock. Raise KeyError if the product is missing."""
        product = self.find_product(product_id)
        if product is None:
            raise KeyError(product_id)
        product.update_stock(quantity)

    def remove_product(self, product_id: str) -> None:
        """Remove the reference. Raise KeyError if the ID is missing."""
        del self.__products[product_id]

    @staticmethod
    def show_product_details(product: Product) -> None:
        """Display detailed information about a specific product."""
        print("\nProduct Details")
        print("-" * 48)
        print(product.display_information())
        print(product.get_fulfilment_info())
        print("-" * 48)
