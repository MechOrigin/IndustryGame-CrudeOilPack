# towers.py


from tkinter.ttk import Label


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

    def add_tower(self, tower_labels, tower_inner_frame):
        if len(self.towers) >= 15:  # Max 15 towers
            self.chat_box.append_message("Maximum number of towers reached!")
            return

        new_tower = self._create_default_tower(len(self.towers) + 1)
        self.towers.append(new_tower)
        self.chat_box.append_message(f"Added new tower: Tower {new_tower['id']}")

        # Update GUI dynamically
        self._create_tower_label(new_tower, tower_labels, tower_inner_frame)

    def process(self, tower_id, barrels, label):
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
                label.config(
                    text=f"Tower {tower_id}\nStatus: Processing\nProcessing: {tower['current']}/{tower['capacity']} barrels\nTimer: {tower['timer']}",
                    bg="yellow"
                )
                self.chat_box.append_message(f"Tower {tower_id} started processing {barrels} barrels.")

    def process_all(self, tower_labels):
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

                # Update the corresponding label
                label = tower_labels[tower["id"]]
                label.config(
                    text=f"Tower {tower['id']}\nStatus: Processing\nProcessing: {tower['current']}/{tower['capacity']} barrels\nTimer: {tower['timer']}",
                    bg="yellow"
                )

        self.inventory_manager.add_to_inventory("Crude Oil", -total_processed)
        self.chat_box.append_message(f"Processing {total_processed} barrels of Crude Oil across towers.")


    def update(self, tower_labels):
        """Updates the processing status of all towers."""
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

                    # Update the corresponding label
                    label = tower_labels[tower["id"]]
                    label.config(
                        text=f"Tower {tower['id']}\nStatus: Available\nProcessing: 0/{tower['capacity']} barrels\nTimer: N/A",
                        bg="white"
                    )

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

    def _create_tower_label(self, tower, tower_labels, tower_inner_frame):
        """Creates a new tower label in the GUI."""
        label = Label(
            tower_inner_frame,
            text=f"Tower {tower['id']}\nStatus: Available\nProcessing: 0/{tower['capacity']} barrels\nTimer: N/A",
            font=("Arial", 10),
            bg="white",
            width=25,
            height=6,
            relief="solid",
            justify="center"
        )
        label.grid(row=(tower['id'] - 1) // 3, column=(tower['id'] - 1) % 3, padx=10, pady=10)
        tower_labels[tower["id"]] = label
