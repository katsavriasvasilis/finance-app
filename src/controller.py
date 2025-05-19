"""
Λογική εφαρμογής: σύνδεση Model και View.
"""
from model import Database
from view import MainWindow

class AppController:
    def __init__(self):
        self.db = Database()
        self.ui = MainWindow()
        self._bind_events()

    def _bind_events(self):
        # TODO: Όταν φορτώνει κάθε tab, γεμίζουμε Widgets από τη ΒΔ
        pass

    def run(self):
        self.ui.mainloop()

if __name__ == "__main__":
    app = AppController()
    app.run()

