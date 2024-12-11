from tkinter import Frame, IntVar, Label, Listbox, Scrollbar, Button, Entry, Toplevel, OptionMenu, StringVar
import os
from tkinter.ttk import Scale

from matplotlib.ft2font import HORIZONTAL

SAVE_FILE_PATH = "game_save.pkl"  # Adjust to your actual save file location


def setup_bounty_board(root, bot_manager, chat_box, market):
    bounty_frame = Frame(root, bg="lightyellow", width=400)
    bounty_frame.pack(side="right", fill="both", expand=False)

    Label(bounty_frame, text="Bounty Board", font=("Arial", 14), bg="lightyellow").pack(pady=5)

    bounty_listbox = Listbox(bounty_frame, height=20, bg="white")
    bounty_listbox.pack(pady=5, fill="both", expand=True)

    scrollbar = Scrollbar(bounty_frame, orient="vertical", command=bounty_listbox.yview)
    scrollbar.pack(side="right", fill="y")
    bounty_listbox.config(yscrollcommand=scrollbar.set)

    def fulfill_selected_bounty():
        """Handles fulfilling the selected bounty."""
        selected_index = bounty_listbox.curselection()
        if not selected_index:
            chat_box.append_message("No bounty selected!")
            return

        bounty = bot_manager.get_bounties()[selected_index[0]]
        if market.inventory_manager.get_inventory().get(bounty["product"], 0) < bounty["amount"]:
            chat_box.append_message(f"Not enough {bounty['product']} to fulfill this bounty!")
            return

        market.inventory_manager.remove_from_inventory(bounty["product"], bounty["amount"])
        market.inventory_manager.add_money(bounty["amount"] * bounty["price"])
        chat_box.append_message(f"Fulfilled bounty: {bounty['amount']} {bounty['product']} @ ${bounty['price']:.2f}")
        update_bounties()

    Button(bounty_frame, text="Fulfill Bounty", command=fulfill_selected_bounty).pack(pady=5)

    def update_bounties():
        """Updates the bounty board with new bounties."""
        bounty_listbox.delete(0, "end")
        bounties = bot_manager.get_bounties()
        for idx, bounty in enumerate(bounties):
            bounty_listbox.insert("end", f"{idx+1}: {bounty['amount']} {bounty['product']} @ ${bounty['price']:.2f}")

    def bounty_tick():
        """Independent timer for updating bounties."""
        bot_manager.generate_bounties()
        update_bounties()
        root.after(300 * 1000, bounty_tick)  # 300 ticks = 300 seconds at default tick speed

    bounty_tick()

def setup_inventory_ui(root, market):
    inventory_frame = Frame(root, bg="lightblue", width=300, height=200)
    inventory_frame.pack(side="top", anchor="nw", pady=10, padx=10)

    inventory_label = Label(inventory_frame, text="Inventory", font=("Arial", 14), bg="lightblue")
    inventory_label.pack(anchor="w", pady=5)

    items_label = Label(inventory_frame, text="", font=("Arial", 12), bg="lightblue", justify="left")
    items_label.pack(anchor="w", padx=10)

    def update_inventory_display(inventory):
        inventory_text = "\n".join([f"{item}: {amount}" for item, amount in inventory.items()])
        items_label.config(text=inventory_text)

    market.inventory_manager.set_update_callback(update_inventory_display)
    update_inventory_display(market.inventory_manager.get_inventory())

