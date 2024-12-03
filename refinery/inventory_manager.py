# inventory_manager.py
class InventoryManager:
    def __init__(self, update_callback=None):
        self.inventory = {"Crude Oil": 80}
        self.update_callback = update_callback

    def add_to_inventory(self, item, amount):
        self.inventory[item] = self.inventory.get(item, 0) + amount
        if self.update_callback:
            self.update_callback(self.inventory)

    def remove_from_inventory(self, item, amount):
        if item in self.inventory and self.inventory[item] >= amount:
            self.inventory[item] -= amount
            if self.update_callback:
                self.update_callback(self.inventory)
                return True
        return False

    def get_inventory(self):
        return self.inventory

    def set_update_callback(self, callback):
        self.update_callback = callback
