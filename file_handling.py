from inventory import Inventory
import persistence

class FileHandling:
    def load_inventory(self) -> tuple[Inventory, str]:
        return persistence.load_inventory()

    def save_inventory(self, inventory: Inventory) -> bool:
        return persistence.save_inventory(inventory)
