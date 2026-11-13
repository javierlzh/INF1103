from math import isfinite

from percentage_discount import PercentageDiscount


class StudentDiscount(PercentageDiscount):
    def __init__(self) -> None:
        super().__init__(5)

    def apply(self, total: float) -> float:
        """Apply the fixed 5% student discount."""
        if type(total) not in (int, float) or not isfinite(total) or total < 0:
            raise ValueError("Total must be a finite, nonnegative number.")
        return total * 0.95
