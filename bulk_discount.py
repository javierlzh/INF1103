from math import isfinite


class BulkDiscount:
    def __init__(self, threshold: int, discount_amount: float) -> None:
        if type(threshold) is not int or threshold <= 0:
            raise ValueError("Bulk threshold must be a positive whole number.")
        if type(discount_amount) not in (int, float) or not isfinite(discount_amount) or discount_amount < 0:
            raise ValueError("Discount amount must be a finite, nonnegative number.")
        self.threshold = threshold
        self.discount_amount = discount_amount

    def apply(self, total: float, quantity: int) -> float:
        if type(total) not in (int, float) or not isfinite(total) or total < 0:
            raise ValueError("Total must be a finite, nonnegative number.")
        if type(quantity) is not int or quantity < 0:
            raise ValueError("Quantity must be a nonnegative whole number.")
        if quantity >= self.threshold:
            if self.discount_amount > total:
                raise ValueError("Discount amount cannot exceed the total.")
            return total - self.discount_amount
        return total
