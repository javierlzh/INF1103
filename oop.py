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