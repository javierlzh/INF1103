"""
Inventory module to manage collections of products.
"""

class Inventory:
    """Manages a collection of Product objects."""

    def __init__(self):
        self.__inventory = []

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

    def search_product(self, product_id):
        """Search for a product by its ID. Returns the product or None."""
        for product in self.__inventory:
            if product.product_id == product_id:
                return product
        return None
    
    def add_product(self, product):
        """Add a Product. Returns False if its ID already exists."""
        if self.search_product(product.product_id) is not None:
            return False
        self.__inventory.append(product)
        return True

    def update_stock(self, product_id, new_stock):
        """Set stock to new_stock. Returns False if new_stock is negative or not found."""
        product = self.search_product(product_id)
        if product is None:
            return False
        return product.update_stock(new_stock)