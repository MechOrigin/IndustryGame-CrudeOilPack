# main.py
from tkinter import Tk, Label
from refinery.bots import BotManager
from refinery.chat_box import ChatBox
from refinery.game_state import GameState
from refinery.inventory_manager import InventoryManager
from refinery.market import Market
from refinery.time_manager import TimeManager
from refinery.towers import TowerManager
from refinery.ui_components import setup_inventory_ui, setup_tower_ui, setup_ui, setup_bounty_board, setup_options_menu
from refinery.logger import get_logger
import logging

# Configure logging level globally
logging.getLogger('matplotlib').setLevel(logging.WARNING)

logger = get_logger()

def main():
    logger.info("Starting Crude Oil Refinery Game")
    try:
        root = Tk()
        root.title("Crude Oil Refinery Game")
        root.geometry("1024x768")

        chat_box = ChatBox(root)
        inventory_manager = InventoryManager()

        # Pass inventory_manager to the Market initialization
        market = Market(chat_box, inventory_manager)
        bot_manager = BotManager(market, chat_box)

        def update_market_prices():
            market.update_prices()
            root.after(1000, update_market_prices)

        update_market_prices()

        bot_manager = BotManager(market, chat_box)
        tower_manager = TowerManager(chat_box)
        tower_manager.link_inventory_manager(inventory_manager)


        # Updated to match GameState definition
        game_state = GameState(inventory_manager, tower_manager, bot_manager)

        if not game_state.load():
            chat_box.append_message("No save data found. Starting a new game!")

        time_label = Label(root, text="Time Remaining: 8 ticks", font=("Arial", 14))
        time_label.pack()
        time_manager = TimeManager(root, time_label, inventory_manager, market, tower_manager)
        time_manager.start()

        setup_inventory_ui(root, market)
        setup_tower_ui(root, tower_manager)
        setup_ui(root, chat_box, market, bot_manager, tower_manager)
        setup_bounty_board(root, bot_manager, chat_box, market)
        setup_options_menu(root, time_manager)

        def update_towers():
            tower_manager.update()
            root.after(1000, update_towers)

        update_towers()

        def save_periodically():
            game_state.save()
            chat_box.append_message("Game saved.")
            logger.info("Game state saved.")
            root.after(60000, save_periodically)

        save_periodically()
        root.mainloop()

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()
