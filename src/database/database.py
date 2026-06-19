import sqlite3
import os
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DATABASE_PATH")

def init_db():
    with sqlite3.connect(DB_PATH) as con:
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                nickname TEXT NOT NULL,
                username TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
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
                UPDATE sessions
                SET updated_at = CURRENT_TIMESTAMP
                WHERE session_id = NEW.session_id;
            END;          
        ''')

        con.commit()


def register_user(user_id: int, nickname: str, username: str = None):
    with sqlite3.connect(DB_PATH) as con:
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO users (user_id, nickname, username)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                nickname = excluded.nickname,
                username = excluded.username

        """, (user_id, nickname, username))
        con.commit()

def new_session(user_id: int) -> int:
    with sqlite3.connect(DB_PATH) as con:
        cursor = con.cursor()
        cursor.execute("INSERT INTO sessions (user_id) VALUES (?)", (user_id,))
        con.commit()
        return cursor.lastrowid

def get_last_session(user_id: int) -> int:
    with sqlite3.connect(DB_PATH) as con:
        cursor = con.cursor()
        
        cursor.execute("""
            SELECT session_id, updated_at
            FROM sessions
            WHERE user_id = ?
            ORDER BY session_id DESC
            LIMIT 1
        """, (user_id,))

        row = cursor.fetchone()
        if not row:
            return new_session(user_id)

        session_id, updated_at = row

        cursor.execute("""
            SELECT (julianday('now') - julianday(?)) * 24 > 2
        """, (updated_at,))

        is_expired = cursor.fetchone()[0]

        if is_expired:
            return new_session(user_id)

        return session_id

def save_message(session_id: int, role: str, text: str):
    with sqlite3.connect(DB_PATH) as con:
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO messages (session_id, role, text) VALUES (?, ?, ?)",
            (session_id, role, text)
        )
        con.commit()

def get_history(session_id: int) -> list[HumanMessage | AIMessage]:
    with sqlite3.connect(DB_PATH) as con:
        cursor = con.cursor()
        cursor.execute("""
            SELECT role, text
            FROM messages
            WHERE session_id = ?
            ORDER BY message_id ASC
        """, (session_id,))

        rows = cursor.fetchall()
        
        chat_history = []
        for role, text in rows:
            if role == "user":
                chat_history.append(HumanMessage(content=text))
            elif role == "assistant":
                chat_history.append(AIMessage(content=text))
                
        return chat_history
