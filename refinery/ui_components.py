from tkinter import Frame, IntVar, Label, Listbox, Scrollbar, Button, Entry, Toplevel, OptionMenu, StringVar
import os
from tkinter.ttk import Scale
import threading

from matplotlib.ft2font import HORIZONTAL

SAVE_FILE_PATH = "assets/saves/game_save.pkl"  # Adjust to your actual save file location

def setup_bounty_board(root, bot_manager, chat_box, market):
    bounty_frame = Frame(root, bg="lightyellow")
    bounty_frame.pack(side="right", fill="both", expand=True)

    Label(bounty_frame, text="Bounty Board", font=("Arial", 14), bg="lightyellow").pack(pady=5)

    bounty_listbox = Listbox(bounty_frame, height=30, bg="white")
    bounty_listbox.pack(pady=5, fill="both", expand=True)

    scrollbar = Scrollbar(bounty_frame, orient="vertical", command=bounty_listbox.yview)
    scrollbar.pack(side="right", fill="y")
    bounty_listbox.config(yscrollcommand=scrollbar.set)

    def fulfill_selected_bounty():
        selected_index = bounty_listbox.curselection()
        if not selected_index:
            chat_box.append_message("No bounty selected!")
            return

        bounty = bot_manager.get_bounties()[selected_index[0]]
        if market.inventory_manager.get_inventory().get(bounty["product"], 0) < bounty["amount"]:
            chat_box.append_message(f"Not enough {bounty['product']} to fulfill this bounty!")
            return

        market.inventory_manager.remove_from_inventory(bounty["product"], bounty["amount"])
        market.inventory_manager.add_to_inventory("Money", bounty["amount"] * bounty["price"])
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
    Button(root, text="Show Market Chart", command=market.show_graph).pack(anchor="ne", pady=10)

    Label(control_frame, text="Bounty Controls", font=("Arial", 14)).pack(pady=5)
    Button(control_frame, text="Fulfill Bounty", command=lambda: market.simulate_trade()).pack(pady=5)

def create_fading_message(parent, text, duration=4000):
    """Creates a message that fades out after a set duration."""
    message = Label(parent, text=text, fg="green", font=("Arial", 10))
    message.pack(anchor="n", pady=2)

    def fade():
        for alpha in range(100, 0, -5):
            hex_alpha = f"{alpha:02x}"  # Ensure two digits (e.g., '0f' for 15)
            message.config(fg=f"#00{hex_alpha}00")
            message.update()
            message.after(50)
        message.destroy()

    threading.Thread(target=lambda: [message.after(duration, fade)]).start()

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
            create_fading_message(options_window, "Settings applied successfully!")

        Button(options_window, text="Apply", command=apply_settings).pack(pady=10)

        # Delete Save Data
        def delete_save_data():
            create_fading_message(options_window, "Save data deleted!")

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
                    create_fading_message(options_window, f"Tick speed set to {multiplier}x")
                else:
                    create_fading_message(options_window, "Value must be greater than 0!", duration=2000)
            except ValueError:
                create_fading_message(options_window, "Invalid input!", duration=2000)

        Button(options_window, text="Apply Tick Speed", command=apply_tick_speed).pack(pady=10)

    Button(root, text="Options", command=open_options).pack(side="top", pady=5)

def setup_tower_ui(root, tower_manager):
    tower_frame = Frame(root, bg="lightgreen", width=300, height=200)
    tower_frame.pack(side="top", anchor="nw", pady=10, padx=10)

    Label(tower_frame, text="Tower Status", font=("Arial", 14), bg="lightgreen").pack(anchor="w", pady=5, padx=10)

    tower_labels = []
    tower_inner_frame = Frame(tower_frame, bg="lightgreen")
    tower_inner_frame.pack(anchor="w")

    def create_tower_label(tower):
        return Label(
            tower_inner_frame,
            text=f"Tower {tower['id']}:\nAvailable\n0/{tower['capacity']} barrels",
            font=("Arial", 12),
            bg="white"
        )

    def arrange_towers():
        for label in tower_labels:
            label.grid_forget()

        row = 0
        col = 0
        for idx, tower in enumerate(tower_manager.towers):
            if idx >= len(tower_labels):
                tower_label = create_tower_label(tower)
                tower_labels.append(tower_label)
            else:
                tower_label = tower_labels[idx]

            # Ensure 'current' and other keys are present in the tower dictionary
            current = tower.get("current", 0)
            capacity = tower.get("capacity", 80)  # Default capacity is 80 unless specified
            timer = tower.get("timer", "N/A")
            selected = tower.get("selected", False)
            processing = tower.get("processing", False)

            if processing:
                status = f"{timer} ticks"
            else:
                status = "Available"

            tower_label.config(
                text=f"Tower {tower['id']}:\n{status}\n{current}/{capacity} barrels",
                bg="yellow" if selected else "white"
            )
            tower_label.grid(row=row, column=col, padx=10, pady=5)
            row += 1
            if row >= 3:
                row = 0
                col += 1

    def update_tower_display():
        try:
            arrange_towers()
        except IndexError as e:
            print(f"Error updating tower display: {e}")

        root.after(1000, update_tower_display)

    update_tower_display()

def setup_upgrade_window(root, tower_manager, inventory_manager):
    def open_upgrade_window():
        upgrade_window = Toplevel(root)
        upgrade_window.title("Upgrades")
        upgrade_window.geometry("400x300")

        Label(upgrade_window, text="Available Upgrades", font=("Arial", 14)).pack(pady=10)

        current_towers = len(tower_manager.towers)
        next_tower_price = 100 * (1.1 ** (current_towers - 3))  # Exponential price increase

        def buy_tower():
            nonlocal next_tower_price
            if current_towers >= 18:
                create_fading_message(upgrade_window, "Maximum towers reached!", duration=2000)
                return

            if inventory_manager.money >= next_tower_price:
                inventory_manager.add_to_inventory("Money", -next_tower_price)
                tower_manager.add_tower()
                next_tower_price *= 1.1
                create_fading_message(upgrade_window, f"Bought a new tower! Price for next: ${next_tower_price:.2f}")
            else:
                create_fading_message(upgrade_window, "Not enough money!", duration=2000)

        Button(upgrade_window, text="Buy Tower", command=buy_tower).pack(pady=10)

    Button(root, text="Upgrades", command=open_upgrade_window).place(relx=0.95, rely=0.05, anchor="ne")

def setup_scalable_gui(root):
    def on_resize(event):
        for child in root.winfo_children():
            if isinstance(child, Frame):
                child.configure(width=event.width, height=event.height)

    root.bind("<Configure>", on_resize)