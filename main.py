# Adjusted main.py imports and function calls to use UIComponents

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
        root = Tk()
        root.title("Crude Oil Refinery Game")
        root.geometry("1024x768")

        chat_box = ChatBox(root)
        inventory_manager = InventoryManager()
        market = Market(chat_box, inventory_manager)
        bot_manager = BotManager(market, chat_box)
        tower_manager = TowerManager(chat_box)
        tower_manager.link_inventory_manager(inventory_manager)

        game_state = GameState(inventory_manager, tower_manager, bot_manager)

        tower_labels = {}  # Dictionary to store tower labels
        tower_frame = Frame(root, bg="lightgreen", width=300, height=200)  # Tower frame
        tower_frame.pack(side="top", anchor="nw", pady=10, padx=10)
        
        # Load bot state
        if not game_state.load():
            chat_box.append_message("No save data found. Starting a new game!")
        else:
            try:
                bot_manager.load_state(game_state.bot_manager_state)
            except Exception as e:
                chat_box.append_message(f"Failed to load bot manager state: {e}")
                print(f"Bot manager state loading error: {e}")

        time_manager = TimeManager(root, inventory_manager, market, tower_manager)
        time_manager.start()

        UIComponents.setup_inventory_ui(root, inventory_manager)
        UIComponents.setup_tower_ui(root, tower_manager, market, tower_labels)
        # Call setup_ui with all required arguments
        UIComponents.setup_ui(root, chat_box, market, bot_manager, tower_manager, tower_frame, tower_labels)
        UIComponents.setup_bounty_board(root, bot_manager, chat_box, market)
        UIComponents.setup_options_menu(root, time_manager, inventory_manager)

        def save_periodically():
            game_state.save()
            chat_box.append_message("Game saved.")
            logger.info("Game state saved.")
            root.after(60000, save_periodically)

        save_periodically()

        # Define the update_towers function to include tower_labels
        def update_towers():
            tower_manager.update(tower_labels)  # Pass tower_labels to update
            root.after(1000, update_towers)

        # Call tower_manager.process_all with tower_labels in relevant UI logic
        def process_all_crude_oil():
            tower_manager.process_all(tower_labels)

        update_towers()

        root.mainloop()

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()
