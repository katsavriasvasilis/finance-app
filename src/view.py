import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk
import os

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
    def __init__(self, controller):
        super().__init__()
        self.controller = controller  # Αποθηκεύουμε την αναφορά του controller

        # Styling combobox
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure(
            'Flat.TButton',
            borderwidth=0,
            highlightthickness=0
        )
        style.configure(
            'Custom.TCombobox',
            fieldbackground=ENTRY_BG,
            background=ENTRY_BG,
            foreground=ENTRY_FG
        )
        style.map(
            'Custom.TCombobox',
            fieldbackground=[('readonly', ENTRY_BG)],
            foreground=[('readonly', ENTRY_FG)]
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
        self._create_reports_frame()
        self._create_settings_frame()  # Δημιουργία του frame ρυθμίσεων

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
        data = [50, 50]  # Placeholder δεδομένασ
        labels = ["Εισόδημα", "Έξοδα"]
        colors = ["#58468A", "#B0B0B3"]
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

        # Πεδίο για την ημερομηνία
        tk.Label(form_tx, text="Ημερομηνία (ΗΗ/ΜΜ/ΧΧ):", font=self.body, bg=BG_PANEL, fg=FG_TEXT).grid(row=0, column=0)
        self.tx_date = tk.Entry(form_tx, bg=ENTRY_BG, fg=ENTRY_FG, font=self.body)
        self.tx_date.grid(row=0, column=1, padx=5)
        self.tx_date.insert(0, "ΗΗ/ΜΜ/ΧΧ")  # Προεπιλεγμένο κείμενο

        # Πεδίο για την κατηγορία
        tk.Label(form_tx, text="Κατηγορία:", font=self.body, bg=BG_PANEL, fg=FG_TEXT).grid(row=1, column=0)
        self.tx_category_cb = ttk.Combobox(
            form_tx,
            state="readonly",
            font=self.body,
            values=[],  # Οι τιμές θα ενημερωθούν από τον controller
            style="Custom.TCombobox",  # Εφαρμογή του ίδιου στυλ
            width=18
        )
        self.tx_category_cb.grid(row=1, column=1, padx=5)

        # Πεδίο για το ποσό
        tk.Label(form_tx, text="Ποσό:", font=self.body, bg=BG_PANEL, fg=FG_TEXT).grid(row=2, column=0)
        self.tx_amount = tk.Entry(form_tx, bg=ENTRY_BG, fg=ENTRY_FG, font=self.body)
        self.tx_amount.grid(row=2, column=1, padx=5)

        # Checkbox για επαναλαμβανόμενη συναλλαγή
        self.tx_recurring = tk.BooleanVar()
        tk.Checkbutton(
            form_tx,
            text="Επαναλαμβανόμενη",
            font=self.body,
            variable=self.tx_recurring,  # Σύνδεση με τη μεταβλητή
            onvalue=True,  # Τιμή όταν είναι επιλεγμένο
            offvalue=False,  # Τιμή όταν δεν είναι επιλεγμένο
            bg=BG_PANEL,
            fg=FG_TEXT
        ).grid(row=3, columnspan=2, pady=5)

        # Κουμπί για προσθήκη συναλλαγής
        self.tx_add_button = tk.Button(form_tx, text="Προσθήκη Συναλλαγής", bg=CRUD_BTN_BG, fg=CRUD_BTN_FG, font=self.body, bd=0)
        self.tx_add_button.grid(row=4, columnspan=2, pady=10)

        # Λίστα συναλλαγών
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

    def _create_reports_frame(self):
        reports = self.frames["reports"]
        tk.Label(reports, text="Αναφορές", font=self.h1, bg=BG_PANEL, fg=FG_TEXT).pack(anchor="n", pady=20)

        # Δημιουργία πλαισίου για το διάγραμμα
        chart_frame = tk.Frame(reports, bg=BG_PANEL)
        chart_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Δεδομένα για το διάγραμμα (μηδενικά δεδομένα)
        months = ["Ιαν", "Φεβ", "Μαρ", "Απρ", "Μάι", "Ιούν", "Ιούλ", "Αύγ", "Σεπ", "Οκτ", "Νοέ", "Δεκ"]
        income = [0] * 12  # Μηδενικά έσοδα
        expenses = [0] * 12  # Μηδενικά έξοδα

        # Δημιουργία διαγράμματος ράβδων
        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(months, income, label="Έσοδα", color="green", alpha=0.7)
        ax.bar(months, expenses, label="Έξοδα", color="red", alpha=0.7)
        ax.set_title("Μηνιαία Έσοδα vs Έξοδα")
        ax.set_xlabel("Μήνες")
        ax.set_ylabel("Ποσά (€)")
        ax.legend()

        # Ενσωμάτωση του διαγράμματος στο Tkinter
        chart_canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill="both", expand=True)

    def _create_settings_frame(self):
        settings_frame = self.frames["settings"]
        tk.Label(settings_frame, text="Ρυθμίσεις", font=self.h1, bg=BG_PANEL, fg=FG_TEXT).pack(anchor="n", pady=20)

        # Ετικέτα για αλλαγή γλώσσας
        tk.Label(settings_frame, text="Αλλαγή γλώσσας:", font=self.body, bg=BG_PANEL, fg=FG_TEXT).pack(anchor="n", pady=10)

        # Πλαίσιο για τις σημαίες
        flags_frame = tk.Frame(settings_frame, bg=BG_PANEL)
        flags_frame.pack(anchor="n", pady=10)

        # Κουμπιά με σημαίες
        greek_flag_path = r"E:\Documents\Πανεπιστήμιο ΕΑΠ\Εργασία  ΠληΠΡΟ (2025)\finance-app\ρυθμίσεις\buttons_greek_english\gr.png"
        english_flag_path = r"E:\Documents\Πανεπιστήμιο ΕΑΠ\Εργασία  ΠληΠΡΟ (2025)\finance-app\ρυθμίσεις\buttons_greek_english\eng.png"

        # Αυξάνουμε το μέγεθος των σημαιών
        greek_flag = ImageTk.PhotoImage(Image.open(greek_flag_path).resize((60, 40)))  # Πλάτος 60, Ύψος 40
        english_flag = ImageTk.PhotoImage(Image.open(english_flag_path).resize((60, 40)))  # Πλάτος 60, Ύψος 40

        greek_btn = tk.Button(flags_frame, image=greek_flag, command=lambda: self.change_language("greek"), bg=BG_PANEL, bd=0)
        greek_btn.image = greek_flag  # Αποθήκευση αναφοράς για να μην χαθεί η εικόνα
        greek_btn.pack(side="left", padx=10)

        english_btn = tk.Button(flags_frame, image=english_flag, command=lambda: self.change_language("english"), bg=BG_PANEL, bd=0)
        english_btn.image = english_flag  # Αποθήκευση αναφοράς για να μην χαθεί η εικόνα
        english_btn.pack(side="left", padx=10)

        # Ετικέτα για αλλαγή νομίσματος
        tk.Label(settings_frame, text="Αλλαγή νομίσματος:", font=self.body, bg=BG_PANEL, fg=FG_TEXT).pack(anchor="n", pady=10)

        # ComboBox για την επιλογή νομίσματος
        currency_combobox = ttk.Combobox(settings_frame, state="readonly", font=self.body)
        currency_combobox['values'] = [
            "Ευρώ (€)", "Δολάριο ΗΠΑ (USD)", "Λίρα Αγγλίας (GBP)", "Ιαπωνικό Γιεν (JPY)",
            "Ελβετικό Φράγκο (CHF)", "Δολάριο Καναδά (CAD)", "Δολάριο Αυστραλίας (AUD)",
            "Κορόνα Σουηδίας (SEK)", "Κορόνα Νορβηγίας (NOK)", "Κορόνα Δανίας (DKK)",
            "Ρούβλι Ρωσίας (RUB)", "Γουάν Κίνας (CNY)", "Ρουπία Ινδίας (INR)",
            "Δολάριο Σιγκαπούρης (SGD)", "Δολάριο Νέας Ζηλανδίας (NZD)", "Πέσο Μεξικού (MXN)"
        ]
        currency_combobox.pack(anchor="n", pady=10)
        currency_combobox.current(0)

        # Κουμπί για εξαγωγή δεδομένων
        export_button = tk.Button(settings_frame, text="Εξαγωγή ως", command=self._export_data, bg=BTN_BG, fg=BTN_FG, font=self.body)
        export_button.pack(anchor="n", pady=10)

    def change_language(self, language):
        """Αλλαγή γλώσσας της εφαρμογής και εμφάνιση μηνύματος σε νέο παράθυρο."""
        if language == "greek":
            message = "Το πρόγραμμα λειτουργεί πλέον στα Ελληνικά"
        elif language == "english":
            message = "The program works now in English"
        else:
            message = "Unknown language"

        # Δημιουργία νέου παραθύρου για το μήνυμα
        popup = tk.Toplevel(self)
        popup.title("Αλλαγή Γλώσσας")
        popup.configure(bg=BG_PANEL)

        # Ετικέτα για το μήνυμα
        label = tk.Label(popup, text=message, font=self.body, bg=BG_PANEL, fg=FG_TEXT)
        label.pack(expand=True, pady=20)

        # Κουμπί για κλείσιμο του παραθύρου
        tk.Button(popup, text="OK", command=popup.destroy, bg=BTN_BG, fg=BTN_FG, font=self.body).pack(pady=10)

        # Προσαρμογή μεγέθους παραθύρου
        popup.update_idletasks()  # Υπολογισμός του απαιτούμενου μεγέθους
        width = label.winfo_reqwidth() + 40  # Προσθέτουμε padding
        height = label.winfo_reqheight() + 80  # Προσθέτουμε padding για το κουμπί
        popup.geometry(f"{width}x{height}")

    def _export_data(self):
        """Λειτουργία εξαγωγής δεδομένων ως CSV ή Excel."""
        folder_selected = filedialog.askdirectory(title="Επιλέξτε φάκελο αποθήκευσης")
        if not folder_selected:
            messagebox.showwarning("Ειδοποίηση", "Δεν επιλέχθηκε φάκελος αποθήκευσης.")
            return
        try:
            df = pd.DataFrame({
                "Ημερομηνία": [],
                "Κατηγορία": [],
                "Ποσό": [],
                "Επαναλαμβανόμενη": []
            })
            file_path = filedialog.asksaveasfilename(
                initialdir=folder_selected,
                title="Αποθήκευση ως",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")]
            )
            if not file_path:
                return
            if file_path.endswith(".csv"):
                df.to_csv(file_path, index=False)
            else:
                df.to_excel(file_path, index=False)
            messagebox.showinfo("Επιτυχία", "Τα δεδομένα εξήχθησαν επιτυχώς.")
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Σφάλμα κατά την εξαγωγή: {e}")

    def _refresh_categories(self):
        # Οι σωστές κατηγορίες
        category_names = [
            "Συνδρομές (streaming, γυμναστήριο)",
            "Μεταβλητά Έξοδα – Καθημερινής Διαβίωσης",
            "Τρόφιμα & Σούπερ Μάρκετ",
            "Καφές / Delivery",
            "Μετακινήσεις (βενζίνη, ΜΜΜ)",
            "Προσωπική Φροντίδα & Υγεία",
            "Φάρμακα & Ιατρικές Επισκέψεις",
            "Κομμωτήριο / Καλλυντικά",
            "Διασκέδαση & Ελεύθερος Χρόνος",
            "Κινηματογράφος / Θέατρο",
            "Ταξίδια & Διακοπές",
            "Εκπαίδευση & Παιδιά",
            "Φροντιστήρια / Μαθήματα",
            "Σχολικά Τέλη & Είδη",
            "Ενδυμασία & Οικιακός Εξοπλισμός",
            "Ρούχα & Υποδήματα",
            "Έπιπλα & Ηλεκτρικές Συσκευές",
            "Αποταμίευση & Επενδύσεις",
            "Ταμείο Έκτακτων Αναγκών",
            "Επενδυτικά Προϊόντα",
            "Φορολογία & Διοικητικά Τέλη",
            "Φόροι (εισοδήματος, ΙΧ)",
            "Δημοτικά & Κυκλοφορίας Τέλη"
        ]
        # Ενημέρωση του Combobox
        self.ui.tx_category_cb['values'] = category_names
        # Ορισμός της πρώτης κατηγορίας ως προεπιλεγμένη
        self.ui.tx_category_cb.current(0)

    def _handle_add_transaction(self):
        date_str = self.ui.tx_date.get().strip()
        cat_name = self.ui.tx_category_cb.get().strip()
        try:
            amt = float(self.ui.tx_amount.get().strip())
        except ValueError:
            print("Μη έγκυρο ποσό!")
            return

        is_recurring = self.ui.tx_recurring.get()  # Παίρνουμε την τιμή του checkbox
        print(f"Ημερομηνία: {date_str}, Κατηγορία: {cat_name}, Ποσό: {amt}, Επαναλαμβανόμενη: {is_recurring}")

        # Αποθήκευση της συναλλαγής στη βάση δεδομένων
        self.db.add_transaction(transaction_date=date_str, category=cat_name, amount=amt, recurring=is_recurring)

        # Εκτύπωση της κατάστασης του checkbox μετά την αποθήκευση
        print(f"Κατάσταση του checkbox μετά την αποθήκευση: {self.ui.tx_recurring.get()}")

        # Επαναφορά των πεδίων στην αρχική τους κατάσταση
        self.ui.tx_date.delete(0, 'end')
        self.ui.tx_date.insert(0, "ΗΗ/ΜΜ/ΧΧ")  # Προσθήκη προεπιλεγμένου κειμένου

        self.ui.tx_category_cb.set('')  # Επαναφορά του Combobox "Κατηγορία"

        self.ui.tx_amount.delete(0, 'end')  # Καθαρισμός του πεδίου "Ποσό"

        self.ui.tx_recurring.set(False)  # Επαναφορά του checkbox σε μη επιλεγμένο

    def _bind_transactions(self):
        self.ui.tx_add_button.config(command=self._handle_add_transaction)
        self._refresh_transactions()

        # Εκτύπωση της τιμής του checkbox όταν αλλάζει
        self.ui.tx_recurring.trace_add("write", lambda *args: print(f"Επαναλαμβανόμενη: {self.ui.tx_recurring.get()}"))

    def add_transaction(self, date, category, amount, recurring):
        # Υλοποίηση της μεθόδου
        pass

class Database:
    def add_transaction(self, transaction_date, category, amount, recurring):
        # Υλοποίηση της μεθόδου
        print(f"Προσθήκη συναλλαγής: {transaction_date}, {category}, {amount}, {recurring}")

def main():
    root = tk.Tk()
    root.geometry("300x200")
    recurring_var = tk.BooleanVar()

    def print_value(*args):
        print(f"Επαναλαμβανόμενη: {recurring_var.get()}")

    recurring_var.trace_add("write", print_value)
    tk.Checkbutton(
        root,
        text="Επαναλαμβανόμενη",
        variable=recurring_var,
        onvalue=True,
        offvalue=False
    ).pack(pady=20)
    root.mainloop()
