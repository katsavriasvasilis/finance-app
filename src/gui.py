import tkinter as tk
from src.db import init_db

def main():
    init_db()
    root = tk.Tk()
    root.title("Finance App")
    root.geometry("1024x576")

    # απλό label για δοκιμή
    lbl = tk.Label(root, text="Welcome to Finance-App", font=("Arial", 24))
    lbl.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
