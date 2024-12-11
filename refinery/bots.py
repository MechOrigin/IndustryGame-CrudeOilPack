# bots.py
import random


class Bot:
    def __init__(self, name, market):
        self.name = name
        self.inventory = {}
        self.money = 1000  # Default starting money for each bot
        self.market = market

    def trade(self):
        if self.market:
            for product, price in self.market.prices.items():
                if random.random() > 0.5:  # Random chance to buy or sell
                    if random.random() > 0.5:  # Buy
                        amount = random.randint(1, 10)
                        cost = amount * price
                        if self.money >= cost:
                            self.inventory[product] = self.inventory.get(product, 0) + amount
                            self.money -= cost
                    else:  # Sell
                        amount = random.randint(1, 10)
                        if self.inventory.get(product, 0) >= amount:
                            revenue = amount * price
                            self.inventory[product] -= amount
                            self.money += revenue

    def generate_bounty(self):
        """Generate a single bounty for this bot."""
        if self.market:
            product = random.choice(list(self.market.prices.keys()))
            amount = random.randint(10, 50)
            price = round(self.market.prices[product] * (1 + random.uniform(-0.2, 0.2)), 3)
            return {"product": product, "amount": amount, "price": price}
        return None


class BotManager:
    def __init__(self, market, chat_box):
        self.bots = [Bot(f"Bot {i+1}", market) for i in range(25)]
        self.chat_box = chat_box
        self.bounties = []  # Centralized list of bounties

    def update(self):
        """Update all bots to trade."""
        for bot in self.bots:
            bot.trade()

    def generate_bounties(self):
        """Generate a new set of centralized bounties."""
        products = list(self.bots[0].market.prices.keys()) if self.bots else []
        if not products:
            self.chat_box.append_message("No products available in the market for bounties!")
            return

        self.bounties = [
            {
                "product": random.choice(products),
                "amount": random.randint(10, 100),
                "price": round(random.uniform(0.8, 1.2) * random.choice([self.bots[0].market.prices[p] for p in products]), 2),
            }
            for _ in range(5)
        ]
        self.chat_box.append_message("Bounties updated!")

    def get_bounties(self):
        """Retrieve current bounties."""
        return self.bounties

    def get_state(self):
        """Get the current state of all bots."""
        return [
            {
                "name": bot.name,
                "inventory": bot.inventory,
                "money": bot.money
            }
            for bot in self.bots
        ]

    def load_state(self, state):
        """Load a saved state for all bots."""
        self.bots = []
        for bot_data in state:
            bot = Bot(bot_data["name"], None)  # Market reference can be set after initialization
            bot.inventory = bot_data["inventory"]
            bot.money = bot_data["money"]
            self.bots.append(bot)
