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
        self.tick_speed = 1000

    def set_tick_speed(self, speed_multiplier):
        """Adjust tower processing speed."""
        self.tick_speed = int(1000 / speed_multiplier)


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
        total_processed = 0

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
                total_processed += to_add

        self.inventory_manager.add_to_inventory("Crude Oil", -total_processed)
        self.chat_box.append_message(f"Processing {total_processed} barrels of Crude Oil across towers.")


    def process_specific(self, barrels):
        try:
            barrels = int(barrels)
            available_oil = self.inventory_manager.get_inventory().get("Crude Oil", 0)

            if barrels > available_oil:
                self.chat_box.append_message("Not enough Crude Oil in inventory!")
                return

            total_added = 0
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
                    total_added += to_add

            if total_added > 0:
                self.inventory_manager.add_to_inventory("Crude Oil", -total_added)
                self.chat_box.append_message(f"Processing {total_added} barrels of Crude Oil across towers.")
            else:
                self.chat_box.append_message("No available space in towers to process Crude Oil.")
        except ValueError:
            self.chat_box.append_message("Invalid number of barrels entered!")


    # Ensure purchased towers have correct capacity and default values, add chat message
    def add_tower(tower_manager, capacity=80):
        new_tower = {
            "id": len(tower_manager.towers) + 1,
            "current": 0,
            "capacity": capacity,
            "timer": 0,
            "selected": False,
            "processing": False
        }
        tower_manager.towers.append(new_tower)
        tower_manager.chat_box.append_message(f"New tower added. Total towers: {len(tower_manager.towers)}")

    # Updated buy_tower to ensure proper usage and resolve errors
    def buy_tower(tower_manager, capacity=80):
        tower_manager.add_tower(capacity)

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

    # Improved set_state implementation for TowerManager
    def set_state(tower_manager, state):
        """Load and validate the tower state."""
        tower_manager.towers.clear()
        for tower_data in state:
            tower = {
                "id": tower_data.get("id", len(tower_manager.towers) + 1),
                "current": tower_data.get("current", 0),
                "capacity": tower_data.get("capacity", 80),
                "timer": tower_data.get("timer", 0),
                "selected": tower_data.get("selected", False),
                "processing": tower_data.get("processing", False)
            }
            tower_manager.towers.append(tower)
        tower_manager.chat_box.append_message(f"State loaded successfully. Total towers: {len(tower_manager.towers)}")

    def load_state(self, state):
        self.towers = state
        self.chat_box.append_message("Towers restored from save.")

    def buy_tower(self, capacity=80):
        add_tower(self, capacity)
