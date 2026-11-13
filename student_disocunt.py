from math import isfinite

from discount_strategy import DiscountStrategy

class StudentDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        """Apply a 10% discount for students."""
        if type(total) not in (int, float) or not isfinite(total) or total < 0:
            raise ValueError("Total must be a finite, nonnegative number.")
        return total * 0.9
