from product import Product

class OrderLine:
    """Represents a line item in an order, linking a product with a quantity."""
    
    def __init__(self, product: Product, quantity: int) -> None:
        if not isinstance(product, Product):
            raise ValueError("Order line requires a Product object.")
        if type(quantity) is not int:
            raise ValueError("Quantity must be a whole number.")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.__product: Product = product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        """Calculate the total price for this order line."""
        return self.__product.get_price() * self.__quantity  
