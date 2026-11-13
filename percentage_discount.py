from math import isfinite

from discount_strategy import DiscountStrategy


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent: float) -> None:
        if type(percent) not in (int, float) or not isfinite(percent) or not 0 <= percent <= 100:
            raise ValueError("Discount percentage must be between 0 and 100.")
        self.__percent: float = percent

    def apply(self, total: float) -> float:
        if type(total) not in (int, float) or not isfinite(total) or total < 0:
            raise ValueError("Total must be a finite, nonnegative number.")
        discount_amount = total * (self.__percent / 100)
        return total - discount_amount
