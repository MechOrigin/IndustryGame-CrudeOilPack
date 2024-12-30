# stock_graph.py
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import logging

logging.getLogger("matplotlib").setLevel(logging.WARNING)  # Suppress matplotlib debug logs

class StockGraph:
    def __init__(self, market):
        self.market = market

    def display(self, time_history, price_history):
        if not time_history or not any(price_history.values()):
            print("No market data available to display.")
            return

        fig, ax = plt.subplots()
        ax.set_title("Market Prices Over Time")
        ax.set_xlabel("Time")
        ax.set_ylabel("Prices")

        def update(frame):
            ax.clear()
            ax.set_title("Market Prices Over Time")
            ax.set_xlabel("Time")
            ax.set_ylabel("Prices")

            for product, prices in sorted(price_history.items()):
                if len(prices) > 0:
                    ax.plot(time_history, prices, label=product)
            ax.legend()

        ani = FuncAnimation(fig, update, interval=1000)
        plt.show()

    def save_graph(self, time_history, price_history, file_path="market_prices.png"):
        """Saves the current market trends as a static image."""
        if not time_history or not any(price_history.values()):
            print("No market data available to save.")
            return

        fig, ax = plt.subplots()
        ax.set_title("Market Prices Over Time")
        ax.set_xlabel("Time")
        ax.set_ylabel("Prices")

        for product, prices in sorted(price_history.items()):
            if len(prices) > 0:
                ax.plot(time_history, prices, label=product)
        ax.legend()

        fig.savefig(file_path)
        print(f"Market trends saved as {file_path}.")
