# market.py
from datetime import datetime
from random import uniform
from refinery.stock_graph import StockGraph

class Market:
    def __init__(self, chat_box):
        self.chat_box = chat_box
        self.base_prices = {"Gasoline": 5, "Diesel": 6, "Light Hydrocarbons": 4, "Crude Oil": 3}
        self.prices = self.base_prices.copy()
        self.price_history = {key: [] for key in self.base_prices}
        self.time_history = []
        self.supply = {key: 1000 for key in self.base_prices}  # Initial supply
        self.demand = {key: 1000 for key in self.base_prices}  # Initial demand
        self.stock_graph = StockGraph(self)
        self.inventory_manager = None  # Placeholder for inventory manager

    def link_inventory_manager(self, inventory_manager):
        """Link the InventoryManager to this Market instance."""
        self.inventory_manager = inventory_manager

    def update_prices(self):
        for product in self.prices:
            supply_demand_ratio = (self.demand[product] + 1) / (self.supply[product] + 1)
            price_change = min(max(0.9, supply_demand_ratio), 1.1)
            self.prices[product] = max(1, self.prices[product] * price_change)
            self.price_history[product].append(self.prices[product])

        self.time_history.append(datetime.now())
        self.chat_box.append_message("Market prices updated.")

    def simulate_trade(self):
        for product in self.prices:
            self.supply[product] = max(0, self.supply[product] + int(uniform(-50, 50)))
            self.demand[product] = max(0, self.demand[product] + int(uniform(-50, 50)))
            self.chat_box.append_message(f"{product}: Supply {self.supply[product]}, Demand {self.demand[product]}")

    def show_graph(self):
        """Display the market price graph."""
        self.stock_graph.display()

    def sell_product(self, product, amount, chat_box):
        try:
            amount = int(amount)
            if product not in self.prices:
                chat_box.append_message(f"{product} is not a valid product.")
                return
            if self.inventory_manager.get_inventory().get(product, 0) < amount:
                chat_box.append_message(f"Not enough {product} in inventory!")
                return

            total_price = amount * self.prices[product]
            self.inventory_manager.add_to_inventory(product, -amount)
            self.inventory_manager.add_to_inventory("Money", total_price)
            chat_box.append_message(f"Sold {amount} {product} for ${total_price:.2f}.")
        except ValueError:
            chat_box.append_message("Invalid amount entered for selling.")

    def get_state(self):
        return {
            "prices": self.prices,
            "price_history": self.price_history,
            "time_history": self.time_history,
            "supply": self.supply,
            "demand": self.demand,
        }

    def load_state(self, state):
        self.prices = state.get("prices", self.base_prices.copy())
        self.price_history = state.get("price_history", {key: [] for key in self.base_prices})
        self.time_history = state.get("time_history", [])
        self.supply = state.get("supply", {key: 1000 for key in self.base_prices})
        self.demand = state.get("demand", {key: 1000 for key in self.base_prices})
