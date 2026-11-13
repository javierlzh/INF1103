"""
Persistence module handling JSON file loading, saving, and validation dynamically.
"""

import json
from typing import TypeGuard
from inventory import Inventory
from product import Product
from product_data import ProductData
from supplier import Supplier, is_supplier_data

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

def is_valid_item(item: object) -> TypeGuard[ProductData]:
    """Validate a saved record before passing it to a typed product factory."""
    if not isinstance(item, dict):
        return False
    if not all(isinstance(item.get(key), str) for key in ("id", "name", "type")):
        return False
    if item["type"] not in Product._registry:
        return False
    if type(item.get("price")) not in (int, float) or type(item.get("stock")) is not int:
        return False
    if not is_supplier_data(item.get("supplier")):
        return False
    for key in ("weight", "download_size"):
        if key in item and type(item[key]) not in (int, float):
            return False
    if "billing_cycle" in item and not isinstance(item["billing_cycle"], str):
        return False
    required_fields: dict[str, str] = {
        "physical": "weight", "digital": "download_size", "subscription": "billing_cycle"
    }
    required_field = required_fields.get(item["type"])
    return required_field is None or required_field in item

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
        print(f"Could not load inventory: {e}")
        inventory = Inventory()
        status = "error"
    return inventory, status
