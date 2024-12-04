# towers.py
class TowerManager:
    def __init__(self, chat_box):
        self.towers = [{"id": 1, "processing": False, "timer": 0, "capacity": 100}]
        self.chat_box = chat_box

    def process_all(self, barrels):
        processed = 0
        for tower in self.towers:
            if not tower["processing"] and barrels > 0:
                to_process = min(barrels, tower["capacity"])
                tower["processing"] = True
                tower["timer"] = to_process  # Simulate 1 second per barrel
                processed += to_process
                barrels -= to_process
                self.chat_box.append_message(f"Processing {to_process} barrels in Tower {tower['id']}")
        return processed

    def process_specific(self, barrels):
        try:
            barrels = int(barrels)
            if barrels <= 0:
                self.chat_box.append_message("Please enter a valid positive number of barrels.")
                return

            available = sum(1 for tower in self.towers if not tower["processing"])
            if available == 0:
                self.chat_box.append_message("No available towers to process crude oil.")
                return

            processed = self.process_all(barrels)
            if processed > 0:
                self.chat_box.append_message(f"Processing {processed} barrels across available towers.")
            else:
                self.chat_box.append_message("Not enough crude oil or towers to process the requested amount.")
        except ValueError:
            self.chat_box.append_message("Invalid input. Please enter a numeric value.")

    def add_tower(self):
        new_tower = {"id": len(self.towers) + 1, "processing": False, "timer": 0, "capacity": 100}
        self.towers.append(new_tower)
        self.chat_box.append_message(f"New tower added. Total towers: {len(self.towers)}")

    def update(self):
        completed = 0
        for tower in self.towers:
            if tower["processing"]:
                tower["timer"] -= 1
                if tower["timer"] <= 0:
                    tower["processing"] = False
                    completed += tower["capacity"]
                    self.chat_box.append_message(f"Tower {tower['id']} completed processing.")
        return completed

    def get_state(self):
        return [{"id": tower["id"], "processing": tower["processing"], "timer": tower["timer"], "capacity": tower["capacity"]} for tower in self.towers]

    def load_state(self, state):
        self.towers = state
        self.chat_box.append_message("Towers restored from save.")
