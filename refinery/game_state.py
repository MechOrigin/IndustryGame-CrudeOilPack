# game_state.py
import pickle
import os
from refinery.save_manager import SaveManager

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
        SaveManager.save(self.save_path, state)

    def load(self):
        state = SaveManager.load(self.save_path)
        if state:
            self.market.load_state(state.get("market", {}))
            self.tower_manager.load_state(state.get("towers", []))
            self.bot_manager.load_state(state.get("bots", []))
            return True
        return False
