# game_state.py
import pickle
import os

class GameState:
    def __init__(self, inventory_manager, tower_manager, bot_manager):
        self.inventory_manager = inventory_manager
        self.tower_manager = tower_manager
        self.bot_manager = bot_manager
        self.save_directory = "assets/saves"
        self.save_file = "game_save.pkl"

        # Create the save directory if it doesn't exist
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)

    def save(self):
        save_path = os.path.join(self.save_directory, self.save_file)
        state = {
            "inventory": self.inventory_manager.get_inventory(),
            "money": self.inventory_manager.money,
            "towers": self.tower_manager.get_state(),
            "bots": self.bot_manager.get_state()
        }
        try:
            with open(save_path, "wb") as f:
                pickle.dump(state, f)
        except Exception as e:
            print(f"Failed to save game state: {e}")

    def load(self):
        save_path = os.path.join(self.save_directory, self.save_file)
        try:
            with open(save_path, "rb") as f:
                state = pickle.load(f)
                self.inventory_manager.set_inventory(state["inventory"])
                self.inventory_manager.money = state["money"]
                self.tower_manager.set_state(state["towers"])
                self.bot_manager.load_state(state["bots"])
                return True
        except FileNotFoundError:
            print("Save file not found. Starting a new game.")
            return False
        except Exception as e:
            print(f"Failed to load game state: {e}")
            return False
