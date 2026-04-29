import sqlite3
from pathlib import Path

DB_PATH = Path("reminders.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS button_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            type TEXT NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            time TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            notified INTEGER DEFAULT 0
        )
    """)

    # Migrate existing databases that lack the notified column
    try:
        c.execute("ALTER TABLE reminders ADD COLUMN notified INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass  # Column already exists

    conn.commit()
    conn.close()

def log_button_press(press_type):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        INSERT INTO button_logs (timestamp, type)
        VALUES (datetime('now'), ?)
    """, (press_type,))

    conn.commit()
    conn.close()


def get_next_reminder():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT id, title, time, timestamp
        FROM reminders
        WHERE notified = 0
        ORDER BY timestamp ASC
        LIMIT 1
    """)

    row = c.fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "title": row[1],
            "time": row[2],
            "timestamp": row[3]
        }
    else:
        return None


def get_pending_reminders():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT id, title, time, timestamp
        FROM reminders
        WHERE notified = 0
        ORDER BY timestamp ASC
    """)

    rows = c.fetchall()
    conn.close()

    return [
        {"id": row[0], "title": row[1], "time": row[2], "timestamp": row[3]}
        for row in rows
    ]


def mark_reminder_notified(reminder_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("UPDATE reminders SET notified = 1 WHERE id = ?", (reminder_id,))

    conn.commit()
    conn.close()


def add_reminder(title, time, timestamp):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        INSERT INTO reminders (title, time, timestamp)
        VALUES (?, ?, ?)
    """, (title, time, timestamp))

    conn.commit()
    conn.close()
