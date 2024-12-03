from time import time

class TimeManager:
    def __init__(self, root, time_label):
        self.root = root
        self.time_label = time_label
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
