from tkinter import Frame, Label, Listbox, Scrollbar, Button, Entry, Toplevel, OptionMenu, StringVar

def setup_bounty_board(root, bot_manager, chat_box, market):
    bounty_frame = Frame(root, bg="lightyellow", width=400)
    bounty_frame.pack(side="right", fill="both", expand=False)

    Label(bounty_frame, text="Bounty Board", font=("Arial", 14), bg="lightyellow").pack(pady=5)

    bounty_listbox = Listbox(bounty_frame, height=20, bg="white")
    bounty_listbox.pack(pady=5, fill="both", expand=True)

    scrollbar = Scrollbar(bounty_frame, orient="vertical", command=bounty_listbox.yview)
    scrollbar.pack(side="right", fill="y")
    bounty_listbox.config(yscrollcommand=scrollbar.set)

    def update_bounties():
        bounty_listbox.delete(0, "end")
        bounties = bot_manager.get_bounties()
        for idx, bounty in enumerate(bounties):
            bounty_listbox.insert("end", f"{idx+1}: {bounty['amount']} {bounty['product']} @ ${bounty['price']}")
        root.after(1000, update_bounties)

    update_bounties()

    Button(bounty_frame, text="Fulfill Bounty", command=lambda: market.fulfill_bounty(chat_box)).pack(pady=5)

def setup_inventory_ui(root, market):
    # Create the inventory frame
    inventory_frame = Frame(root, bg="lightblue", width=600, height=300)
    inventory_frame.pack(side="top", fill="x", pady=10, padx=10)

    # Add title
    inventory_label = Label(inventory_frame, text="Inventory & Market Prices:", font=("Arial", 16), bg="lightblue")
    inventory_label.pack(anchor="w", pady=5)

    # Dynamic inventory display
    items_label = Label(inventory_frame, text="", font=("Arial", 14), bg="lightblue", justify="left")
    items_label.pack(anchor="w", padx=10)

    def update_inventory_display(inventory):
        """Update the inventory dynamically based on the current state."""
        inventory_text = "\n".join([f"{item}: {amount}" for item, amount in inventory.items()])
        items_label.config(text=inventory_text)

    # Link the inventory update callback to the market
    market.inventory_manager.set_update_callback(update_inventory_display)

    # Initial inventory display
    update_inventory_display(market.inventory_manager.inventory)

def setup_ui(root, chat_box, market, bot_manager, tower_manager):
    control_frame = Frame(root)
    control_frame.pack(side="left", fill="y")

    Label(control_frame, text="Processing Controls", font=("Arial", 14)).pack(pady=5)
    Button(control_frame, text="Process All Crude Oil", command=lambda: tower_manager.process_all(100)).pack(pady=5)

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

    Label(control_frame, text="Market Controls", font=("Arial", 14)).pack(pady=5)
    Button(control_frame, text="Show Market Chart", command=market.show_graph).pack(pady=10)

    Label(control_frame, text="Bounty Controls", font=("Arial", 14)).pack(pady=5)
    Button(control_frame, text="Fulfill Bounty", command=lambda: market.simulate_trade()).pack(pady=5)

def setup_options_menu(root):
    def open_options():
        options_window = Toplevel(root)
        options_window.title("Options")
        options_window.geometry("300x200")

        Label(options_window, text="Window Size:").pack(pady=5)
        size_var = StringVar(value="800x600")
        OptionMenu(options_window, size_var, "800x600", "1024x768", "1280x720").pack(pady=5)

        def apply_settings():
            root.geometry(size_var.get())

        Button(options_window, text="Apply", command=apply_settings).pack(pady=10)

    Button(root, text="Options", command=open_options).pack(side="top", pady=5)

def setup_tower_ui(root, tower_manager):
    tower_frame = Frame(root, bg="lightgreen", width=800, height=300)
    tower_frame.pack(side="top", fill="x", pady=10, padx=10)

    Label(tower_frame, text="Tower Status", font=("Arial", 16), bg="lightgreen").pack(anchor="w", pady=5)

    tower_labels = []

    # Create individual labels for each tower
    for tower in tower_manager.towers:
        tower_label = Label(
            tower_frame,
            text=f"Tower {tower['id']}: Available, Capacity: {tower['capacity']} barrels",
            font=("Arial", 14),
            bg="lightgreen",
            justify="left"
        )
        tower_label.pack(anchor="w", padx=10)
        tower_labels.append(tower_label)

    def update_tower_display():
        for idx, tower in enumerate(tower_manager.towers):
            if tower["processing"]:
                status = f"Processing, Time Left: {tower['timer']} ticks"
            else:
                status = "Available"
            tower_labels[idx].config(
                text=f"Tower {tower['id']}: {status}, Capacity: {tower['capacity']} barrels"
            )
        root.after(1000, update_tower_display)

    update_tower_display()