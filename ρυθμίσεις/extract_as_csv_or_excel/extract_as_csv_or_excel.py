import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

def export_data():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
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
        root.destroy()
    root.destroy()
    return

# Δημιουργία παραθύρου για την καρτέλα "Ρυθμίσεις"
def create_settings_tab(root):
    settings_frame = tk.Frame(root)
    settings_frame.pack(padx=10, pady=10)

    export_button = tk.Button(settings_frame, text="Εξαγωγή Δεδομένων", command=export_data)
    export_button.pack(pady=10)

    return settings_frame

# Δημιουργία του κύριου παραθύρου
def main():
    root = tk.Tk()
    root.title("Εφαρμογή Εξαγωγής Δεδομένων")

    # Δημιουργία καρτέλας "Ρυθμίσεις"
    settings_tab = create_settings_tab(root)

    root.mainloop()
if __name__ == "__main__":
    main()
