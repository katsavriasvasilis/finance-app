"""
Λογική εφαρμογής: σύνδεση Model και View.
"""
from model import Database
from view import MainWindow
from datetime import datetime

class AppController:
    def __init__(self):
        self.db = Database()
        self.ui = MainWindow()
        # Bind navigation buttons
        self._bind_nav()
        # Bind λειτουργίες οθονών
        self._bind_preview()
        self._bind_transactions()
        self._bind_categories()
        # (Αναφορές & Ρυθμίσεις θα προστεθούν μετέπειτα)

        # Ξεκινάμε πάντοτε με την προεπισκόπηση
        self.ui.show_frame("preview")

    def _bind_nav(self):
        # Τα κουμπιά στο view καλούν το show_frame απευθείας, οπότε δεν χρειαζόμαστε επιπλέον binding εδώ.
        pass

    # ——— Preview ———
    def _bind_preview(self):
        # Όταν εμφανίζεται η οθόνη, ανανεώνουμε τα νούμερα
        original_show = self.ui.show_frame
        def show_and_refresh(key):
            original_show(key)
            if key == "preview":
                self._refresh_preview()
        self.ui.show_frame = show_and_refresh

    def _refresh_preview(self):
        income = sum(t["amount"] for t in self.db.get_all_categories() if False)  # placeholder
        # καλύτερα: γράψε μεθόδους db.get_total_income() / get_total_expenses()
        total_inc = sum(tx["amount"] for tx in self.db.get_transactions_by_month(
            datetime.now().year, datetime.now().month) if tx["amount"]>0)
        total_exp = sum(-tx["amount"] for tx in self.db.get_transactions_by_month(
            datetime.now().year, datetime.now().month) if tx["amount"]<0)
        balance   = total_inc - total_exp
        self.ui.preview_income.config(text=f"Εισόδημα: {total_inc:.2f}€")
        self.ui.preview_balance.config(text=f"Διαθέσιμο Υπόλοιπο: {balance:.2f}€")

    # ——— Συναλλαγές ———
    def _bind_transactions(self):
        # Κουμπί Προσθήκης
        btn = self.ui.frames["transactions"].children.get("!button")
        btn.config(command=self._handle_add_transaction)
        # TODO: δες ποιο widget είναι ποιο based on το order

    def _handle_add_transaction(self):
        date_str  = self.ui.tx_date.get().strip()
        cat       = self.ui.tx_category.get().strip()
        amt       = float(self.ui.tx_amount.get().strip() or 0)
        recur     = self.ui.tx_recurring.get()
        # Για ευκολία, βρίσκουμε category_id βάσει ονόματος
        cats = self.db.get_all_categories()
        cat_map = {c["name"]: c["id"] for c in cats}
        if date_str and cat in cat_map:
            # Format date
            try:
                d = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return
            self.db.add_transaction(date_str, amt, cat_map[cat], recur)
            self._refresh_transactions()

    def _refresh_transactions(self):
        # Προσθέτουμε στη οθόνη έναν Listbox ή Treeview με όλες τις συναλλαγές
        tx_frame = self.ui.frames["transactions"]
        # TODO: διαγραφή παλιού πίνακα + ανανέωση με νέα δεδομένα

    # ——— Κατηγορίες ———
    def _bind_categories(self):
        # Συνδέουμε τα stubs από view στα handlers που κάναμε παλαιότερα
        self.ui._add_category    = self._handle_add_category
        self.ui._delete_category = self._handle_delete_category
        self.ui._update_category = self._handle_update_category
        # Αρχική φόρτωση
        self._refresh_categories()

    def _refresh_categories(self):
        cats = self.db.get_all_categories()
        lb = self.ui.cat_listbox
        lb.delete(0, 'end')
        self._cat_ids = []
        for cat in cats:
            label = f"{cat['name']} ({cat['type']})"
            if cat['is_monthly_template']:
                label += " [Μηνιαίο]"
            lb.insert('end', label)
            self._cat_ids.append(cat["id"])

    def _handle_add_category(self):
        name = self.ui.cat_name_entry.get().strip()
        ctype= self.ui.cat_type_var.get()
        mon  = self.ui.cat_monthly_var.get()
        if name:
            self.db.add_category(name, ctype, mon)
            self._refresh_categories()

    def _handle_delete_category(self):
        sel = self.ui.cat_listbox.curselection()
        if not sel: return
        cat_id = self._cat_ids[sel[0]]
        self.db.delete_category(cat_id)
        self._refresh_categories()

    def _handle_update_category(self):
        sel = self.ui.cat_listbox.curselection()
        if not sel: return
        cat_id = self._cat_ids[sel[0]]
        name   = self.ui.cat_name_entry.get().strip()
        ctype  = self.ui.cat_type_var.get()
        mon    = self.ui.cat_monthly_var.get()
        if name:
            self.db.update_category(cat_id, name=name, type=ctype, is_monthly_template=mon)
            self._refresh_categories()

    def run(self):
        self.ui.mainloop()

if __name__ == "__main__":
    AppController().run()
