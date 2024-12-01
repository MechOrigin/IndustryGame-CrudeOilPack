import tkinter as tk
from tkinter import messagebox
from random import randint

class RefineryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Crude Oil Refinery Game")
        self.crude_oil = 80
        self.products = {"Gasoline": 0, "Diesel": 0, "Light Hydrocarbons": 0}
        self.money = 1000
        self.time_remaining = 8  # Hours until the next crude delivery

        # UI Elements
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Crude Oil Refinery", font=("Arial", 18)).pack(pady=10)

        # Status
        self.status_label = tk.Label(self.root, text=self.get_status(), font=("Arial", 14))
        self.status_label.pack(pady=10)

        # Buttons
        tk.Button(self.root, text="Process Crude Oil", command=self.process_crude).pack(pady=5)
        tk.Button(self.root, text="Sell Products", command=self.sell_products).pack(pady=5)
        tk.Button(self.root, text="Advance Time", command=self.advance_time).pack(pady=5)

    def get_status(self):
        return (f"Crude Oil: {self.crude_oil} barrels\n"
                f"Products: {self.products}\n"
                f"Money: ${self.money}\n"
                f"Next Delivery in: {self.time_remaining} hours")

    def process_crude(self):
        if self.crude_oil > 0:
            self.crude_oil -= 10
            self.products["Gasoline"] += randint(5, 10)
            self.products["Diesel"] += randint(3, 7)
            self.products["Light Hydrocarbons"] += randint(2, 5)
            messagebox.showinfo("Processing", "Crude oil processed into products!")
        else:
            messagebox.showwarning("Error", "No crude oil available to process.")
        self.update_status()

    def sell_products(self):
        total_earnings = sum(self.products.values()) * 5  # Example price per unit
        self.money += total_earnings
        for key in self.products:
            self.products[key] = 0
        messagebox.showinfo("Sales", f"Products sold for ${total_earnings}!")
        self.update_status()

    def advance_time(self):
        self.time_remaining -= 1
        if self.time_remaining <= 0:
            self.crude_oil += 80
            self.time_remaining = 8
            messagebox.showinfo("Delivery", "80 barrels of crude oil delivered!")
        self.update_status()

    def update_status(self):
        self.status_label.config(text=self.get_status())

# Run the game
root = tk.Tk()
game = RefineryGame(root)
root.mainloop()
