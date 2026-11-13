from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from subscription_product import SubscriptionProduct
from supplier import Supplier

class ProductFactory:
    """Factory class to create Product instances."""
    
    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        *,
        weight: float | None = None,
        download_size: float | None = None,
        billing_cycle: str | None = None,
    ) -> Product:
        if product_type == "physical":
            if weight is None:
                raise ValueError("Physical products require a weight.")
            return PhysicalProduct(product_id, name, price, stock_quantity, weight, supplier)
        if product_type == "digital":
            if download_size is None:
                raise ValueError("Digital products require a download size.")
            return DigitalProduct(product_id, name, price, stock_quantity, download_size, supplier)
        if product_type == "subscription":
            if billing_cycle is None:
                raise ValueError("Subscription products require a billing cycle.")
            return SubscriptionProduct(product_id, name, price, stock_quantity, billing_cycle, supplier)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
