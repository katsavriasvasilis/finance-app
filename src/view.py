"""
GUI components με tkinter.
"""
import tkinter as tk
from tkinter import ttk

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Personal Finance Manager")
        self.geometry("800x600")
        tab_control = ttk.Notebook(self)
        self.tab_categories = ttk.Frame(tab_control)
        self.tab_transactions = ttk.Frame(tab_control)
        self.tab_reports = ttk.Frame(tab_control)
        tab_control.add(self.tab_categories, text='Κατηγορίες')
        tab_control.add(self.tab_transactions, text='Συναλλαγές')
        tab_control.add(self.tab_reports, text='Αναφορές')
        tab_control.pack(expand=1, fill='both')
        # TODO: Προσθήκη widgets σε κάθε tab

