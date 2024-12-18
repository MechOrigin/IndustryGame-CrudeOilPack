from datetime import datetime
from refinery.stock_graph import StockGraph
import matplotlib
import logging
import random

# Suppress matplotlib debug logs
matplotlib_logger = logging.getLogger('matplotlib')
matplotlib_logger.setLevel(logging.WARNING)

class MarketBot:
    def __init__(self, id, money=10000):
        self.id = id
        self.money = money
        self.inventory = {
            "Diesel": 100,
            "Gasoline": 100,
            "Light Hydrocarbons": 100,
            "Crude Oil": 100,
        }

    def trade(self, market_prices):
        """Simulates the bot's trading based on supply and demand."""
        for product, price in market_prices.items():
            if price > 0:  # Prevent trading at non-positive prices
                # Selling logic
                if self.inventory[product] > 10:  # Ensure enough inventory to sell
                    max_sell_quantity = min(10, self.inventory[product])
                    quantity = random.randint(1, max_sell_quantity)
                    self.inventory[product] -= quantity
                    self.money += quantity * price
                # Buying logic
                elif self.money >= price:  # Ensure sufficient funds to buy
                    max_buy_quantity = min(10, int(self.money / price))
                    if max_buy_quantity > 0:  # Ensure valid range for randint
                        quantity = random.randint(1, max_buy_quantity)
                        total_cost = quantity * price
                        self.inventory[product] += quantity
                        self.money -= total_cost


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
        self.bots = [MarketBot(i) for i in range(200)]
        self.player_influence = 0.33  # Player has 33% influence compared to bots

    def set_tick_speed(self, speed_multiplier):
        """Adjust market tick speed."""
        self.tick_speed = int(1000 / speed_multiplier)

    def update_prices(self, player_trades):
        """Simulates market updates with bots and player influence."""
        demand = {product: 0 for product in self.prices}
        supply = {product: 0 for product in self.prices}

        # Collect supply and demand from bots
        for bot in self.bots:
            bot.trade(self.prices)
            for product, quantity in bot.inventory.items():
                if bot.money > self.prices[product]:
                    demand[product] += quantity
                supply[product] += quantity

        # Incorporate player trades with a handicap
        for product, player_quantity in player_trades.items():
            if player_quantity > 0:  # Player buying
                demand[product] += player_quantity * self.player_influence
            else:  # Player selling
                supply[product] -= player_quantity * self.player_influence

        # Update prices based on supply and demand
        for product in self.prices:
            if supply[product] > demand[product]:
                self.prices[product] = max(0, self.prices[product] - 0.5)
            elif demand[product] > supply[product]:
                self.prices[product] += 0.5
            self.prices[product] = round(self.prices[product], 2)

        # Update price history
        self.time_history.append(datetime.now())
        for product in self.prices:
            self.price_history[product].append(self.prices[product])

        # Limit history to last 100 entries
        if len(self.time_history) > 100:
            self.time_history.pop(0)
            for product in self.price_history:
                self.price_history[product].pop(0)

    def show_graph(self):
        self.stock_graph.display(self.time_history, self.price_history)

    def sell_product(self, product, amount):
        try:
            amount = int(amount)
            if product not in self.prices:
                self.chat_box.append_message(f"{product} is not a valid product.")
                return
            if self.inventory_manager.get_inventory().get(product, 0) < amount:
                self.chat_box.append_message(f"Not enough {product} in inventory!")
                return

            total_price = amount * self.prices[product]
            self.inventory_manager.add_to_inventory(product, -amount)
            self.inventory_manager.add_to_inventory("Money", total_price)
            self.chat_box.append_message(f"Sold {amount} {product} for ${total_price:.2f}.")
        except ValueError:
            self.chat_box.append_message("Invalid amount entered for selling.")

    def sell_all(self):
        total_sold = 0
        for product, quantity in self.inventory_manager.get_inventory().items():
            if quantity > 0:
                price = self.prices.get(product, 0)
                self.inventory_manager.add_to_inventory(product, -quantity)
                self.inventory_manager.add_to_inventory("Money", quantity * price)
                total_sold += quantity * price
                self.chat_box.append_message(f"Sold {quantity} {product} for ${quantity * price:.2f}")

        if total_sold == 0:
            self.chat_box.append_message("No items to sell.")
        else:
            self.chat_box.append_message(f"Total earnings: ${total_sold:.2f}")
