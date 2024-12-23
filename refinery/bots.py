# bots.py
class Bot:
    def __init__(self, name, market):
        self.name = name
        self.inventory = {}
        self.money = 1000
        self.market = market

    def trade(self):
        for product, price in self.market.prices.items():
            if price > 0:
                if self.money >= price:
                    quantity = min(10, self.money // price)
                    self.money -= quantity * price
                    self.inventory[product] = self.inventory.get(product, 0) + quantity
                elif self.inventory.get(product, 0) > 0:
                    quantity = min(10, self.inventory[product])
                    self.money += quantity * price
                    self.inventory[product] -= quantity

class BotManager:
    def __init__(self, market, chat_box):
        self.bots = [Bot(f"Bot {i+1}", market) for i in range(200)]
        self.chat_box = chat_box
        self.bounties = []

    def update(self):
        for bot in self.bots:
            bot.trade()

    def generate_bounties(self):
        self.bounties = [
            {
                "product": "Diesel",
                "amount": 10,
                "price": 50.0
            }
            for _ in range(5)
        ]
        self.chat_box.append_message("Generated bounties: " + str(self.bounties))

    def get_bounties(self):
        return self.bounties

    def get_state(self):
        return [
            {
                "name": bot.name,
                "inventory": bot.inventory,
                "money": bot.money
            }
            for bot in self.bots
        ]

    def load_state(self, state):
        for bot, bot_data in zip(self.bots, state):
            bot.name = bot_data.get("name", bot.name)
            bot.inventory = bot_data.get("inventory", {})
            bot.money = bot_data.get("money", 1000)
