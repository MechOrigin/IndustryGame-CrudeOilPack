class Tower:
    def __init__(self, id):
        self.id = id
        self.processing = False
        self.timer = 0
        self.capacity = 100  # Number of barrels per cycle
        self.barrels_processing = 0

    def process(self, barrels):
        if not self.processing:
            self.barrels_processing = min(barrels, self.capacity)
            self.timer = self.barrels_processing  # 1 second per barrel
            self.processing = True

    def update(self):
        if self.processing:
            self.timer -= 1
            if self.timer <= 0:
                self.processing = False
                return self.barrels_processing  # Return processed barrels
        return 0


class TowerManager:
    def __init__(self, chat_box):
        self.towers = [Tower(1)]
        self.chat_box = chat_box

    def add_tower(self):
        new_tower = Tower(len(self.towers) + 1)
        self.towers.append(new_tower)
        self.chat_box.append_message(f"New tower purchased! Total towers: {len(self.towers)}")

    def process_all(self, barrels):
        processed = 0
        for tower in self.towers:
            if not tower.processing and barrels > 0:
                tower.process(barrels)
                processed += tower.barrels_processing
                barrels -= tower.barrels_processing
        return processed

    def update(self):
        processed = 0
        for tower in self.towers:
            processed += tower.update()
        return processed

    def get_state(self):
        return [{"id": tower.id, "capacity": tower.capacity, "processing": tower.processing, "timer": tower.timer} for tower in self.towers]

    def load_state(self, state):
        self.towers = [Tower(data["id"]) for data in state]
        for tower, data in zip(self.towers, state):
            tower.capacity = data["capacity"]
            tower.processing = data["processing"]
            tower.timer = data["timer"]

    def verbose_status(self):
        status = "Towers:\n"
        for tower in self.towers:
            if tower.processing:
                status += f"Tower {tower.id}: {tower.barrels_processing} barrels in progress ({tower.timer} seconds remaining)\n"
            else:
                status += f"Tower {tower.id}: Idle\n"
        return status
