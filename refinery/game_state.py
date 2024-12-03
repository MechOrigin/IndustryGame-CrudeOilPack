import pickle
import os

class GameState:
    def __init__(self, market, tower_manager, bot_manager):
        self.market = market
        self.tower_manager = tower_manager
        self.bot_manager = bot_manager
        self.save_path = "assets/saves/game_state.pkl"

    def save(self):
        state = {
            "market": self.market.get_state(),
            "towers": self.tower_manager.get_state(),
            "bots": self.bot_manager.get_state(),
        }
        with open(self.save_path, "wb") as file:
            pickle.dump(state, file)

    def load(self):
        if os.path.exists(self.save_path):
            with open(self.save_path, "rb") as file:
                state = pickle.load(file)
                self.market.load_state(state["market"])
                self.tower_manager.load_state(state["towers"])
                self.bot_manager.load_state(state["bots"])
                return True
        return False
