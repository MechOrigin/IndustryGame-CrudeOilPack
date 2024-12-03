# main.py
from tkinter import Tk, Label
from refinery.ui_components import setup_inventory_ui, setup_ui, setup_bounty_board
from refinery.time_manager import TimeManager
from refinery.market import Market
from refinery.bots import BotManager
from refinery.towers import TowerManager
from refinery.chat_box import ChatBox
from refinery.game_state import GameState
from refinery.inventory_manager import InventoryManager

def main():
    root = Tk()
    root.title("Crude Oil Refinery Game")

    # Initialize components
    chat_box = ChatBox(root)
    market = Market(chat_box)
    bot_manager = BotManager(market, chat_box)
    tower_manager = TowerManager(chat_box)
    game_state = GameState(market, tower_manager, bot_manager)

    # Load game state
    if not game_state.load():
        chat_box.append_message("New game started.")

    # Set up UI
    time_label = Label(root, text="Time: 07:59", font=("Arial", 14))
    time_label.pack()

    setup_ui(root, chat_box, market, bot_manager, tower_manager)
    setup_bounty_board(root, bot_manager, chat_box, market)
    # Initialize Inventory Manager
    inventory_manager = InventoryManager()

    # Set up inventory UI
    setup_inventory_ui(root, inventory_manager)

    # Time Manager
    time_manager = TimeManager(root, time_label)
    time_manager.start()

    # Save game periodically
    def save_periodically():
        game_state.save()
        chat_box.append_message("Game saved.")
        root.after(60000, save_periodically)  # Save every minute

    save_periodically()
    root.mainloop()

if __name__ == "__main__":
    main()