def setup_ui(root, chat_box, market, bot_manager, tower_manager):
    control_frame = Frame(root)
    control_frame.pack(side="left", fill="y")

    Label(control_frame, text="Processing Controls", font=("Arial", 14)).pack(pady=5)
    # Corrected process all button
    Button(control_frame, text="Process All Crude Oil", command=tower_manager.process_all).pack(pady=5)

    Label(control_frame, text="Enter Barrels to Process:").pack(pady=2)
    process_entry = Entry(control_frame)
    process_entry.pack(pady=5)
    Button(control_frame, text="Process", command=lambda: tower_manager.process_specific(process_entry.get())).pack(pady=5)

    Label(control_frame, text="Selling Controls", font=("Arial", 14)).pack(pady=5)
    for product in market.prices.keys():
        sell_frame = Frame(control_frame)
        sell_frame.pack(pady=5, fill="x")
        Label(sell_frame, text=f"Sell {product}:").pack(side="left")
        sell_entry = Entry(sell_frame, width=5)
        sell_entry.pack(side="left")
        Button(sell_frame, text="Sell", command=lambda p=product, e=sell_entry: market.sell_product(p, e.get(), chat_box)).pack(side="left")

    Button(control_frame, text="Sell All", command=lambda: market.sell_all(chat_box)).pack(pady=10)
    Button(control_frame, text="Show Market Chart", command=market.show_graph).pack(pady=10)

    Label(control_frame, text="Bounty Controls", font=("Arial", 14)).pack(pady=5)
    Button(control_frame, text="Fulfill Bounty", command=lambda: market.simulate_trade()).pack(pady=5)

def setup_options_menu(root, time_manager):
    def open_options():
        options_window = Toplevel(root)
        options_window.title("Options")
        options_window.geometry("300x400")

        # Window Size Options
        Label(options_window, text="Window Size:").pack(pady=5)
        size_var = StringVar(value="1024x768")
        OptionMenu(options_window, size_var, "800x600", "1024x768", "1280x720").pack(pady=5)

        def apply_settings():
            root.geometry(size_var.get())

        Button(options_window, text="Apply", command=apply_settings).pack(pady=10)

        # Delete Save Data
        def delete_save_data():
            if os.path.exists(SAVE_FILE_PATH):
                os.remove(SAVE_FILE_PATH)
                Label(options_window, text="Save data deleted!", fg="green").pack(pady=5)
            else:
                Label(options_window, text="No save data found!", fg="red").pack(pady=5)

        Button(options_window, text="Delete Save Data", command=delete_save_data).pack(pady=10)

        # Developer Menu
        Label(options_window, text="Developer Menu", font=("Arial", 14)).pack(pady=10)

        # Tick Speed Input Field
        Label(options_window, text="Enter Tick Speed Multiplier (x):").pack(pady=5)
        tick_speed_entry = Entry(options_window)
        tick_speed_entry.pack(pady=5)

        def apply_tick_speed():
            try:
                multiplier = float(tick_speed_entry.get())
                if multiplier > 0:
                    time_manager.set_speed(multiplier)
                    Label(options_window, text=f"Tick speed set to {multiplier}x", fg="green").pack(pady=5)
                else:
                    Label(options_window, text="Please enter a value greater than 0!", fg="red").pack(pady=5)
            except ValueError:
                Label(options_window, text="Invalid input! Enter a number.", fg="red").pack(pady=5)

        Button(options_window, text="Apply Tick Speed", command=apply_tick_speed).pack(pady=10)

    Button(root, text="Options", command=open_options).pack(side="top", pady=5)


def setup_tower_ui(root, tower_manager):
    tower_frame = Frame(root, bg="lightgreen", width=300, height=200)
    tower_frame.pack(side="top", anchor="nw", pady=10, padx=10)

    Label(tower_frame, text="Tower Status", font=("Arial", 14), bg="lightgreen").pack(anchor="w", pady=5)

    tower_labels = []

    for tower in tower_manager.towers:
        tower_label = Label(
            tower_frame,
            text=f"Tower {tower['id']}:\nAvailable\n0/80 barrels",
            font=("Arial", 12),
            bg="white"
        )
        tower_label.pack(anchor="w", padx=10, pady=5)
        tower_labels.append(tower_label)

    def update_tower_display():
        for idx, tower in enumerate(tower_manager.towers):
            if tower["processing"]:
                status = f"Processing, Time Left: {tower['timer']} ticks"
            else:
                status = "Available"
            tower_labels[idx].config(
                text=f"Tower {tower['id']}:\n{status}\n{tower['current']}/{tower['capacity']} barrels",
                bg="yellow" if tower["selected"] else "white"
            )
        root.after(1000, update_tower_display)

    update_tower_display()