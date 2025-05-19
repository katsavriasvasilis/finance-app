"""
Data layer: SQLite schema και CRUD για categories & transactions
"""
import sqlite3
from datetime import date

class Database:
    def __init__(self, db_path="finance.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Πίνακας κατηγοριών
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT CHECK(type IN ('income','expense')) NOT NULL,
            is_monthly_template INTEGER NOT NULL DEFAULT 0
        )
        """)
        # Πίνακας συναλλαγών
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            category_id INTEGER NOT NULL,
            is_template INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY(category_id) REFERENCES categories(id)
        )
        """)
        self.conn.commit()

    # --- CRUD για κατηγορίες ---
    def add_category(self, name: str, type: str, is_monthly_template: bool=False):
        sql = "INSERT INTO categories (name,type,is_monthly_template) VALUES (?,?,?)"
        self.conn.execute(sql, (name, type, int(is_monthly_template)))
        self.conn.commit()

    def get_all_categories(self):
        cursor = self.conn.execute(
            "SELECT id,name,type,is_monthly_template FROM categories"
        )
        return [dict(row) for row in cursor.fetchall()]

    def update_category(self, category_id: int, name: str=None, type: str=None, is_monthly_template: bool=None):
        fields, params = [], []
        if name is not None:
            fields.append("name = ?"); params.append(name)
        if type is not None:
            fields.append("type = ?"); params.append(type)
        if is_monthly_template is not None:
            fields.append("is_monthly_template = ?"); params.append(int(is_monthly_template))
        if not fields:
            return
        sql = f"UPDATE categories SET {', '.join(fields)} WHERE id = ?"
        params.append(category_id)
        self.conn.execute(sql, params)
        self.conn.commit()

    def delete_category(self, category_id: int):
        # Policy: διαγράφουμε κατηγορίες καί cascade delete σε συναλλαγές
        self.conn.execute("DELETE FROM transactions WHERE category_id = ?", (category_id,))
        self.conn.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        self.conn.commit()

    # --- CRUD για συναλλαγές ---
    def add_transaction(self, date_str: str, amount: float, category_id: int, is_template: bool=False):
        sql = "INSERT INTO transactions (date,amount,category_id,is_template) VALUES (?,?,?,?)"
        self.conn.execute(sql, (date_str, amount, category_id, int(is_template)))
        self.conn.commit()

    def get_transactions_by_month(self, year: int, month: int):
        pattern = f"{year:04d}-{month:02d}-%"
        cursor = self.conn.execute(
            "SELECT id,date,amount,category_id,is_template FROM transactions WHERE date LIKE ?",
            (pattern,)
        )
        return [dict(row) for row in cursor.fetchall()]

    def update_transaction(self, txn_id: int, date_str: str=None, amount: float=None,
                           category_id: int=None, is_template: bool=None):
        fields, params = [], []
        if date_str is not None:
            fields.append("date = ?"); params.append(date_str)
        if amount is not None:
            fields.append("amount = ?"); params.append(amount)
        if category_id is not None:
            fields.append("category_id = ?"); params.append(category_id)
        if is_template is not None:
            fields.append("is_template = ?"); params.append(int(is_template))
        if not fields:
            return
        sql = f"UPDATE transactions SET {', '.join(fields)} WHERE id = ?"
        params.append(txn_id)
        self.conn.execute(sql, params)
        self.conn.commit()

    def delete_transaction(self, txn_id: int):
        self.conn.execute("DELETE FROM transactions WHERE id = ?", (txn_id,))
        self.conn.commit()

# Δοκιμή του model
if __name__ == "__main__":
    db = Database(":memory:")
    db.add_category("Μισθός", "income", True)
    db.add_category("Τρόφιμα", "expense", False)
    db.add_transaction("2025-05-19", 1000, 1, True)
    db.add_transaction("2025-05-20", 50, 2, False)
    print("Categories:", db.get_all_categories())
    print("May 2025 txns:", db.get_transactions_by_month(2025, 5))

