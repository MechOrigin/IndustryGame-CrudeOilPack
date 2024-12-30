# market.py
from tkinter import Frame, IntVar, Label, Listbox, Scrollbar, Button, Entry, Toplevel, OptionMenu, StringVar
import threading
import random
from matplotlib import pyplot as plt
import logging

# Suppress matplotlib debug logs
logging.getLogger('matplotlib').setLevel(logging.WARNING)

class Market:
    def __init__(self, chat_box, inventory_manager):
        self.chat_box = chat_box
        self.inventory_manager = inventory_manager
        self.prices = {
            "Crude Oil": 3.0,
            "Diesel": 8.0,
            "Gas": 5.0,
            "Light Hydrocarbons": 6.0
        }
        self.bots = self.initialize_bots(200)
        self.price_history = {key: [] for key in self.prices}
        self.time_history = []
        self.graph_initialized = False
        self.fig = None
        self.ax = None
        self.external_supply = {key: 500 for key in self.prices}
        self.price_limits = {
            "Crude Oil": (0.0, 6.0),
            "Diesel": (5.0, 11.0),
            "Gas": (2.0, 8.0),
            "Light Hydrocarbons": (3.0, 9.0)
        }
        self.recent_sales = {key: 0 for key in self.prices}

    def initialize_bots(self, num_bots):
        bots = []
        materials = list(self.prices.keys())
        for i in range(num_bots):
            specialization = materials[i % len(materials)]
            inventory = {specialization: 1000, "Money": 1000}
            bots.append({"id": i, "inventory": inventory, "specialization": specialization})
        return bots

    def simulate_market(self):
        for bot in self.bots:
            specialization = bot["specialization"]
            price = self.prices[specialization]
            if random.random() < 0.5:
                if "Money" in bot["inventory"] and bot["inventory"].get("Money", 0) >= price:
                    quantity = random.randint(1, 10)
                    cost = quantity * price
                    if bot["inventory"]["Money"] >= cost:
                        bot["inventory"]["Money"] -= cost
                        bot["inventory"].setdefault(specialization, 0)
                        bot["inventory"][specialization] += quantity
                elif bot["inventory"].get(specialization, 0) > 0:
                    quantity = random.randint(1, 10)
                    revenue = quantity * price
                    bot["inventory"].setdefault("Money", 0)
                    bot["inventory"]["Money"] += revenue
                    bot["inventory"][specialization] -= quantity
                    self.recent_sales[specialization] += quantity

    def inject_resources(self):
        for product in self.external_supply:
            self.external_supply[product] += random.randint(50, 100)

    def adjust_prices(self):
        supply = {key: self.external_supply.get(key, 0) for key in self.prices}
        demand = {key: 0 for key in self.prices}

        control_price = random.uniform(0.66, 1.33)

        for bot in self.bots:
            specialization = bot["specialization"]
            supply[specialization] += bot["inventory"].get(specialization, 0)
            demand[specialization] += random.randint(100, 175)

        for product in self.recent_sales:
            demand[product] += self.recent_sales[product]

        for product in self.prices:
            if demand[product] > supply[product]:
                self.prices[product] = round(self.prices[product] * control_price, 3)
            elif supply[product] > demand[product]:
                self.prices[product] = round(self.prices[product] * control_price, 3)

        for product, (min_price, max_price) in self.price_limits.items():
            self.prices[product] = max(min(self.prices[product], max_price), min_price)

        self.recent_sales = {key: 0 for key in self.prices}
        self.time_history.append(len(self.time_history))
        for product in self.prices:
            self.price_history[product].append(self.prices[product])

    def show_graph(self):
        if not self.graph_initialized:
            self.fig, self.ax = plt.subplots(figsize=(10, 5))
            self.graph_initialized = True
            plt.ion()

        def on_close(event):
            self.graph_initialized = False

        self.fig.canvas.mpl_connect('close_event', on_close)

        self.ax.clear()
        for product, history in self.price_history.items():
            self.ax.plot(self.time_history, history, label=product)

        self.ax.set_title("Market Prices Over Time")
        self.ax.set_xlabel("Time (ticks)")
        self.ax.set_ylabel("Price")
        self.ax.legend()
        self.ax.grid()
        plt.show(block=False)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def sell_product(self, product, quantity, chat_box):
        quantity = int(quantity)
        if quantity <= 0:
            chat_box.append_message("Invalid quantity.")
            return

        if product not in self.prices:
            chat_box.append_message(f"{product} is not a valid product.")
            return

        inventory = self.inventory_manager.get_inventory()
        if inventory.get(product, 0) >= quantity:
            self.inventory_manager.remove_from_inventory(product, quantity)
            self.inventory_manager.add_to_inventory("Money", quantity * self.prices[product])
            self.recent_sales[product] += quantity
            chat_box.append_message(f"Sold {quantity} {product} for ${quantity * self.prices[product]:.2f}.")
        else:
            chat_box.append_message(f"Not enough {product} to sell.")

    def sell_all(self, chat_box):
        inventory = self.inventory_manager.get_inventory()
        for product, quantity in inventory.items():
            if product in self.prices and quantity > 0:
                price = self.prices[product]
                self.inventory_manager.remove_from_inventory(product, quantity)
                self.inventory_manager.add_to_inventory("Money", quantity * price)
                self.recent_sales[product] += quantity
                chat_box.append_message(f"Sold {quantity} {product} for ${quantity * price:.2f}.")

    def update_prices(self, *args):
        self.simulate_market()
        self.inject_resources()
        self.adjust_prices()
        self.chat_box.append_message(f"Updated market prices: {self.prices}")
        if self.graph_initialized:
            self.show_graph()

    def simulate_trade(self):
        self.simulate_market()
        self.inject_resources()
        self.adjust_prices()
        self.chat_box.append_message("Market trade cycle completed.")
