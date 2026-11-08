from order_line import OrderLine
from product import Product

class Order:
    """Represents an order containing products and their quantities."""
    
    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []  # List to hold OrderLine instances

    def get_order_id(self) -> str:
        return self.__order_id
    
    def add_order_line(self, product: Product, quantity: int) -> None:
        """Add a product and its quantity to the order."""
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, index: int) -> None:
        """Remove a line by index. Raise IndexError if out of bounds."""
        del self.__order_lines[index]

    def get_order_lines(self) -> list[tuple[Product, int, float]]:
        return [
        (line.get_product(),
         line.get_quantity(),
         line.calculate_subtotal())
        for line in self.__order_lines
        ]

    def calculate_total(self) -> float:
        """Calculate the total price for the entire order."""
        return sum(line.calculate_subtotal() for line in self.__order_lines)