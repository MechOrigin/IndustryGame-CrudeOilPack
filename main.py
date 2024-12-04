# main.py
from tkinter import Tk, Label
from refinery.bots import BotManager
from refinery.chat_box import ChatBox
from refinery.game_state import GameState
from refinery.inventory_manager import InventoryManager
from refinery.market import Market
from refinery.stock_graph import StockGraph
from refinery.time_manager import TimeManager
from refinery.towers import TowerManager
from refinery.ui_components import setup_inventory_ui, setup_ui, setup_bounty_board, setup_options_menu

def main():
    root = Tk()
    root.title("Crude Oil Refinery Game")
    root.geometry("1024x768")

    chat_box = ChatBox(root)
    inventory_manager = InventoryManager()
    market = Market(chat_box)
    market.link_inventory_manager(inventory_manager)

    bot_manager = BotManager(market, chat_box)
    tower_manager = TowerManager(chat_box)
    game_state = GameState(market, tower_manager, bot_manager)

    if not game_state.load():
        chat_box.append_message("New game started.")
    else:
        chat_box.append_message("Game state loaded.")

    time_label = Label(root, text="Time: 08.000 seconds", font=("Arial", 14))
    time_label.pack()
    time_manager = TimeManager(root, time_label, inventory_manager)
    time_manager.start()

    setup_inventory_ui(root, market)
    setup_ui(root, chat_box, market, bot_manager, tower_manager)
    setup_bounty_board(root, bot_manager, chat_box, market)
    setup_options_menu(root)

    def save_periodically():
        game_state.save()
        chat_box.append_message("Game saved.")
        root.after(60000, save_periodically)

    save_periodically()
    root.mainloop()

if __name__ == "__main__":
    main()
