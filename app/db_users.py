import sqlite3
from pathlib import Path

DB_PATH = Path("users.db")

# Создаём таблицу, если ещё нет
# conn = sqlite3.connect(DB_PATH)
# cursor = conn.cursor()
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         user_id INTEGER PRIMARY KEY,
#         first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     )
# """)
# conn.commit()

# def save_user(user_id: int):
#     cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
#     conn.commit()

# def get_total_users():
#     cursor.execute("SELECT COUNT(*) FROM users")
#     return cursor.fetchone()[0]

# def get_all_users():
#     cursor.execute("SELECT user_id FROM users")
#     return [row[0] for row in cursor.fetchall()]

from pathlib import Path
import sqlite3
from typing import List

DB_PATH = Path("users.db")

# Для простоты ставим check_same_thread=False — удобно для асинхронного приложения
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

def get_all_user_names():
    cursor.execute("SELECT first_name, last_name FROM users")
    return cursor.fetchall()

# def save_user(user_id: int, first_name: str, last_name: str):
#     cursor.execute("""
#         INSERT OR IGNORE INTO users (user_id, first_name, last_name)
#         VALUES (?, ?, ?)
#     """, (user_id, first_name, last_name))
#     conn.commit()

def save_user(user_id: int, first_name: str, last_name: str):
    cursor.execute("""
        INSERT INTO users (user_id, first_name, last_name)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            first_name=excluded.first_name,
            last_name=excluded.last_name
    """, (user_id, first_name, last_name))
    conn.commit()

def get_total_users() -> int:
    cursor.execute("SELECT COUNT(*) FROM users")
    row = cursor.fetchone()
    return row[0] if row else 0

def get_all_users() -> List[int]:
    cursor.execute("SELECT user_id FROM users")
    return [r[0] for r in cursor.fetchall()]

def close_db():
    cursor.close()
    conn.close()

