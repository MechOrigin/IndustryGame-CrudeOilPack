# chat_box.py
from tkinter import Frame, Text, Scrollbar, END

class ChatBox:
    def __init__(self, root):
        self.frame = Frame(root)
        self.frame.pack(side="bottom", fill="both", expand=True)

        self.text_widget = Text(self.frame, wrap="word", state="normal", height=10)
        self.text_widget.pack(side="left", fill="both", expand=True)

        self.input_widget = Text(self.frame, wrap="word", height=2)
        self.input_widget.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(self.frame, orient="vertical", command=self.text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        self.text_widget["yscrollcommand"] = scrollbar.set

    def append_message(self, message):
        self.text_widget.insert(END, f"{message}\n")
        self.text_widget.see(END)

    def get_user_input(self):
        input_text = self.input_widget.get("1.0", "end").strip()
        self.input_widget.delete("1.0", "end")
        return input_text
