"""Set up controller state for focused CSV-loading tests."""
from inventory import Inventory
from main import Main
from supplier import Supplier


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    app = Main()
    app._Main__inventory = inventory
    app._Main__supplier = supplier
    app.load_products(path)
