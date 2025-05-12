import sqlite3
from sqlite3 import Connection

def get_conn(db_path: str = "data/finance.db") -> Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path: str = "data/finance.db"):
    sql_create_categories = """
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT CHECK(type IN ('income','expense')) NOT NULL,
        is_monthly INTEGER NOT NULL DEFAULT 0
    );"""
    sql_create_transactions = """
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        category_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        description TEXT,
        FOREIGN KEY(category_id) REFERENCES categories(id)
    );"""
    conn = get_conn(db_path)
    with conn:
        conn.execute(sql_create_categories)
        conn.execute(sql_create_transactions)
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Initialized database at", "data/finance.db")


