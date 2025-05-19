"""
GUI components με tkinter.
"""
import tkinter as tk
from tkinter import ttk

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Personal Finance Manager")
        self.geometry("800x600")

        # Tab control
        tab_control = ttk.Notebook(self)
        self.tab_categories   = ttk.Frame(tab_control)
        self.tab_transactions = ttk.Frame(tab_control)
        self.tab_reports      = ttk.Frame(tab_control)

        tab_control.add(self.tab_categories,   text='Κατηγορίες')
        tab_control.add(self.tab_transactions, text='Συναλλαγές')
        tab_control.add(self.tab_reports,      text='Αναφορές')
        tab_control.pack(expand=1, fill='both')

        # --- ΚΑΡΤΕΛΑ ΚΑΤΗΓΟΡΙΩΝ ---
        # Listbox για τις κατηγορίες
        self.cat_listbox = tk.Listbox(self.tab_categories)
        self.cat_listbox.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        # Δεξί πλαίσιο με φόρμα και κουμπιά
        right_frame = ttk.Frame(self.tab_categories)
        right_frame.pack(side='right', fill='y', padx=5, pady=5)

        # Όνομα κατηγορίας
        tk.Label(right_frame, text="Όνομα Κατηγορίας:").pack(anchor='w')
        self.cat_name_entry = tk.Entry(right_frame)
        self.cat_name_entry.pack(fill='x')

        # Τύπος (income/expense)
        tk.Label(right_frame, text="Τύπος:").pack(anchor='w', pady=(10,0))
        self.cat_type_var = tk.StringVar(value='expense')
        ttk.Combobox(
            right_frame,
            textvariable=self.cat_type_var,
            values=['income', 'expense']
        ).pack(fill='x')

        # Checkbox για μηνιαίο
        self.cat_monthly_var = tk.BooleanVar()
        tk.Checkbutton(
            right_frame,
            text="Μηνιαίο",
            variable=self.cat_monthly_var
        ).pack(anchor='w', pady=5)

        # Κουμπιά CRUD
        ttk.Button(
            right_frame,
            text="Προσθήκη",
            command=self._add_category
        ).pack(fill='x', pady=(10,2))
        ttk.Button(
            right_frame,
            text="Διαγραφή",
            command=self._delete_category
        ).pack(fill='x', pady=2)
        ttk.Button(
            right_frame,
            text="Ενημέρωση",
            command=self._update_category
        ).pack(fill='x', pady=2)

    # --- Stubs για χειριστήρια (θα δεθούν από τον controller) ---
    def _add_category(self):
        """Κλήση από κουμπί Προσθήκης κατηγορίας"""
        pass

    def _delete_category(self):
        """Κλήση από κουμπί Διαγραφής επιλεγμένης κατηγορίας"""
        pass

    def _update_category(self):
        """Κλήση από κουμπί Ενημέρωσης επιλεγμένης κατηγορίας"""
        pass
