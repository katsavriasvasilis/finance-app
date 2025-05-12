from src.db import get_conn
from typing import List, Dict, Any

def create_category(name: str, type_: str, is_monthly: bool=False):
    conn = get_conn()
    with conn:
        cur = conn.execute(
            "INSERT INTO categories (name, type, is_monthly) VALUES (?, ?, ?)",
            (name, type_, int(is_monthly))
        )
    return cur.lastrowid

def list_categories() -> List[Dict[str, Any]]:
    conn = get_conn()
    rows = conn.execute("SELECT * FROM categories").fetchall()
    conn.close()
    return [dict(r) for r in rows]

# Πρόσθεσε συναρτήσεις για update/delete ανάλογα
