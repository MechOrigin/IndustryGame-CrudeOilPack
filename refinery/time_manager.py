# time_manager.py
class TimeManager:
    def __init__(self, root, time_label, inventory_manager):
        self.root = root
        self.time_label = time_label
        self.inventory_manager = inventory_manager
        self.timer = 8  # Start at 8 ticks
        self.has_shipped = False

    def start(self):
        self.update_timer()
        self.root.after(1000, self.tick)  # Trigger every second

    def tick(self):
        if self.timer > 0:
            self.timer -= 1
        else:
            self.inventory_manager.add_to_inventory("Crude Oil", 80)
            self.timer = 8  # Reset the timer after shipment

        self.update_timer()
        self.root.after(1000, self.tick)

    def update_timer(self):
        self.time_label.config(text=f"Time Remaining: {self.timer} ticks")
