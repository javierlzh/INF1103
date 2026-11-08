"""
Persistence module handling JSON file loading, saving, and validation dynamically.
"""

import json
from typing import TypeGuard
from model_types import ProductData, is_product_data
from inventory import Inventory
from product import Product
from supplier import Supplier

INVENTORY_FILE: str = "inventory.json"

def save_inventory(inventory: Inventory) -> bool:
    try:
        with open(INVENTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(inventory.to_list(), file, indent=4)
        return True
    except OSError:
        return False

def is_valid_item(item: object) -> TypeGuard[ProductData]:
    """Validate a saved record before passing it to a typed product factory."""
    return is_product_data(item) and item.get("type") in Product._registry

def load_inventory() -> tuple[Inventory, str]:
    inventory = Inventory()
    status = "loaded"
    suppliers: dict[str, Supplier] = {}
    try:
        with open(INVENTORY_FILE, "r", encoding="utf-8") as file:
            data: object = json.load(file)
        if not isinstance(data, list):
            raise ValueError("Top level of the file must be a list.")
        for item in data:
            if not is_valid_item(item):
                raise ValueError("Invalid product entry.")
            product = Product.create_from_dict(item, suppliers)
            if inventory.find_product(product.get_product_id()) is not None:
                status = "duplicates"
                continue
            inventory.add_product(product)
    except FileNotFoundError:
        status = "not_found"
    except (OSError, ValueError) as e:
        print(f"DEBUG ERROR: {e}")
        inventory = Inventory()
        status = "error"
    return inventory, status
