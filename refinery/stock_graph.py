import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# stock_graph.py
class StockGraph:
    def __init__(self, market):
        self.market = market

    def display(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title("Market Prices Over Time")
        ax.set_xlabel("Time")
        ax.set_ylabel("Price ($)")
        ax.grid()

        def update(frame):
            ax.clear()
            ax.set_title("Market Prices Over Time")
            ax.set_xlabel("Time")
            ax.set_ylabel("Price ($)")
            ax.grid()

            min_length = min(len(self.market.time_history), *[len(self.market.price_history[product]) for product in self.market.price_history])
            if min_length > 0:
                time_data = self.market.time_history[-min_length:]
                for product, prices in self.market.price_history.items():
                    ax.plot(time_data, prices[-min_length:], label=product)
                ax.legend(loc="upper left")

        ani = FuncAnimation(fig, update, interval=1000, cache_frame_data=False)
        plt.show()
