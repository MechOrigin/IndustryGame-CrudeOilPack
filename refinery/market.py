# market.py
from datetime import datetime
from refinery.stock_graph import StockGraph
import matplotlib
import logging

# Suppress matplotlib debug logs
matplotlib_logger = logging.getLogger('matplotlib')
matplotlib_logger.setLevel(logging.WARNING)

class Market:
    def __init__(self, chat_box, inventory_manager):
        self.chat_box = chat_box
        self.inventory_manager = inventory_manager
        self.prices = {
            "Diesel": 10.5,
            "Gasoline": 8.75,
            "Light Hydrocarbons": 5.0,
            "Crude Oil": 3.0,
        }
        self.price_history = {product: [] for product in self.prices}
        self.time_history = []
        self.tick_speed = 1000
        self.stock_graph = StockGraph(self)

    def set_tick_speed(self, speed_multiplier):
        """Adjust market tick speed."""
        self.tick_speed = int(1000 / speed_multiplier)


    def update_prices(self):
        # Simulate price changes
        from random import uniform
        for product in self.prices:
            self.prices[product] += uniform(-0.5, 0.5)
            self.prices[product] = round(self.prices[product], 2)  # Keep prices rounded to 2 decimals

        self.time_history.append(datetime.now())
        for product in self.prices:
            self.price_history[product].append(self.prices[product])

        # Keep history limited to last 100 entries
        if len(self.time_history) > 100:
            self.time_history.pop(0)
            for product in self.price_history:
                self.price_history[product].pop(0)

    def show_graph(self):
        self.stock_graph.display(self.time_history, self.price_history)

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