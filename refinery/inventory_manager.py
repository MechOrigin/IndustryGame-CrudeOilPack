# inventory_manager.py
class InventoryManager:
    def __init__(self, update_callback=None):
        self.inventory = {"Crude Oil": 80}
        self.money = 0
        self.update_callback = update_callback

    def add_to_inventory(self, item, amount):
        if item == "Money":
            self.money += amount
        else:
            self.inventory[item] = self.inventory.get(item, 0) + amount
        self.trigger_update()

    def remove_from_inventory(self, item, amount):
        if item in self.inventory and self.inventory[item] >= amount:
            self.inventory[item] -= amount
            self.trigger_update()
            return True
        return False

    def get_inventory(self):
        return {**self.inventory, "Money": round(self.money, 2)}

    def set_inventory(self, inventory):
        self.inventory = inventory
        self.money = inventory.get("Money", self.money)
        self.trigger_update()

    def get_player_trades(self):
        """Returns player trades for market interactions."""
        return {product: 0 for product in ["Diesel", "Gasoline", "Light Hydrocarbons", "Crude Oil"]}

    def set_update_callback(self, callback):
        self.update_callback = callback

    def reset_inventory(self):
        self.inventory = {"Crude Oil": 80}
        self.money = 0
        self.trigger_update()

    def trigger_update(self):
        if self.update_callback:
            self.update_callback(self.get_inventory())
