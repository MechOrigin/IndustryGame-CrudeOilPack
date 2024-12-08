# inventory_manager.py
class InventoryManager:
    def __init__(self, update_callback=None):
        self.inventory = {"Crude Oil": 80}
        self.money = 0  # New attribute for money
        self.update_callback = update_callback

    def add_to_inventory(self, item, amount):
        if item == "Money":
            self.money += amount  # Update money if item is "Money"
        else:
            if item in self.inventory:
                self.inventory[item] += amount
            else:
                self.inventory[item] = amount

        if self.update_callback:
            self.update_callback(self.get_inventory())


    def remove_from_inventory(self, item, amount):
        if self.inventory.get(item, 0) >= amount:
            self.inventory[item] -= amount
            if self.update_callback:
                self.update_callback(self.inventory)
            return True
        return False

    def get_inventory(self):
        return {**self.inventory, "Money": round(self.money, 2)}  # Include money in the inventory


    def set_update_callback(self, callback):
        self.update_callback = callback

    def trigger_update(self):
        if self.update_callback:
            self.update_callback(self.inventory)