# refinery/time_manager.py
class TimeManager:
    def __init__(self, root, market, bot_manager, game_state, tower_manager, time_label):
        self.root = root
        self.market = market
        self.bot_manager = bot_manager
        self.game_state = game_state
        self.tower_manager = tower_manager
        self.time_label = time_label  # Reference to the time label in the UI
        self.hour = 7
        self.minute = 59

    def start(self):
        self.update_time()
        self.root.after(1000, self.tick)

    def tick(self):
        self.minute -= 1
        if self.minute < 0:
            self.minute = 59
            self.hour -= 1
            if self.hour < 0:
                self.hour = 7  # Reset to 7 hours

        # Update market, bots, and towers
        self.market.update_prices()
        self.bot_manager.update()
        processed = self.tower_manager.update()
        if processed > 0:
            # Handle processed products (add to inventory, etc.)
            pass

        self.update_time()
        self.root.after(1000, self.tick)

    def update_time(self):
        time_display = f"Time: {self.hour:02}:{self.minute:02}"
        self.time_label.config(text=time_display)
