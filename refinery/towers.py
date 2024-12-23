# towers.py
class TowerManager:
    def __init__(self, chat_box):
        self.chat_box = chat_box
        self.towers = [
            self._create_default_tower(i + 1)
            for i in range(3)
        ]
        self.inventory_manager = None

    def _create_default_tower(self, tower_id):
        """Creates a default tower structure."""
        return {
            "id": tower_id,
            "current": 0,
            "capacity": 80,
            "processing": False,
            "timer": 0
        }

    def link_inventory_manager(self, inventory_manager):
        """Links the inventory manager to allow interactions with inventory."""
        self.inventory_manager = inventory_manager

    def add_tower(self):
        new_tower = self._create_default_tower(len(self.towers) + 1)
        self.towers.append(new_tower)
        self.chat_box.append_message(f"Added new tower: Tower {new_tower['id']}")

    def process(self, tower_id, barrels):
        for tower in self.towers:
            if tower["id"] == tower_id:
                if tower["processing"]:
                    self.chat_box.append_message(f"Tower {tower_id} is already processing.")
                    return
                if barrels > tower["capacity"] - tower["current"]:
                    barrels = tower["capacity"] - tower["current"]
                if barrels <= 0:
                    self.chat_box.append_message(f"Tower {tower_id} cannot process zero barrels.")
                    return
                tower["current"] += barrels
                tower["processing"] = True
                tower["timer"] = 8
                self.chat_box.append_message(f"Tower {tower_id} started processing {barrels} barrels.")

    def process_all(self):
        """Processes all available crude oil in all towers."""
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

    def update(self):
        for tower in self.towers:
            if tower["processing"]:
                tower["timer"] -= 1
                if tower["timer"] <= 0:
                    tower["processing"] = False
                    processed = tower["current"]
                    tower["current"] = 0
                    if self.inventory_manager:
                        self.inventory_manager.add_to_inventory("Diesel", processed // 2)
                        self.inventory_manager.add_to_inventory("Gasoline", processed // 4)
                        self.inventory_manager.add_to_inventory("Light Hydrocarbons", processed // 4)
                    self.chat_box.append_message(f"Tower {tower['id']} completed processing {processed} barrels.")

    def distribute_outputs(self, processed):
        """Distributes processed barrels into multiple product categories."""
        products = {
            "Diesel": processed // 2,
            "Gasoline": processed // 4,
            "Light Hydrocarbons": processed // 4
        }
        return products

    def get_state(self):
        return [
            {
                "id": tower.get("id", i + 1),
                "current": tower.get("current", 0),
                "capacity": tower.get("capacity", 80),
                "processing": tower.get("processing", False),
                "timer": tower.get("timer", 0)
            }
            for i, tower in enumerate(self.towers)
        ]

    def set_state(self, state):
        self.towers = [
            self._create_default_tower(tower_data.get("id", i + 1)) | tower_data
            for i, tower_data in enumerate(state)
        ]
        self.chat_box.append_message("Towers state has been restored.")
