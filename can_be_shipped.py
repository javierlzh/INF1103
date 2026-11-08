from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface defining shipping cost calculation requirements."""

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass