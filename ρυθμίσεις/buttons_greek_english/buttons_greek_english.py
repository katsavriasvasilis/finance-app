import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os

def change_language(language):
    if language == "greek":
        messagebox.showinfo("Αλλαγή Γλώσσας", "Το πρόγραμμα είναι τώρα στα Ελληνικά.")
    elif language == "english":
        messagebox.showinfo("Language Change", "The program is now in English.")
    else:
        messagebox.showerror("Σφάλμα", "Μη υποστηριζόμενη γλώσσα.")

def create_button_with_flag(root, flag_path, language):
    # Φτιάχνουμε απόλυτο μονοπάτι με βάση τον φάκελο του τρέχοντος αρχείου
    absolute_path = os.path.abspath(flag_path)
    if not os.path.exists(absolute_path):
        messagebox.showerror("Σφάλμα", f"Το αρχείο {absolute_path} δεν βρέθηκε.")
        return None

    img = Image.open(absolute_path)
    img = img.resize((50, 30), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(img)

    btn = ttk.Button(root, image=photo, command=lambda: change_language(language))
    btn.image = photo  # κρατάμε την αναφορά
    return btn

def main():
    # Διαδρομές για τις σημαίες
    greek_flag_path = r"E:\Documents\Πανεπιστήμιο ΕΑΠ\Εργασία  ΠληΠΡΟ (2025)\finance-app\assets\gr"
    english_flag_path = r"E:\Documents\Πανεπιστήμιο ΕΑΠ\Εργασία  ΠληΠΡΟ (2025)\finance-app\assets\eng"

    print("Ελέγχουμε αν τα αρχεία υπάρχουν:")
    print(f"gr υπάρχει: {os.path.exists(greek_flag_path)}")
    print(f"eng υπάρχει: {os.path.exists(english_flag_path)}")

    root = tk.Tk()
    root.title("Αλλαγή Γλώσσας")
    root.geometry("400x200")
    root.resizable(False, False)
    root.configure(bg="white")

    frame = ttk.Frame(root, padding=10)
    frame.pack(expand=True)

    # Δημιουργούμε τα κουμπιά
    greek_btn = create_button_with_flag(frame, greek_flag_path, "greek")
    english_btn = create_button_with_flag(frame, english_flag_path, "english")

    if greek_btn:
        greek_btn.grid(row=0, column=0, padx=20, pady=20)
    if english_btn:
        english_btn.grid(row=0, column=1, padx=20, pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()