# towers.py
class TowerManager:
    def __init__(self, chat_box):
        self.towers = [{"id": i + 1, "processing": False, "timer": 0, "capacity": 80} for i in range(3)]
        self.chat_box = chat_box
        self.inventory_manager = None

    def link_inventory_manager(self, inventory_manager):
        self.inventory_manager = inventory_manager

    def process_all(self):
        for tower in self.towers:
            if not tower["processing"]:
                tower["processing"] = True
                tower["timer"] = 8  # Takes 8 ticks to process
                self.chat_box.append_message(f"Tower {tower['id']} started processing.")


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
        for tower in self.towers:
            if tower["processing"]:
                tower["timer"] -= 1
                if tower["timer"] <= 0:
                    tower["processing"] = False
                    self.inventory_manager.add_to_inventory("Diesel", 40)
                    self.inventory_manager.add_to_inventory("Gasoline", 20)
                    self.inventory_manager.add_to_inventory("Light Hydrocarbons", 20)
                    self.chat_box.append_message(f"Tower {tower['id']} completed processing.")

    def get_state(self):
        return [{"id": tower["id"], "processing": tower["processing"], "timer": tower["timer"], "capacity": tower["capacity"]} for tower in self.towers]

    def load_state(self, state):
        self.towers = state
        self.chat_box.append_message("Towers restored from save.")
