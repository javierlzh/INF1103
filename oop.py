# ---------------------------------------------------------------
# Product class: stores and manages one product
# ---------------------------------------------------------------
class Product:
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

    def to_dict(self):  # Convert to a dict so json can save it.
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

# ---------------------------------------------------------------
# Inventory class: manages a collection of Product objects 
# ---------------------------------------------------------------
class Inventory:
    """Represents one product and manages its own state."""
    def __init__(self):
        self.__inventory = []

    def to_list(self):
        return [product.to_dict() for product in self.__inventory]

    def display_all(self):
        print("\nCurrent Inventory")
        print("-" * 48)
        if len(self.__inventory) == 0:
            print("No products in inventory.")
        for p in self.__inventory:
            print(p.display_information())
        print("-" * 48)

    def search_product(self, product_id):
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
        """Set stock to new_stock. Returns False if new_stock is negative."""
        product = self.search_product(product_id)
        if product is None:
            return False
        return product.update_stock(new_stock)