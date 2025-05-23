from src.view import MainWindow
from src.controller import AppController
from src.model import Database

def main():
    db = Database()
    ui = MainWindow(None)  # Το controller θα συνδεθεί αργότερα
    controller = AppController(ui, db)
    ui.controller = controller  # Σύνδεση του controller στο view
    ui.mainloop()

if __name__ == "__main__":
    main()