import sqlite3
import os

DB_PATH = "db/database.sqlite"

def init_db():
    os.makedirs("db", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            source     TEXT NOT NULL,
            name       TEXT NOT NULL,
            contact    TEXT NOT NULL,
            message    TEXT NOT NULL,
            status     TEXT DEFAULT 'new',
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        )
    """)
    conn.commit()
    conn.close()
    print("✅ База данных готова")

def save_lead(source, name, contact, message):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO leads (source, name, contact, message) VALUES (?, ?, ?, ?)",
        (source, name, contact, message)
    )
    conn.commit()
    conn.close()

def get_all_leads():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM leads ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]