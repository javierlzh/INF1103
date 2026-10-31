"""
SubscriptionProduct module.
"""

from product import Product

@Product.register_product_type("subscription")
class SubscriptionProduct(Product):
    """Represents a subscription-based product with a billing cycle."""

    def __init__(self, product_id, name, price, stock, billing_cycle):
        super().__init__(product_id, name, price, stock)
        self.__billing_cycle = billing_cycle

    @property
    def billing_cycle(self):
        return self.__billing_cycle

    def display_information(self):
        product_info = super().display_information()
        return f"{product_info} | Billing Cycle: {self.billing_cycle}"

    def get_fulfilment_info(self):
        return f"Subscription product. No physical fulfillment. Billing cycle: {self.billing_cycle}"

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "subscription"
        data["billing_cycle"] = self.billing_cycle
        return data

    @classmethod
    def from_dict(cls, item):
        return cls(
            item["id"], item["name"], item["price"],
            item["stock"], item["billing_cycle"]
        )

    @classmethod
    def get_ui_inputs(cls, product_id, name, price, stock, read_number_func):
        billing_cycle = input("Billing Cycle (e.g., Monthly/Yearly): ").strip()
        return cls(product_id, name, price, stock, billing_cycle)