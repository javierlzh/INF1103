from math import isfinite

from discount_strategy import DiscountStrategy


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float) -> None:
        if type(percentage) not in (int, float) or not isfinite(percentage) or not 0 <= percentage <= 100:
            raise ValueError("Discount percentage must be between 0 and 100.")
        self.percentage = percentage

    def apply(self, total: float) -> float:
        if type(total) not in (int, float) or not isfinite(total) or total < 0:
            raise ValueError("Total must be a finite, nonnegative number.")
        discount_amount = total * (self.percentage / 100)
        return total - discount_amount
