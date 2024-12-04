# time_manager.py
from time import time

class TimeManager:
    def __init__(self, root, time_label, inventory_manager):
        self.root = root
        self.time_label = time_label
        self.inventory_manager = inventory_manager
        self.start_time = time()

    def start(self):
        self.update_timer()
        self.root.after(10, self.tick)

    def tick(self):
        self.update_timer()
        self.root.after(10, self.tick)

    def update_timer(self):
        elapsed = 8 - (time() - self.start_time) % 8
        seconds = int(elapsed)
        milliseconds = int((elapsed - seconds) * 1000)
        self.time_label.config(text=f"Time: {seconds}.{milliseconds:03} seconds")

        if seconds == 0 and milliseconds == 0:
            self.inventory_manager.add_to_inventory("Crude Oil", 80)
