from order_line import OrderLine
from product import Product
from discount_strategy import DiscountStrategy
from no_discount import NoDiscount

class Order:
    """Represents an order containing products and their quantities."""
    
    def __init__(self, order_id: str, discount_strategy: DiscountStrategy | None = None) -> None:
        self.__order_id: str = order_id
        self.__discount_strategy: DiscountStrategy = (NoDiscount() if discount_strategy is None else discount_strategy)
        self.__order_lines: list[OrderLine] = []  # List to hold OrderLine instances

    def get_order_id(self) -> str:
        return self.__order_id

    def set_discount(self, discount_strategy: DiscountStrategy) -> None:
        """Set the discount strategy for the order."""
        self.__discount_strategy = discount_strategy
    
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
        total = sum(line.calculate_subtotal() for line in self.__order_lines)
        return self.__discount_strategy.apply(total)