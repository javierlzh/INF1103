from model_types import ProductData, ReadNumber

from product import Product
from supplier import Supplier

@Product.register_product_type("subscription")
class SubscriptionProduct(Product):
    """Represents a subscription-based product with a billing cycle."""

    def __init__(self, product_id: str, name: str, price: float, stock: int, billing_cycle: str, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__billing_cycle: str = billing_cycle

    def get_billing_cycle(self) -> str:
        return self.__billing_cycle

    def display_information(self) -> str:
        product_info = super().display_information()
        return f"{product_info} | Billing Cycle: {self.get_billing_cycle()}"

    def get_fulfilment_info(self) -> str:
        return f"Subscription product. No physical fulfillment. Billing cycle: {self.get_billing_cycle()}"

    def to_dict(self) -> ProductData:
        data = super().to_dict()
        data["type"] = "subscription"
        data["billing_cycle"] = self.get_billing_cycle()
        return data

    @classmethod
    def from_dict(cls, item: ProductData, supplier: Supplier) -> 'SubscriptionProduct':
        if "billing_cycle" not in item:
            raise ValueError("Subscription product requires billing cycle.")
        return cls(
            item["id"], item["name"], item["price"],
            item["stock"], item["billing_cycle"], supplier
        )

    @classmethod
    def get_ui_inputs(cls, product_id: str, name: str, price: float, stock: int, read_number_func: ReadNumber, supplier: Supplier) -> 'SubscriptionProduct':
        billing_cycle = input("Billing Cycle (e.g., Monthly/Yearly): ").strip()
        return cls(product_id, name, price, stock, billing_cycle, supplier)
