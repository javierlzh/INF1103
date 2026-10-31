"""
Persistence module handling JSON file loading, saving, and validation.
"""

import json
from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct

INVENTORY_FILE = "inventory.json"


def save_inventory(inventory):
    """Save the inventory collection to the JSON file."""
    try:
        with open(INVENTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(inventory.to_list(), file, indent=4)
        return True
    except OSError:
        return False


def create_product(item):
    """Factory function to instantiate the correct Product subclass from a dictionary."""
    if item["type"] == "physical":
        shipping_rate = item.get("shipping_rate", 0.5)
        return PhysicalProduct(
            item["id"], item["name"], item["price"],
            item["stock"], item["weight"], shipping_rate
        )
    return DigitalProduct(
        item["id"], item["name"], item["price"],
        item["stock"], item["download_size"]
    )


def is_valid_item(item):
    """Validate dictionary fields and data types for a product entry."""
    if not isinstance(item, dict):
        return False
    for key in ("type", "id", "name", "price", "stock"):
        if key not in item:
            return False
    if not (isinstance(item["id"], str) and item["id"].strip() != ""
            and isinstance(item["name"], str) 
            and isinstance(item["price"], (int, float)) and item["price"] >= 0
            and isinstance(item["stock"], int) and item["stock"] >= 0):
        return False
    if item["type"] == "physical":
        return isinstance(item.get("weight"), (int, float)) and item["weight"] >= 0
    if item["type"] == "digital":
        return isinstance(item.get("download_size"), (int, float)) and item["download_size"] >= 0
    return False


def load_inventory():
    """Load inventory data from the JSON file and return the inventory and status."""
    inventory = Inventory()
    status = "loaded"
    try:
        with open(INVENTORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise ValueError("Top level of the file must be a list.")
        for item in data:
            if not is_valid_item(item):
                raise ValueError("Invalid product entry.")
            product = create_product(item)
            if not inventory.add_product(product):
                status = "duplicates"
    except FileNotFoundError:
        status = "not_found"
    except (OSError, ValueError):
        inventory = Inventory()
        status = "error"
    return inventory, status