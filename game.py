import tkinter as tk
from tkinter import simpledialog, scrolledtext
import random
import matplotlib.pyplot as plt # type: ignore
from matplotlib.animation import FuncAnimation # type: ignore
from datetime import datetime

class Market:
    def __init__(self):
        self.base_prices = {"Gasoline": 5, "Diesel": 6, "Light Hydrocarbons": 4, "Crude Oil": 3}
        self.market_prices = self.base_prices.copy()
        self.price_history = {product: [] for product in self.base_prices}
        self.time_history = []

    def update_prices(self, bots, player_inventory):
        total_supply = {product: player_inventory.get(product, 0) for product in self.base_prices}
        total_demand = {product: 0 for product in self.base_prices}

        for bot in bots:
            for product in self.base_prices:
                total_supply[product] += bot.inventory.get(product, 0)
                total_demand[product] += random.randint(20, 50)

        for product in self.base_prices:
            demand = total_demand[product]
            supply = total_supply[product]
            self.market_prices[product] = round(max(1, self.base_prices[product] * (demand / max(supply, 1))), 3)

            self.price_history[product].append(self.market_prices[product])
        
        self.time_history.append(datetime.now())

    def plot_prices(self):
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

            min_length = min(len(self.time_history), *[len(prices) for prices in self.price_history.values()])
            if min_length > 0:
                time_data = self.time_history[-min_length:]
                for product, prices in self.price_history.items():
                    ax.plot(time_data, prices[-min_length:], label=product)
                ax.legend(loc="upper left")

        ani = FuncAnimation(fig, update, interval=1000, cache_frame_data=False)
        plt.show()


class Bot:
    def __init__(self, name):
        self.name = name
        self.inventory = {"Gasoline": 50, "Diesel": 50, "Light Hydrocarbons": 50, "Crude Oil": 50}
        self.money = 1000
        self.bounties = []

    def buy(self, market_prices):
        for product, price in market_prices.items():
            if random.random() > 0.5:  # Random chance to buy
                amount = random.randint(1, 10)
                cost = amount * price
                if self.money >= cost:
                    self.inventory[product] += amount
                    self.money -= cost

    def sell(self, market_prices):
        for product, price in market_prices.items():
            if random.random() > 0.5:  # Random chance to sell
                amount = random.randint(1, 10)
                if self.inventory[product] >= amount:
                    revenue = amount * price
                    self.inventory[product] -= amount
                    self.money += revenue

    def generate_bounties(self):
        products = ["Gasoline", "Diesel", "Light Hydrocarbons", "Crude Oil"]
        self.bounties = []
        for _ in range(random.randint(1, 3)):
            product = random.choice(products)
            amount = random.randint(10, 50)
            price = random.randint(1, 10)
            self.bounties.append({"product": product, "amount": amount, "price": price})


class RefineryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Crude Oil Refinery Game")
        self.crude_oil = 80
        self.products = {"Gasoline": 0, "Diesel": 0, "Light Hydrocarbons": 0, "Crude Oil": 80}
        self.money = 1000
        self.time_remaining = 8
        self.bots = [Bot(f"Bot {i}") for i in range(1, 6)]
        self.market = Market()

        self.setup_ui()
        self.update_time_and_market()

    def setup_ui(self):
        tk.Label(self.root, text="Crude Oil Refinery", font=("Arial", 18)).pack(pady=10)
        self.status_label = tk.Label(self.root, text=self.get_status(), font=("Arial", 14))
        self.status_label.pack(pady=10)

        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Buttons for processing and selling
        tk.Button(control_frame, text="Process Crude Oil", command=self.process_crude_prompt).pack(pady=5)
        tk.Button(control_frame, text="Sell Products", command=self.sell_products_prompt).pack(pady=5)
        tk.Button(control_frame, text="Show Market Graph", command=self.market.plot_prices).pack(pady=5)

        # Chat box for displaying messages
        self.chat_box = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=10, state='disabled')
        self.chat_box.pack(pady=10, fill=tk.BOTH, expand=True)

        # Bounty board
        self.bounty_board = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=10, state='disabled', bg="lightyellow")
        self.bounty_board.pack(side=tk.RIGHT, fill=tk.Y)
        self.update_bounty_board()

    def append_to_chat(self, message):
        self.chat_box.config(state='normal')
        self.chat_box.insert(tk.END, f"{message}\n")
        self.chat_box.see(tk.END)
        self.chat_box.config(state='disabled')

    def update_bounty_board(self):
        self.bounty_board.config(state='normal')
        self.bounty_board.delete(1.0, tk.END)
        for bot in self.bots:
            bot.generate_bounties()
            self.bounty_board.insert(tk.END, f"{bot.name} Bounties:\n")
            for bounty in bot.bounties:
                self.bounty_board.insert(tk.END, f"  - {bounty['amount']} {bounty['product']} @ ${bounty['price']}/unit\n")
        self.bounty_board.config(state='disabled')

    def get_status(self):
        return (f"Time Remaining: {self.time_remaining} seconds\n"
                f"Crude Oil: {self.crude_oil} barrels\n"
                f"Products: {self.products}\n"
                f"Money: ${self.money}\n"
                f"Market Prices: {self.market.market_prices}")

    def process_crude_prompt(self):
        amount = simpledialog.askinteger("Process Crude Oil", "Enter barrels to process (or 0 for all):", minvalue=0)
        if amount == 0 or amount > self.crude_oil:
            amount = self.crude_oil
        self.crude_oil -= amount
        self.products["Gasoline"] += amount * 0.4
        self.products["Diesel"] += amount * 0.35
        self.products["Light Hydrocarbons"] += amount * 0.25
        self.append_to_chat(f"Processed {amount} barrels of crude oil.")

    def sell_products_prompt(self):
        product = simpledialog.askstring("Sell Products", "Enter product to sell (Gasoline, Diesel, Light Hydrocarbons, Crude Oil):")
        if product not in self.products:
            self.append_to_chat("Invalid product.")
            return
        amount = simpledialog.askinteger("Sell Products", f"Enter amount of {product} to sell (or 0 for all):", minvalue=0)
        if amount == 0 or amount > self.products[product]:
            amount = self.products[product]
        self.products[product] -= amount
        revenue = amount * self.market.market_prices[product]
        self.money += revenue
        self.append_to_chat(f"Sold {amount} units of {product} for ${revenue:.2f}.")

    def update_time_and_market(self):
        self.time_remaining -= 1
        if self.time_remaining <= 0:
            self.time_remaining = 8
            self.crude_oil += 80
            self.append_to_chat("80 barrels of crude oil delivered!")

        self.simulate_market()
        self.update_status()
        self.root.after(1000, self.update_time_and_market)

    def simulate_market(self):
        for bot in self.bots:
            bot.buy(self.market.market_prices)
            bot.sell(self.market.market_prices)
        self.market.update_prices(self.bots, self.products)

    def update_status(self):
        self.status_label.config(text=self.get_status())


root = tk.Tk()
game = RefineryGame(root)
root.mainloop()
