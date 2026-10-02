"""
INF1103 Week 5 - Inventory Manager
"""
import json
 
# Global Constant
INVENTORY_FILE = "inventory.json"
 
 
# ---------------------------------------------------------------
# Persistence Functions (no UI prompt and printing)
# ---------------------------------------------------------------
def load_inventory():
    """Load inventory from INVENTORY_FILE.
 
    Returns (inventory, status) where status is one of:
    "loaded", "not_found", "error".
    """
    inventory = []
    try:
        with open(INVENTORY_FILE, "r") as file:
            inventory = json.load(file)
        status = "loaded"
    except FileNotFoundError:
        inventory = []
        status = "not_found"
    except (json.JSONDecodeError, OSError):
        inventory = []
        status = "error"
    return inventory, status


# ---------------------------------------------------------------
# Manage UI Menu
# ---------------------------------------------------------------
def main():
    inventory, status = load_inventory()
    if status == "loaded":
        print(f"\n{INVENTORY_FILE} found.")
        print("Inventory loaded successfully.")
    elif status == "not_found":
        print(f"\n{INVENTORY_FILE} not found. Starting with empty inventory.")
    else:
        print(f"\nError reading {INVENTORY_FILE}. Starting with empty inventory.")
        

# __name__ (Program Entry Point)
if __name__ == "__main__":
    main()