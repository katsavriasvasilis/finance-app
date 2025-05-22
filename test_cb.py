import tkinter as tk
from tkinter import ttk

ENTRY_BG  = "#4B5563"
ENTRY_FG  = "#F9FAFB"

root = tk.Tk()
root.title("Test Combobox")
root.geometry("400x200")

style = ttk.Style(root)
style.theme_use('clam')
style.configure('Custom.TCombobox',
                fieldbackground=ENTRY_BG,
                background=ENTRY_BG,
                foreground=ENTRY_FG)
style.map('Custom.TCombobox',
          fieldbackground=[('readonly', ENTRY_BG)],
          foreground=[('readonly', ENTRY_FG)])

tk.Label(root, text="Επιλογή Κατηγορίας:", anchor="w") \
  .pack(fill="x", padx=20, pady=(20,0))

cb = ttk.Combobox(
    root,
    state="readonly",
    style="Custom.TCombobox",
    values=[
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
)
cb.pack(fill="x", padx=20, pady=20)
cb.current(0)

root.mainloop()
