# auth.py
import os
import sqlite3
from passlib.hash import bcrypt

DB_NAME = os.path.join(os.path.dirname(__file__), "users.db")


def bcrypt_safe_password(pw: str) -> str:
    # bcrypt limit is 72 BYTES (utf-8). This enforces it safely.
    return pw.encode("utf-8")[:72].decode("utf-8", errors="ignore")


def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)
        conn.commit()


def create_user(username: str, email: str, password: str) -> tuple[bool, str]:
    try:
        safe_pw = bcrypt_safe_password(password)
        password_hash = bcrypt.hash(safe_pw)

        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            conn.commit()

        return True, "Account created."

    except sqlite3.IntegrityError:
        return False, "Username or email already exists."

    except Exception as e:
        return False, f"Signup failed: {e}"


def verify_user(username: str, password: str) -> tuple[bool, str]:
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        row = cur.fetchone()

    if not row:
        return False, "User not found."

    password_hash = row[0]
    safe_pw = bcrypt_safe_password(password)

    if bcrypt.verify(safe_pw, password_hash):
        return True, "Login successful."

    return False, "Incorrect password."