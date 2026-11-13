from discount_strategy import DiscountStrategy


class HalfPriceDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total * 0.5
