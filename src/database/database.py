import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DATABASE_PATH")

def init_db(db_path: str):
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                role TEXT NOT NULL,
                text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
            )
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_messages_session_id 
            ON messages(session_id);
        ''')

        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS update_session_timestamp
            AFTER INSERT ON messages
            BEGIN
                UPDATE session
                SET updated_at = CURRENT_TIMESTAMP
                WHERE session_id = NEW.session_id;
            END;          
        ''')

        con.commit()

def create_session() -> int:
    with sqlite3.connect(DB_PATH) as con:
        cursor = con.cursor()
        cursor.execute("INSERT INTO sessions DEFAULT VALUES")
        con.commit()
        return cursor.lastrowid()

def add_message(session_id: int, role: str, text: str):
    with sqlite3.connect(DB_PATH) as con:
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO messages (session_id, role, text) VALUES (?, ?, ?)",
            (session_id, role, text)
        )
        con.commit()