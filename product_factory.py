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
        stock: int,
        extra_value: float,
        supplier: Supplier,
    ) -> Product:
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock, extra_value, supplier)
        if product_type == "digital":
            return DigitalProduct(product_id, name, price, stock, extra_value, supplier)
        else:
            raise ValueError(f"Unknown product type: {product_type}")

    @staticmethod
    def create_subscription(
        product_id: str, name: str, price: float, stock: int,
        billing_cycle: str, supplier: Supplier,
    ) -> Product:
        """Keep the existing subscription extension outside the UML create interface."""
        return SubscriptionProduct(product_id, name, price, stock, billing_cycle, supplier)
