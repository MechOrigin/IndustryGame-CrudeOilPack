# time_manager.py
from tkinter import Label

class TimeManager:
    def __init__(self, root, inventory_manager, market, tower_manager):
        self.root = root
        self.inventory_manager = inventory_manager
        self.market = market
        self.tower_manager = tower_manager
        self.timer = 8  # Initialize with 300 ticks for a quarter
        self.tick_speed = 1000  # Default tick speed (1 second per tick)
        self.label = Label(root, text=f"Time Remaining: {self.timer} ticks", font=("Arial", 14))
        self.label.pack()

    def set_tick_speed(self, multiplier):
        self.tick_speed = int(1000 / multiplier)

    def start(self):
        self.schedule_tick()

    def schedule_tick(self):
        self.root.after(self.tick_speed, self.tick)

    def tick(self):
        try:
            if self.timer > 0:
                self.timer -= 1
                self.update_label()
                self.market.update_prices(self.inventory_manager.get_player_trades())
                self.tower_manager.update()
            else:
                self.end_quarter()
        except Exception as e:
            print(f"Error during tick: {e}")
        finally:
            self.schedule_tick()

    def update_label(self):
        self.label.config(text=f"Time Remaining: {self.timer} ticks")

    def end_quarter(self):
        """Handles end-of-quarter logic such as reporting and inventory restocking."""
        self.market.simulate_trade()
        self.inventory_manager.add_to_inventory("Crude Oil", 80)  # Example replenishment
        self.generate_quarterly_report()
        self.timer = 8  # Reset the timer for the next quarter

    def generate_quarterly_report(self):
        """Generates a quarterly performance report for the player."""
        inventory = self.inventory_manager.get_inventory()
        money = inventory.get("Money", 0)
        report = (
            f"Quarterly Report:\n"
            f"Remaining Money: ${money:.2f}\n"
            f"Inventory: {', '.join(f'{k}: {v}' for k, v in inventory.items() if k != 'Money')}\n"
        )
        print(report)

    def pause(self):
        """Pauses the timer by unscheduling the next tick."""
        self.root.after_cancel(self.schedule_tick)

    def resume(self):
        """Resumes the timer."""
        self.schedule_tick()
