from tkinter import Tk
from tkinter.ttk import Frame
from refinery.bots import BotManager
from refinery.chat_box import ChatBox
from refinery.game_state import GameState
from refinery.inventory_manager import InventoryManager
from refinery.market import Market
from refinery.time_manager import TimeManager
from refinery.towers import TowerManager
from refinery.logger import get_logger
from refinery.ui_components import UIComponents

logger = get_logger()

def main():
    logger.info("Starting Crude Oil Refinery Game")
    try:
        # Initialize main window
        root = Tk()
        root.title("Crude Oil Refinery Game")
        root.geometry("1024x768")

        # Core components
        chat_box = ChatBox(root)
        inventory_manager = InventoryManager()
        market = Market(chat_box, inventory_manager)
        bot_manager = BotManager(market, chat_box)
        tower_manager = TowerManager(chat_box)
        tower_manager.link_inventory_manager(inventory_manager)

        game_state = GameState(inventory_manager, tower_manager, bot_manager)

        # Initialize tower_labels
        tower_labels = {}

        # Load game state
        if not game_state.load():
            chat_box.append_message("No save data found. Starting a new game!")

        time_manager = TimeManager(root, inventory_manager, market, tower_manager, tower_labels)
        time_manager.start()

        # UI setup
        UIComponents.setup_inventory_ui(root, inventory_manager)
        UIComponents.setup_tower_ui(root, tower_manager, market, tower_labels)
        UIComponents.setup_ui(root, chat_box, market, bot_manager, tower_manager, tower_labels)
        UIComponents.setup_bounty_board(root, bot_manager, chat_box, market)
        UIComponents.setup_options_menu(root, time_manager, inventory_manager)

        # Periodic save function
        def save_periodically():
            game_state.save()
            chat_box.append_message("Game saved.")
            logger.info("Game state saved.")
            root.after(60000, save_periodically)

        save_periodically()

        # Tower update loop
        def update_towers():
            tower_manager.update()
            root.after(1000, update_towers)

        update_towers()

        root.mainloop()

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()
