import datetime
import random
from refinery.inventory_manager import InventoryManager
from refinery.stock_graph import StockGraph

class Market:
    def __init__(self, chat_box):
        self.chat_box = chat_box
        self.prices = {"Gasoline": 5, "Diesel": 6, "Light Hydrocarbons": 4, "Crude Oil": 3}
        self.price_history = {key: [] for key in self.prices}
        self.time_history = []
        self.inventory_manager = InventoryManager()

    def add_to_inventory(self, item, amount):
        self.inventory[item] = self.inventory.get(item, 0) + amount
        if self.update_callback:
            self.update_callback(self.inventory)

    def remove_from_inventory(self, item, amount):
        if item in self.inventory and self.inventory[item] >= amount:
            self.inventory[item] -= amount
            if self.update_callback:
                self.update_callback(self.inventory)
            
    def update_prices(self):
        for product in self.prices:
            self.prices[product] *= 1 + random.uniform(-0.05, 0.05)
            self.price_history[product].append(self.prices[product])
        self.time_history.append(datetime.now())

    def show_graph(self):
        self.stock_graph.display()

    def get_state(self):
        return {"prices": self.prices, "history": self.price_history, "time": self.time_history}

    def load_state(self, state):
        self.prices = state["prices"]
        self.price_history = state["history"]
        self.time_history = state["time"]
