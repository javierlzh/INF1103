from math import isfinite

from discount_strategy import DiscountStrategy


class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, discount_amount: float) -> None:
        if type(threshold) not in (int, float) or not isfinite(threshold) or threshold <= 0:
            raise ValueError("Bulk threshold must be a finite number greater than zero.")
        if type(discount_amount) not in (int, float) or not isfinite(discount_amount) or discount_amount < 0:
            raise ValueError("Discount amount must be a finite, nonnegative number.")
        self.threshold = threshold
        self.discount_amount = discount_amount

    def apply(self, total: float) -> float:
        """Subtract the fixed amount when the order total meets the threshold."""
        if type(total) not in (int, float) or not isfinite(total) or total < 0:
            raise ValueError("Total must be a finite, nonnegative number.")
        if total >= self.threshold:
            if self.discount_amount > total:
                raise ValueError("Discount amount cannot exceed the total.")
            return total - self.discount_amount
        return total
