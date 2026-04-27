import sqlite3
from pathlib import Path

DB_PATH = Path("reminders.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            time TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def get_next_reminder():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT title, time, timestamp
        FROM reminders
        ORDER BY timestamp ASC
        LIMIT 1
    """)

    row = c.fetchone()
    conn.close()

    if row:
        return {
            "title": row[0],
            "time": row[1],
            "timestamp": row[2]
        }
    else:
        return None


def add_reminder(title, time, timestamp):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        INSERT INTO reminders (title, time, timestamp)
        VALUES (?, ?, ?)
    """, (title, time, timestamp))

    conn.commit()
    conn.close()
