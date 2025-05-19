from .model import Database
from .view import MainWindow
from datetime import datetime

class AppController:
    def __init__(self):
        # Model
        self.db = Database()
        # View
        self.ui = MainWindow()
        # Bind events
        self._bind_categories()
        self._bind_transactions()
        # Start
        self.ui.show_frame("preview")

    # ——— Categories CRUD ———
    def _bind_categories(self):
        self.ui.cat_add_btn.config(command=self._handle_add_category)
        self.ui.cat_del_btn.config(command=self._handle_delete_category)
        self.ui.cat_upd_btn.config(command=self._handle_update_category)
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
            self._cat_ids.append(cat['id'])
        # ενημέρωση combobox συναλλαγών
        self.ui.tx_category_cb['values'] = [c['name'] for c in cats]

    def _handle_add_category(self):
        name = self.ui.cat_name_entry.get().strip()
        ctype = self.ui.cat_type_var.get()
        mon = self.ui.cat_monthly_var.get()
        if name:
            self.db.add_category(name, ctype, mon)
            self._refresh_categories()

    def _handle_delete_category(self):
        sel = self.ui.cat_listbox.curselection()
        if sel:
            cid = self._cat_ids[sel[0]]
            self.db.delete_category(cid)
            self._refresh_categories()

    def _handle_update_category(self):
        sel = self.ui.cat_listbox.curselection()
        if sel:
            cid = self._cat_ids[sel[0]]
            name = self.ui.cat_name_entry.get().strip()
            ctype = self.ui.cat_type_var.get()
            mon = self.ui.cat_monthly_var.get()
            if name:
                self.db.update_category(cid, name=name, type=ctype, is_monthly_template=mon)
                self._refresh_categories()

    # ——— Transactions CRUD ———
    def _bind_transactions(self):
        self.ui.tx_add_button.config(command=self._handle_add_transaction)
        self._refresh_transactions()

    def _refresh_transactions(self):
        txns = self.db.get_transactions_by_month(datetime.now().year, datetime.now().month)
        lb = self.ui.tx_listbox
        lb.delete(0, 'end')
        for tx in txns:
            lb.insert('end', f"{tx['date']} • {tx['amount']}€ • {tx['category_name']}")

    def _handle_add_transaction(self):
        date_str = self.ui.tx_date.get().strip()
        cat_name = self.ui.tx_category_cb.get().strip()
        try:
            amt = float(self.ui.tx_amount.get().strip())
        except ValueError:
            return
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return
        cats = self.db.get_all_categories()
        name_to_id = {c['name']: c['id'] for c in cats}
        cid = name_to_id.get(cat_name)
        if cid is None:
            return
        self.db.add_transaction(date_str, amt, cid, self.ui.tx_recurring.get())
        self._refresh_transactions()

    def run(self):
        self.ui.mainloop()

if __name__ == '__main__':
    AppController().run()
