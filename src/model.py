"""
Model layer: Database access with SQLite3.
"""
import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path: str = "finance.db"):
        # Συνδέεται με SQLite database (creates file if not exists)
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        # Δημιουργεί πίνακες categories και transactions αν δεν υπάρχουν
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                is_monthly_template INTEGER NOT NULL
            );
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category_id INTEGER NOT NULL,
                is_template INTEGER NOT NULL,
                FOREIGN KEY(category_id) REFERENCES categories(id)
            );
            """
        )
        self.conn.commit()

    def get_all_categories(self) -> list[dict]:
        cur = self.conn.execute("SELECT * FROM categories")
        return [dict(row) for row in cur.fetchall()]

    def add_category(self, name: str, ctype: str, is_monthly: bool) -> None:
        self.conn.execute(
            "INSERT INTO categories(name, type, is_monthly_template) VALUES (?, ?, ?)",
            (name, ctype, int(is_monthly)),
        )
        self.conn.commit()

    def delete_category(self, category_id: int) -> None:
        self.conn.execute(
            "DELETE FROM categories WHERE id = ?", (category_id,)
        )
        self.conn.commit()

    def update_category(
        self, category_id: int, name: str, type: str, is_monthly_template: bool
    ) -> None:
        self.conn.execute(
            "UPDATE categories SET name = ?, type = ?, is_monthly_template = ? WHERE id = ?",
            (name, type, int(is_monthly_template), category_id),
        )
        self.conn.commit()

    def add_transaction(
        self, date_str: str, amount: float, category_id: int, is_template: bool
    ) -> None:
        self.conn.execute(
            "INSERT INTO transactions(date, amount, category_id, is_template) VALUES (?, ?, ?, ?)",
            (date_str, amount, category_id, int(is_template)),
        )
        self.conn.commit()

    def get_transactions_by_month(self, year: int, month: int) -> list[dict]:
        like = f"{year:04d}-{month:02d}-%"
        cur = self.conn.execute(
            "SELECT * FROM transactions WHERE date LIKE ? ORDER BY date DESC", (like,)
        )
        return [dict(row) for row in cur.fetchall()]

    def get_total_income(self, year: int, month: int) -> float:
        txns = self.get_transactions_by_month(year, month)
        return sum(tx["amount"] for tx in txns if tx["amount"] >= 0)

    def get_total_expense(self, year: int, month: int) -> float:
        txns = self.get_transactions_by_month(year, month)
        return sum(-tx["amount"] for tx in txns if tx["amount"] < 0)
