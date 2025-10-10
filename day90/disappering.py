import tkinter as tk
from tkinter import messagebox
import time

class DangerousWritingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("The Most Dangerous Writing App 🕒")
        self.root.geometry("700x500")
        self.root.configure(bg="#1e1e1e")

        self.label = tk.Label(
            root, text="Start typing... Don't stop or everything will be lost!",
            font=("Helvetica", 14), bg="#1e1e1e", fg="white"
        )
        self.label.pack(pady=10)

        self.text = tk.Text(root, wrap="word", font=("Consolas", 14), bg="#2e2e2e", fg="white")
        self.text.pack(expand=True, fill="both", padx=20, pady=10)

        self.text.bind("<Key>", self.reset_timer)

        self.timeout = 5  # seconds
        self.last_key_time = time.time()

        self.check_timer()

    def reset_timer(self, event=None):
        self.last_key_time = time.time()

    def check_timer(self):
        elapsed = time.time() - self.last_key_time
        if elapsed > self.timeout:
            self.text.delete("1.0", tk.END)
            messagebox.showwarning("Time’s Up!", "You stopped typing. All progress is lost!")
            self.last_key_time = time.time()  # reset after clearing

        self.root.after(1000, self.check_timer)  # check every 1 second


if __name__ == "__main__":
    root = tk.Tk()
    app = DangerousWritingApp(root)
    root.mainloop()
