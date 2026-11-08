"""
Persistence module handling JSON file loading, saving, and validation dynamically.
"""

import json
from inventory import Inventory
from product import Product
from supplier import Supplier
# Make sure to import all product modules so their decorators execute!
import physical_product
import digital_product
import subscription_product

INVENTORY_FILE: str = "inventory.json"

def save_inventory(inventory: Inventory) -> bool:
    try:
        with open(INVENTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(inventory.to_list(), file, indent=4)
        return True
    except OSError:
        return False

def is_valid_item(item: object) -> bool:
    """Generic structural validation (type checking can also be delegated if desired)."""
    if not isinstance(item, dict):
        return False
    for key in ("type", "id", "name", "price", "stock"):
        if key not in item:
            return False
    return item["type"] in Product._registry

def load_inventory() -> tuple[Inventory, str]:
    inventory = Inventory()
    status = "loaded"
    suppliers: dict[str, Supplier] = {}
    try:
        with open(INVENTORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise ValueError("Top level of the file must be a list.")
        for item in data:
            if not is_valid_item(item):
                raise ValueError("Invalid product entry.")
            # Polymorphic creation handles any registered product type automatically!
            product = Product.create_from_dict(item, suppliers)
            if not inventory.add_product(product):
                status = "duplicates"
    except FileNotFoundError:
        status = "not_found"
    except (OSError, ValueError) as e:
        print(f"DEBUG ERROR: {e}")  # <-- Add this line temporarily
        inventory = Inventory()
        status = "error"
    return inventory, status
