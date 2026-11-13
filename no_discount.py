from math import isfinite

from discount_strategy import DiscountStrategy

class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        if type(total) not in (int, float) or not isfinite(total) or total < 0:
            raise ValueError("Total must be a finite, nonnegative number.")
        return total
