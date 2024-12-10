# save_manager.py
import os
import pickle
from refinery.logger import get_logger

logger = get_logger()

class SaveManager:
    @staticmethod
    def save(path, state):
        try:
            with open(path, "wb") as file:
                pickle.dump(state, file)
            logger.info(f"Game state saved to {path}")
        except Exception as e:
            logger.error(f"Failed to save game state: {e}", exc_info=True)

    @staticmethod
    def load(path):
        try:
            if os.path.exists(path):
                with open(path, "rb") as file:
                    state = pickle.load(file)
                logger.info(f"Game state loaded from {path}")
                return state
            logger.warning(f"Save file not found at {path}")
        except Exception as e:
            logger.error(f"Failed to load game state: {e}", exc_info=True)
        return None

# TODO: Fix when closing the game, save loads the previous state and it's invalid causing crash; game wont load.