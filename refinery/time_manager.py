from refinery import market
from refinery.towers import TowerManager

class TimeManager:
    def __init__(self, root, time_label, inventory_manager, market, tower_manager):
        self.root = root
        self.time_label = time_label
        self.inventory_manager = inventory_manager
        self.market = market
        self.tower_manager = tower_manager
        self.timer = 8  # Start at 8 ticks
        self.tick_speed = 1000  # Default 1 second per tick

    def set_speed(self, speed_multiplier):
        self.tick_speed = int(1000 / speed_multiplier)  # Adjust tick speed based on multiplier
        self.market.set_tick_speed(speed_multiplier)
        self.tower_manager.set_tick_speed(speed_multiplier)

    def start(self):
        self.update_timer()
        self.root.after(self.tick_speed, self.tick)  # Trigger based on tick speed

    def tick(self):
        try:
            if self.timer > 0:
                self.timer -= 1
            else:
                self.inventory_manager.add_to_inventory("Crude Oil", 80)
                self.timer = 8  # Reset the timer after shipment

            self.update_timer()
            self.tower_manager.update()

            # Fetch player trades safely
            player_trades = (self.inventory_manager.get_player_trades()
                            if hasattr(self.inventory_manager, 'get_player_trades') else {})
            self.market.update_prices(player_trades)

        except Exception as e:
            print(f"Error in tick: {e}")

        # Schedule the next tick at the end of the method
        self.root.after(self.tick_speed, self.tick)


    def update_timer(self):
        self.time_label.config(text=f"Time Remaining: {self.timer} ticks")
