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

    def _bind_events(self):
        """
        Εδώ θα συνδέσουμε:
        - self.ui._add_category  → self.db.add_category + refresh listbox
        - self.ui._delete_category → self.db.delete_category + refresh
        - self.ui._update_category → self.db.update_category + refresh
        """
        pass

    def run(self):
        # Εκκίνηση του GUI loop
        self.ui.mainloop()

if __name__ == "__main__":
    # Αν τρέξουμε απευθείας:
    AppController().run()
