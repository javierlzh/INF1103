class PercentageDiscount:
    def __init__(self, percentage: float):
        self.percentage = percentage

    def apply(self, total: float) -> float:
        discount_amount = total * (self.percentage / 100)
        return total - discount_amount