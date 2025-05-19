"""
GUI components με tkinter.
"""
import tkinter as tk
from tkinter import ttk

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Personal Finance Manager")
        self.geometry("1200x700")
        self.configure(bg="#222222")

        # —————— Αριστερό Navigation Panel ——————
        nav_frame = tk.Frame(self, bg="#333333", width=200)
        nav_frame.pack(side="left", fill="y")

        buttons = [
            ("Προεπισκόπηση",   "preview"),
            ("Συναλλαγές",      "transactions"),
            ("Κατηγορίες",      "categories"),
            ("Αναφορές",        "reports"),
            ("Ρυθμίσεις",       "settings")
        ]
        for (text, key) in buttons:
            btn = tk.Button(
                nav_frame, text=text, 
                font=("Arial", 12), fg="#000", bg="#dddddd",
                relief="flat", command=lambda k=key: self.show_frame(k)
            )
            btn.pack(fill="x", pady=5, padx=10)

        # —————— Δεξιά Content Area ——————
        container = tk.Frame(self, bg="#222222")
        container.pack(side="right", fill="both", expand=True)

        # Δημιουργούμε πέντε frames και τα τοποθετούμε το ένα πάνω στο άλλο
        self.frames = {}
        for key in ["preview","transactions","categories","reports","settings"]:
            frame = tk.Frame(container, bg="#222222")
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.frames[key] = frame

        # —————— Προεπισκόπηση ——————
        pv = self.frames["preview"]
        self.preview_balance = tk.Label(
            pv, text="Διαθέσιμο Υπόλοιπο: 0€",
            bg="#d3d3d3", font=("Arial", 14)
        )
        self.preview_balance.pack(pady=(50,10))
        self.preview_income = tk.Label(
            pv, text="Εισόδημα: 0€",
            bg="#d3d3d3", font=("Arial", 14)
        )
        self.preview_income.pack()

        # TODO: Canvas με πίτα (matplotlib/Canvas)

        # —————— Συναλλαγές ——————
        tx = self.frames["transactions"]
        tk.Label(tx, text="Προσθέστε Συναλλαγή:", fg="white", bg="#222222", font=("Arial",16)).pack(pady=20)
        form = tk.Frame(tx, bg="#222222")
        form.pack(pady=10)
        # Ημερομηνία
        tk.Label(form, text="Ημερομηνία:", fg="white", bg="#222222").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.tx_date = tk.Entry(form); self.tx_date.grid(row=0, column=1, padx=5, pady=5)
        # Κατηγορία
        tk.Label(form, text="Κατηγορία:", fg="white", bg="#222222").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.tx_category = tk.Entry(form); self.tx_category.grid(row=1, column=1, padx=5, pady=5)
        # Ποσό
        tk.Label(form, text="Ποσό:", fg="white", bg="#222222").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.tx_amount = tk.Entry(form); self.tx_amount.grid(row=2, column=1, padx=5, pady=5)
        # Επαναλαμβανόμενη
        self.tx_recurring = tk.BooleanVar()
        tk.Checkbutton(
            tx, text="Σημειώστε την ως επαναλαμβανόμενη συναλλαγή",
            variable=self.tx_recurring, fg="white", bg="#222222"
        ).pack(pady=10)
        tk.Button(tx, text="Προσθήκη", font=("Arial",18), bg="#2a7f97", fg="white").pack(pady=20)

        # —————— Κατηγορίες ——————
        cat = self.frames["categories"]
        # (εδώ μπορείς να επικολλήσεις τον κώδικα της φόρμας CRUD κατηγοριών που είχες ήδη)
        # π.χ. listbox, entry, combobox, checkbutton, buttons

        # —————— Αναφορές ——————
        rep = self.frames["reports"]
        tk.Label(rep, text="Αναφορές", fg="white", bg="#222222", font=("Arial",20)).pack(pady=20)
        # TODO: Ενσωμάτωση matplotlib bar chart

        # —————— Ρυθμίσεις ——————
        sett = self.frames["settings"]
        tk.Label(sett, text="Ρυθμίσεις", fg="white", bg="#222222", font=("Arial",20)).pack(pady=20)
        # TODO: Ρυθμίσεις export, defaults κλπ.

        # Εμφάνιση πρώτης οθόνης
        self.show_frame("preview")

    def show_frame(self, key: str):
        """Φέρνει μπροστά το frame με κλειδί key."""
        frame = self.frames[key]
        frame.tkraise()
