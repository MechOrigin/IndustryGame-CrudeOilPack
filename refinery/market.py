import datetime
import random
from refinery.stock_graph import StockGraph

class Market:
    def __init__(self, chat_box):
        self.chat_box = chat_box
        self.base_prices = {"Gasoline": 5, "Diesel": 6, "Light Hydrocarbons": 4, "Crude Oil": 3}
        self.prices = self.base_prices.copy()
        self.price_history = {key: [] for key in self.base_prices}
        self.time_history = []
        self.stock_graph = StockGraph(self)

    def update_prices(self):
        for product in self.prices:
            self.prices[product] = max(1, self.base_prices[product] * (1 + random.uniform(-0.1, 0.1)))
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
