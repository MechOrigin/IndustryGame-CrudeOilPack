from tkinter import Text, Scrollbar, Frame, END, BOTH, VERTICAL

class ChatBox:
    def __init__(self, root):
        self.frame = Frame(root)
        self.frame.pack(side="bottom", fill="both", expand=True)

        self.text_widget = Text(self.frame, wrap="word", state="disabled", height=10)
        self.text_widget.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(self.frame, orient=VERTICAL, command=self.text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        self.text_widget["yscrollcommand"] = scrollbar.set

    def append_message(self, message):
        self.text_widget.config(state="normal")
        self.text_widget.insert(END, f"{message}\n")
        self.text_widget.see(END)
        self.text_widget.config(state="disabled")

    def get_confirmation(self, prompt):
        self.append_message(prompt)
        response = self.text_widget.get("1.0", END).strip().lower()
        return response in ["y", "yes"]
