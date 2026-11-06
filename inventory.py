"""
Inventory module to manage collections of products.
"""

from product import Product


class Inventory:
    """Manages a collection of Product objects."""

    def __init__(self):
        self.__inventory: list[Product] = []  # List to hold Product instances

    def to_list(self):
        """Convert all products in inventory to a list of dictionaries."""
        return [product.to_dict() for product in self.__inventory]

    def display_all(self):
        """Display details of all products currently in inventory."""
        print("\nCurrent Inventory")
        print("-" * 48)
        if len(self.__inventory) == 0:
            print("No products in inventory.")
        for p in self.__inventory:
            print(p.display_information())
        print("-" * 48)

    def search_product(self, product_id: str) -> Product | None:
        """Search for a product by its ID. Returns the product or None."""
        for product in self.__inventory:
            if product.get_product_id() == product_id:
                return product
        return None
    
    def add_product(self, product: Product):
        """Add a Product. Returns False if its ID already exists."""
        if self.search_product(product.get_product_id()) is not None:
            return False
        self.__inventory.append(product)
        return True

    def update_stock(self, product_id: str, new_stock: int):
        """Set stock to new_stock. Returns False if new_stock is negative or not found."""
        product = self.search_product(product_id)
        if product is None:
            return False
        return product.update_stock(new_stock)

    def remove_product(self, product_id: str):
        """Remove a product by its ID. Returns False if not found."""
        product = self.search_product(product_id)
        if product is None:
            return False
        self.__inventory.remove(product)
        return True