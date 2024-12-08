# towers.py
class TowerManager:
    def __init__(self, chat_box):
        # Initialize towers with all required keys
        self.towers = [
            {"id": i + 1, "processing": False, "timer": 0, "capacity": 80, "current": 0, "selected": False}
            for i in range(3)
        ]
        self.chat_box = chat_box
        self.inventory_manager = None

    def link_inventory_manager(self, inventory_manager):
        self.inventory_manager = inventory_manager

    def select_tower(self, tower_id):
        for tower in self.towers:
            tower["selected"] = tower["id"] == tower_id
        self.chat_box.append_message(f"Tower {tower_id} selected.")

    def process(self, tower_id, barrels):
        for tower in self.towers:
            if tower["id"] == tower_id:
                if tower["processing"]:
                    self.chat_box.append_message(f"Tower {tower_id} is already processing!")
                    return
                if barrels > tower["capacity"] - tower["current"]:
                    barrels = tower["capacity"] - tower["current"]
                if barrels <= 0:
                    self.chat_box.append_message(f"Tower {tower_id} has no available capacity!")
                    return
                tower["processing"] = True
                tower["timer"] = 8  # ticks to process
                tower["current"] += barrels
                self.chat_box.append_message(f"Tower {tower_id} started processing {barrels} barrels.")

    def process_all(self):
        crude_oil_balance = self.inventory_manager.get_inventory().get("Crude Oil", 0)
        if crude_oil_balance <= 0:
            self.chat_box.append_message("No Crude Oil available for processing!")
            return

        for tower in self.towers:
            if crude_oil_balance <= 0:
                break
            available_space = tower["capacity"] - tower["current"]
            to_add = min(available_space, crude_oil_balance)
            if to_add > 0:
                tower["current"] += to_add
                tower["processing"] = True
                tower["timer"] = 8
                crude_oil_balance -= to_add

        self.inventory_manager.add_to_inventory("Crude Oil", -crude_oil_balance)
        self.chat_box.append_message("Processing all Crude Oil across towers.")


    def process_specific(self, barrels):
        try:
            barrels = int(barrels)
            if self.inventory_manager.get_inventory().get("Crude Oil", 0) < barrels:
                self.chat_box.append_message("Not enough Crude Oil in inventory!")
                return

            for tower in self.towers:
                if barrels <= 0:
                    break
                available_space = tower["capacity"] - tower["current"]
                to_add = min(available_space, barrels)
                if to_add > 0:
                    tower["current"] += to_add
                    tower["processing"] = True
                    tower["timer"] = 8
                    barrels -= to_add

            self.inventory_manager.add_to_inventory("Crude Oil", -int(barrels))
            self.chat_box.append_message("Started processing barrels across towers.")
        except ValueError:
            self.chat_box.append_message("Invalid number of barrels entered!")


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
                    processed = tower["current"]
                    tower["current"] = 0
                    self.inventory_manager.add_to_inventory("Diesel", processed // 2)
                    self.inventory_manager.add_to_inventory("Gasoline", processed // 4)
                    self.inventory_manager.add_to_inventory("Light Hydrocarbons", processed // 4)
                    self.chat_box.append_message(f"Tower {tower['id']} completed processing.")


    def get_state(self):
        return [{"id": tower["id"], "processing": tower["processing"], "timer": tower["timer"], "capacity": tower["capacity"]} for tower in self.towers]

    def set_state(self, state):
        # Ensure state has all required keys
        for tower in state:
            tower.setdefault("current", 0)
            tower.setdefault("processing", False)
            tower.setdefault("timer", 0)
        self.towers = state

    def load_state(self, state):
        self.towers = state
        self.chat_box.append_message("Towers restored from save.")
