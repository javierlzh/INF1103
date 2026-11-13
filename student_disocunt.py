from discount_strategy import DiscountStrategy

class StudentDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        """Apply a 10% discount for students."""
        return total * 0.9