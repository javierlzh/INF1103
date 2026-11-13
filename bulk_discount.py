class BulkDiscount:
    def __init__(self, threshold: int, discount_amount: float):
        self.threshold = threshold
        self.discount_amount = discount_amount

    def apply(self, total: float, quantity: int) -> float:
        if quantity >= self.threshold:
            return total - self.discount_amount
        return total