import tkinter as tk
from tkinter import ttk, font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Χρώματα & fonts
BG_DARK       = "#1F2937"
BG_NAV        = "#111827"
BG_PANEL      = "#374151"
FG_TEXT       = "#F9FAFB"
BTN_BG        = "#4B5563"
BTN_FG        = "#F9FAFB"
CRUD_BTN_BG   = "#3B82F6"
CRUD_BTN_FG   = "#FFFFFF"
ENTRY_BG      = "#4B5563"
ENTRY_FG      = "#F9FAFB"

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        # Styling combobox
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure(
            'Custom.TCombobox',
            fieldbackground=ENTRY_BG,
            background=ENTRY_BG,
            foreground=ENTRY_FG
        )

        self.title("Personal Finance Manager")
        self.geometry("1024x680")
        self.configure(bg=BG_DARK)

        # Fonts
        self.h1 = font.Font(family="Segoe UI", size=18, weight="bold")
        self.h2 = font.Font(family="Segoe UI", size=14, weight="bold")
        self.body = font.Font(family="Segoe UI", size=12)

        # Nav panel
        nav = tk.Frame(self, bg=BG_NAV, width=180)
        nav.pack(side="left", fill="y")
        items = [
            ("Προεπισκόπηση", "preview", "🔍"),
            ("Συναλλαγές", "transactions", "💰"),
            ("Κατηγορίες", "categories", "📁"),
            ("Αναφορές", "reports", "📊"),
            ("Ρυθμίσεις", "settings", "⚙️")
        ]
        for text, key, icon in items:
            btn = tk.Button(
                nav, text=f"{icon}  {text}", anchor="w",
                bg=BG_NAV, fg=FG_TEXT, font=self.body, bd=0,
                activebackground=BTN_BG, activeforeground=BTN_FG,
                command=lambda k=key: self.show_frame(k)
            )
            btn.pack(fill="x", padx=10, pady=8)

        # Container για frames
        container = tk.Frame(self, bg=BG_PANEL)
        container.pack(side="right", expand=True, fill="both")

        # Frames dictionary
        self.frames = {}
        for key in ["preview", "transactions", "categories", "reports", "settings"]:
            frame = tk.Frame(container, bg=BG_PANEL)
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.frames[key] = frame

        # Δημιουργία περιεχομένου
        self._create_preview_frame()
        self._create_transactions_frame()
        self._create_categories_frame()

        self.show_frame("preview")

    def show_frame(self, key: str):
        frame = self.frames.get(key)
        if frame:
            frame.tkraise()

    def _create_preview_frame(self):
        pr = self.frames["preview"]
        tk.Label(pr, text="Πίνακας Ελέγχου", font=self.h1, bg=BG_PANEL, fg=FG_TEXT).pack(anchor="n", pady=20)

        # Στατιστικά (Εισόδημα και Έξοδα) στο κέντρο κάτω από τον τίτλο
        stats_frame = tk.Frame(pr, bg=BG_PANEL)
        stats_frame.pack(anchor="n", pady=20)

        self.income_label = tk.Label(stats_frame, text="Εισόδημα: 0€", font=self.h2, bg="white", fg="black", width=15, height=2, relief="solid")
        self.income_label.grid(row=0, column=0, padx=10)

        self.expense_label = tk.Label(stats_frame, text="Έξοδα: 0€", font=self.h2, bg="white", fg="black", width=15, height=2, relief="solid")
        self.expense_label.grid(row=0, column=1, padx=10)

        # Δημιουργία πλαισίου για τα δύο κουτιά (Αναλογία και Κινήσεις)
        content_frame = tk.Frame(pr, bg=BG_PANEL)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Χρήση grid για ευθυγράμμιση και ίσο μέγεθος
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)

        # Αριστερό πλαίσιο (Αναλογία Εισοδήματος/Εξόδων)
        left_frame = tk.Frame(content_frame, bg=BG_PANEL, bd=1, relief="solid")
        left_frame.grid(row=0, column=0, padx=20, pady=0, sticky="nsew")

        # Δεξί πλαίσιο (Κινήσεις)
        right_frame = tk.Frame(content_frame, bg="white", bd=1, relief="solid")
        right_frame.grid(row=0, column=1, padx=20, pady=0, sticky="nsew")

        # Διάγραμμα "Αναλογία Εισοδήματος/Εξόδων" στο αριστερό πλαίσιο
        tk.Label(left_frame, text="Αναλογία Εισοδήματος/Εξόδων", font=self.h2, bg=BG_PANEL, fg=FG_TEXT).pack(anchor="n", pady=10)

        # Δημιουργία διαγράμματος κουλούρας
        fig = Figure(figsize=(4, 4), dpi=100)
        ax = fig.add_subplot(111)
        data = [50, 50]  # Placeholder δεδομένα
        labels = ["Εισόδημα", "Έξοδα"]
        colors = ["#4CAF50", "#F44336"]
        ax.pie(data, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors)
        ax.set_title("Αναλογία Εισοδήματος/Εξόδων")

        # Ενσωμάτωση του διαγράμματος στο Tkinter
        self.chart_canvas = FigureCanvasTkAgg(fig, master=left_frame)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(anchor="center", pady=10)

        # Κινήσεις από "Συναλλαγές" και "Κατηγορίες Εξόδων" στο δεξί πλαίσιο
        tk.Label(right_frame, text="Κινήσεις", font=self.h2, bg="white", fg="black").pack(anchor="n", pady=10)

        self.movements_listbox = tk.Listbox(right_frame, bg="white", fg="black", font=self.body)
        self.movements_listbox.pack(fill="both", expand=True, padx=10, pady=10)

    def _create_transactions_frame(self):
        tx = self.frames["transactions"]
        tk.Label(tx, text="Προσθήκη Συναλλαγής", font=self.h2, bg=BG_PANEL, fg=FG_TEXT).pack(anchor="w", padx=20, pady=(20, 0))

        form_tx = tk.Frame(tx, bg=BG_PANEL)
        form_tx.pack(anchor="nw", padx=20, pady=10)

        tk.Label(form_tx, text="Ημερομηνία:", font=self.body, bg=BG_PANEL, fg=FG_TEXT).grid(row=0, column=0)
        self.tx_date = tk.Entry(form_tx, bg=ENTRY_BG, fg=ENTRY_FG, font=self.body)
        self.tx_date.grid(row=0, column=1, padx=5)

        tk.Label(form_tx, text="Κατηγορία:", font=self.body, bg=BG_PANEL, fg=FG_TEXT).grid(row=1, column=0)
        self.tx_category_cb = ttk.Combobox(form_tx, state="readonly", font=self.body)
        self.tx_category_cb.grid(row=1, column=1, padx=5)

        tk.Label(form_tx, text="Ποσό:", font=self.body, bg=BG_PANEL, fg=FG_TEXT).grid(row=2, column=0)
        self.tx_amount = tk.Entry(form_tx, bg=ENTRY_BG, fg=ENTRY_FG, font=self.body)
        self.tx_amount.grid(row=2, column=1, padx=5)

        self.tx_recurring = tk.BooleanVar()
        tk.Checkbutton(form_tx, text="Επαναλαμβανόμενη", font=self.body, variable=self.tx_recurring, bg=BG_PANEL, fg=FG_TEXT).grid(row=3, columnspan=2, pady=5)

        self.tx_add_button = tk.Button(form_tx, text="Προσθήκη Συναλλαγής", bg=CRUD_BTN_BG, fg=CRUD_BTN_FG, font=self.body, bd=0)
        self.tx_add_button.grid(row=4, columnspan=2, pady=10)

        self.tx_listbox = tk.Listbox(tx, bg=ENTRY_BG, fg=ENTRY_FG, font=self.body)
        self.tx_listbox.pack(fill="both", expand=True, padx=20, pady=10)

    def _create_categories_frame(self):
        ct = self.frames["categories"]
        tk.Label(ct, text="Κατηγορίες", font=self.h2, bg=BG_PANEL, fg=FG_TEXT).pack(anchor="w", padx=20, pady=(20, 0))

        self.cat_listbox = tk.Listbox(ct, bg=ENTRY_BG, fg=ENTRY_FG, font=self.body)
        self.cat_listbox.pack(fill="both", expand=True, padx=20, pady=5)

        form_cat = tk.Frame(ct, bg=BG_PANEL)
        form_cat.pack(anchor="nw", padx=20, pady=10)

        tk.Label(form_cat, text="Όνομα:", font=self.body, bg=BG_PANEL, fg=FG_TEXT).grid(row=0, column=0)
        self.cat_name_entry = tk.Entry(form_cat, bg=ENTRY_BG, fg=ENTRY_FG, font=self.body)
        self.cat_name_entry.grid(row=0, column=1, padx=5)

        tk.Label(form_cat, text="Τύπος:", font=self.body, bg=BG_PANEL, fg=FG_TEXT).grid(row=1, column=0)
        self.cat_type_var = tk.StringVar(value="expense")
        self.cat_type_cb = ttk.Combobox(form_cat, textvariable=self.cat_type_var, values=["income", "expense"], font=self.body)
        self.cat_type_cb.grid(row=1, column=1, padx=5)

        self.cat_monthly_var = tk.BooleanVar()
        tk.Checkbutton(form_cat, text="Μηνιαίο", font=self.body, variable=self.cat_monthly_var, bg=BG_PANEL, fg=FG_TEXT).grid(row=2, columnspan=2, pady=5)

        btn_frame = tk.Frame(form_cat, bg=BG_PANEL)
        btn_frame.grid(row=3, columnspan=2, pady=10)

        # Δημιουργία κουμπιών
        self.cat_add_btn = tk.Button(btn_frame, text="Προσθήκη", bg=CRUD_BTN_BG, fg=CRUD_BTN_FG, font=self.body, bd=0)
        self.cat_add_btn.pack(side="left", expand=True, fill="x", padx=2)

        self.cat_del_btn = tk.Button(btn_frame, text="Διαγραφή", bg=CRUD_BTN_BG, fg=CRUD_BTN_FG, font=self.body, bd=0)
        self.cat_del_btn.pack(side="left", expand=True, fill="x", padx=2)

        self.cat_upd_btn = tk.Button(btn_frame, text="Ενημέρωση", bg=CRUD_BTN_BG, fg=CRUD_BTN_FG, font=self.body, bd=0)
        self.cat_upd_btn.pack(side="left", expand=True, fill="x", padx=2)
