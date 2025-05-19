"""
Λογική εφαρμογής: σύνδεση Model και View.
"""
from model import Database
from view import MainWindow

class AppController:
    def __init__(self):
        # 1) Data layer
        self.db = Database()
        # 2) GUI
        self.ui = MainWindow()
        # 3) Σύνδεση GUI ↔ Model
        self._bind_events()
        # 4) Αρχικό γέμισμα της λίστας κατηγοριών
        self._refresh_categories()

    def _bind_events(self):
        """
        Συνδέει τα κουμπιά της view με τις μεθόδους του controller.
        """
        self.ui._add_category    = self._handle_add_category
        self.ui._delete_category = self._handle_delete_category
        self.ui._update_category = self._handle_update_category

    def _refresh_categories(self):
        """
        Φορτώνει όλες τις κατηγορίες από τη ΒΔ και τις εμφανίζει στο listbox.
        """
        cats = self.db.get_all_categories()
        lb = self.ui.cat_listbox
        lb.delete(0, 'end')
        for cat in cats:
            label = f"{cat['name']} ({cat['type']})"
            if cat['is_monthly_template']:
                label += " [Μηνιαίο]"
            lb.insert('end', label)
        # Φυλάμε τα ids σε list για later reference
        self._cat_ids = [cat['id'] for cat in cats]

    def _handle_add_category(self):
        """
        Κουμπί 'Προσθήκη': παίρνει τιμές από τα πεδία και καλεί το model.
        """
        name = self.ui.cat_name_entry.get().strip()
        ctype = self.ui.cat_type_var.get()
        monthly = self.ui.cat_monthly_var.get()
        if name:
            self.db.add_category(name, ctype, monthly)
            self._refresh_categories()

    def _handle_delete_category(self):
        """
        Κουμπί 'Διαγραφή': διαγράφει την επιλεγμένη κατηγορία.
        """
        sel = self.ui.cat_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        cat_id = self._cat_ids[idx]
        self.db.delete_category(cat_id)
        self._refresh_categories()

    def _handle_update_category(self):
        """
        Κουμπί 'Ενημέρωση': ενημερώνει την επιλεγμένη κατηγορία με νέα τιμή.
        """
        sel = self.ui.cat_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        cat_id = self._cat_ids[idx]
        name = self.ui.cat_name_entry.get().strip()
        ctype = self.ui.cat_type_var.get()
        monthly = self.ui.cat_monthly_var.get()
        if name:
            self.db.update_category(cat_id, name=name, type=ctype, is_monthly_template=monthly)
            self._refresh_categories()

    def run(self):
        # Εκκίνηση του GUI loop
        self.ui.mainloop()

if __name__ == "__main__":
    AppController().run()
