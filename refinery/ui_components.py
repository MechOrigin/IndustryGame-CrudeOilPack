from tkinter import Frame, Button, Entry, Label
from tkinter import Frame, Label, Listbox, Scrollbar, Button

def setup_bounty_board(root, bot_manager, chat_box, market):
    bounty_frame = Frame(root, bg="lightyellow", width=300)
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

    def fulfill_bounty():
        selection = bounty_listbox.curselection()
        if selection:
            idx = selection[0]
            bounties = bot_manager.get_bounties()
            selected_bounty = bounties[idx]
            product = selected_bounty["product"]
            amount = selected_bounty["amount"]
            price = selected_bounty["price"]

            chat_box.append_message(f"Fulfilling bounty: {amount} {product} @ ${price}. Confirm (y/n)?")
            if chat_box.get_confirmation(f"Fulfill {amount} {product} @ ${price}?"):
                if market.fulfill_bounty(product, amount, price):
                    chat_box.append_message(f"Fulfilled bounty for {amount} {product} @ ${price}.")
                else:
                    chat_box.append_message(f"Failed to fulfill bounty: Not enough {product}.")

    Button(bounty_frame, text="Fulfill Bounty", command=fulfill_bounty).pack(pady=5)
    root.after(1000, update_bounties)


def setup_ui(root, chat_box, market, bot_manager, tower_manager):
    """
    Sets up the main UI for the game.
    """
    # Create main control frame
    control_frame = Frame(root)
    control_frame.pack(side="left", fill="y")

    # Add processing controls
    Label(control_frame, text="Processing Controls", font=("Arial", 14)).pack(pady=5)
    Button(control_frame, text="Process All Crude Oil", command=tower_manager.process_all).pack(pady=5)
    Label(control_frame, text="Enter Barrels to Process:").pack(pady=2)
    process_entry = Entry(control_frame)
    process_entry.pack(pady=5)
    Button(control_frame, text="Process", command=lambda: tower_manager.process_specific(process_entry.get())).pack(pady=5)

    # Add selling controls
    Label(control_frame, text="Selling Controls", font=("Arial", 14)).pack(pady=5)
    for product in market.base_prices.keys():
        sell_frame = Frame(control_frame)
        sell_frame.pack(pady=5, fill="x")
        Label(sell_frame, text=f"Sell {product}:").pack(side="left")
        sell_entry = Entry(sell_frame, width=5)
        sell_entry.pack(side="left")
        Button(sell_frame, text="Sell", command=lambda p=product, e=sell_entry: market.sell_product(p, e.get(), chat_box)).pack(side="left")

    Button(control_frame, text="Sell All", command=lambda: market.sell_all(chat_box)).pack(pady=10)

    # Add buttons for market graph
    Button(control_frame, text="Show Market Chart", command=market.show_graph).pack(pady=10)
