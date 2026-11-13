from math import isfinite

from discount_strategy import DiscountStrategy


class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float) -> None:
        if type(threshold) not in (int, float) or not isfinite(threshold) or threshold <= 0:
            raise ValueError("Bulk threshold must be a finite number greater than zero.")
        if type(amount) not in (int, float) or not isfinite(amount) or amount < 0:
            raise ValueError("Discount amount must be a finite, nonnegative number.")
        self.__threshold: float = threshold
        self.__amount: float = amount

    def apply(self, total: float) -> float:
        """Subtract the fixed amount when the order total meets the threshold."""
        if type(total) not in (int, float) or not isfinite(total) or total < 0:
            raise ValueError("Total must be a finite, nonnegative number.")
        if total >= self.__threshold:
            if self.__amount > total:
                raise ValueError("Discount amount cannot exceed the total.")
            return total - self.__amount
        return total
