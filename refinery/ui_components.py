# ui_components.py
from tkinter import Frame, Label, Listbox, Scrollbar, Button, Entry, Toplevel, OptionMenu, StringVar
import threading
import time

class UIComponents:
    @staticmethod
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
            bounty_listbox.delete(0, "end")
            bounties = bot_manager.get_bounties()
            for idx, bounty in enumerate(bounties):
                bounty_listbox.insert("end", f"{idx+1}: {bounty['amount']} {bounty['product']} @ ${bounty['price']:.2f}")

        def bounty_tick():
            bot_manager.generate_bounties()
            update_bounties()
            root.after(8 * 1000, bounty_tick)

        bounty_tick()

    @staticmethod
    def setup_tower_ui(tower_frame, tower_manager, market, tower_labels):
        Label(tower_frame, text="Towers", font=("Arial", 14), bg="lightgreen").pack(anchor="w", pady=5, padx=10)

        tower_frame = Frame(tower_frame, bg="lightgreen", width=300, height=200)
        tower_frame.pack(side="top", anchor="nw", pady=10, padx=10)

        def create_tower_label(tower):
            label = Label(
                tower_frame,
                text=f"Tower {tower['id']}\nStatus: Available\nProcessing: 0/{tower['capacity']} barrels\nTimer: N/A",
                font=("Arial", 10),
                bg="white",
                width=25,
                height=6,
                relief="solid",
                justify="center"
            )
            label.grid(row=(tower['id'] - 1) // 3, column=(tower['id'] - 1) % 3, padx=10, pady=10)
            tower_labels[tower["id"]] = label

        for tower in tower_manager.towers:
            create_tower_label(tower)

        def update_tower_labels():
            for tower_id, label in tower_labels.items():
                tower = next((t for t in tower_manager.towers if t["id"] == tower_id), None)
                if tower:
                    if tower["processing"]:
                        label.config(
                            text=f"Tower {tower['id']}\nStatus: Processing\nProcessing: {tower['current']}/{tower['capacity']} barrels\nTimer: {tower['timer']}",
                            bg="yellow"
                        )
                    else:
                        label.config(
                            text=f"Tower {tower['id']}\nStatus: Available\nProcessing: 0/{tower['capacity']} barrels\nTimer: N/A",
                            bg="white"
                        )

        tower_manager.update_tower_labels = update_tower_labels

    @staticmethod
    def create_fading_message(parent, text, color, duration=3000):
        message = Label(parent, text=text, fg=color, font=("Arial", 10))
        message.pack(anchor="n", pady=2)

        def fade():
            time.sleep(duration / 1000)
            message.destroy()

        threading.Thread(target=fade).start()

    @staticmethod
    def setup_upgrade_window(root, market, tower_manager):
        def open_upgrade_window():
            upgrade_window = Toplevel(root)
            upgrade_window.title("Upgrades")
            upgrade_window.geometry("400x400")

            Label(upgrade_window, text="Available Upgrades", font=("Arial", 14)).pack(pady=10)

            current_towers = len(tower_manager.towers)
            next_tower_price = 100 * (1.1 ** (current_towers - 3))

            def buy_tower():
                nonlocal next_tower_price
                current_money = market.inventory_manager.get_inventory().get("Money", 0)
                if current_towers >= 21:
                    UIComponents.create_fading_message(upgrade_window, "Maximum towers reached!", "red")
                    return

                if current_money >= next_tower_price:
                    tower_manager.add_tower()
                    market.inventory_manager.remove_from_inventory("Money", next_tower_price)
                    next_tower_price = round(next_tower_price * 1.1, 2)
                    UIComponents.create_fading_message(upgrade_window, f"Bought a new tower! Next price: ${next_tower_price:.2f}", "green")
                else:
                    UIComponents.create_fading_message(upgrade_window, "Not enough money!", "red")

            Label(upgrade_window, text=f"Next Tower Price: ${next_tower_price:.2f}", font=("Arial", 12)).pack(pady=5)
            Button(upgrade_window, text="Buy Tower", command=buy_tower).pack(pady=10)

            def upgrade_capacity():
                current_money = market.inventory_manager.get_inventory().get("Money", 0)
                upgrade_cost = 50
                if current_money >= upgrade_cost:
                    for tower in tower_manager.towers:
                        if tower["capacity"] < 200:
                            tower["capacity"] = min(tower["capacity"] + 10, 200)
                            market.inventory_manager.remove_from_inventory("Money", upgrade_cost)
                            UIComponents.create_fading_message(upgrade_window, "Upgraded tower capacity by +10 barrels!", "green")
                            break
                    else:
                        UIComponents.create_fading_message(upgrade_window, "All towers are at max capacity!", "red")
                else:
                    UIComponents.create_fading_message(upgrade_window, "Not enough money!", "red")

            Button(upgrade_window, text="Upgrade Capacity (+10 barrels)", command=upgrade_capacity).pack(pady=10)

        Button(root, text="Upgrades", command=open_upgrade_window).pack(side="top", anchor="ne", padx=10, pady=5)

    @staticmethod
    def setup_inventory_ui(root, inventory_manager):
        inventory_frame = Frame(root, bg="lightblue", width=300, height=200)
        inventory_frame.pack(side="top", anchor="nw", pady=10, padx=10)

        inventory_label = Label(inventory_frame, text="Inventory", font=("Arial", 14), bg="lightblue")
        inventory_label.pack(anchor="w", pady=5)

        items_label = Label(inventory_frame, text="", font=("Arial", 12), bg="lightblue", justify="left")
        items_label.pack(anchor="w", padx=10)

        def update_inventory_display(inventory):
            inventory_text = "\n".join([f"{item}: {amount}" for item, amount in inventory.items()])
            items_label.config(text=inventory_text)

        inventory_manager.set_update_callback(update_inventory_display)
        update_inventory_display(inventory_manager.get_inventory())

    @staticmethod
    def setup_ui(root, chat_box, market, bot_manager, tower_manager, tower_labels):
        control_frame = Frame(root)
        control_frame.pack(side="left", fill="y")

        Label(control_frame, text="Processing Controls", font=("Arial", 14)).pack(pady=5)
        Button(control_frame, text="Process All Crude Oil", command=lambda: tower_manager.process_all()).pack(pady=5)

        Label(control_frame, text="Selling Controls", font=("Arial", 14)).pack(pady=5)
        for product in market.prices.keys():
            sell_frame = Frame(control_frame)
            sell_frame.pack(pady=5, fill="x")
            Label(sell_frame, text=f"Sell {product}:").pack(side="left")
            sell_entry = Entry(sell_frame, width=5)
            sell_entry.pack(side="left")
            Button(sell_frame, text="Sell", command=lambda p=product, e=sell_entry: market.sell_product(p, e.get(), chat_box)).pack(side="left")

        Button(control_frame, text="Sell All", command=lambda: market.sell_all(chat_box)).pack(pady=10)
        UIComponents.setup_tower_ui(root, tower_manager, market, tower_labels)
        UIComponents.setup_upgrade_window(root, market, tower_manager)

    @staticmethod
    def setup_options_menu(root, time_manager, inventory_manager):
        def open_options():
            options_window = Toplevel(root)
            options_window.title("Options")
            options_window.geometry("300x400")

            Label(options_window, text="Window Size:").pack(pady=5)
            size_var = StringVar(value="1024x768")
            OptionMenu(options_window, size_var, "800x600", "1024x768", "1280x720").pack(pady=5)

            def apply_settings():
                root.geometry(size_var.get())
                print("Window size applied.")

            Button(options_window, text="Apply", command=apply_settings).pack(pady=10)

            Label(options_window, text="Tick Speed:").pack(pady=5)
            tick_speed_entry = Entry(options_window)
            tick_speed_entry.pack(pady=5)

            def apply_tick_speed():
                try:
                    multiplier = float(tick_speed_entry.get())
                    if multiplier > 0:
                        time_manager.set_tick_speed(multiplier)
                        print(f"Tick speed set to {multiplier}x.")
                    else:
                        print("Invalid tick speed value. Must be greater than 0.")
                except ValueError:
                    print("Invalid tick speed input.")

            Button(options_window, text="Apply Tick Speed", command=apply_tick_speed).pack(pady=10)

            Label(options_window, text="Reset Inventory:").pack(pady=5)

            def reset_inventory():
                inventory_manager.reset_inventory()
                print("Inventory reset.")

            Button(options_window, text="Reset Inventory", command=reset_inventory).pack(pady=10)

        Button(root, text="Options", command=open_options).pack(side="top", pady=5)
