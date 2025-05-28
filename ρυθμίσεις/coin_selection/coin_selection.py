from PyQt5.QtWidgets import QComboBox, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTabWidget

class SettingsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ρυθμίσεις")
        self.setFixedSize(500, 300)  # Αυξάνουμε το πλάτος του παραθύρου

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Κεντράρουμε το περιεχόμενο του layout

        # Ετικέτα για την επιλογή νομίσματος
        self.label = QLabel("Επιλογή σε άλλο νόμισμα:")
        self.label.setFont(QFont("Arial", 12))  # Αυξάνουμε το μέγεθος της γραμματοσειράς
        self.label.setAlignment(Qt.AlignCenter)  # Ευθυγράμμιση στο κέντρο
        self.label.setStyleSheet("padding: 15px;")  # Προσθέτουμε padding γύρω από την ετικέτα
        layout.addWidget(self.label)

        # ComboBox για την επιλογή νομίσματος
        self.comboBox = QComboBox()
        self.comboBox.addItems([
            "Δολάριο ΗΠΑ (USD)",
            "Λίρα Αγγλίας (GBP)",
            "Ιαπωνικό Γιεν (JPY)",
            "Ελβετικό Φράγκο (CHF)",
            "Δολάριο Καναδά (CAD)",
            "Δολάριο Αυστραλίας (AUD)",
            "Κορόνα Σουηδίας (SEK)",
            "Κορόνα Νορβηγίας (NOK)",
            "Κορόνα Δανίας (DKK)",
            "Ρούβλι Ρωσίας (RUB)",
            "Γουάν Κίνας (CNY)",
            "Ρουπία Ινδίας (INR)",
            "Δολάριο Σιγκαπούρης (SGD)",
            "Δολάριο Νέας Ζηλανδίας (NZD)",
            "Πέσο Μεξικού (MXN)"
        ])
        self.comboBox.setStyleSheet("padding: 5px;")  # Προσθέτουμε padding στο ComboBox
        layout.addWidget(self.comboBox)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Κύριο Παράθυρο")
        self.setFixedSize(900, 700)

        # Κεντρικό layout για το κύριο παράθυρο
        centralWidget = QWidget(self)
        centralLayout = QVBoxLayout(centralWidget)
        centralLayout.setAlignment(Qt.AlignCenter)  # Κεντράρουμε το περιεχόμενο

        # Προσθήκη καρτέλας "Ρυθμίσεις"
        self.tabWidget = QTabWidget(self)
        self.settingsTab = SettingsTab(self)
        self.tabWidget.addTab(self.settingsTab, "Ρυθμίσεις")

        centralLayout.addWidget(self.tabWidget)
        self.setCentralWidget(centralWidget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
