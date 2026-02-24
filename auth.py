# auth.py
import os
import sqlite3
from typing import Optional
from passlib.hash import bcrypt

DB_NAME = os.path.join(os.path.dirname(__file__), "users.db")


def bcrypt_safe_password(pw: str) -> str:
    """
    bcrypt has a 72-BYTE input limit. We safely truncate UTF-8 bytes to 72 and
    decode back to a string (dropping any partial characters).
    """
    return pw.encode("utf-8")[:72].decode("utf-8", errors="ignore")


def init_db() -> None:
    """Create required tables if they don't exist."""
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

        cur.execute("""
            CREATE TABLE IF NOT EXISTS connections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                email TEXT,
                company TEXT,
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        conn.commit()


def create_user(username: str, email: str, password: str) -> tuple[bool, str]:
    username = username.strip()
    email = email.strip()

    if not username or not email or not password:
        return False, "Username, email, and password are required."

    try:
        safe_pw = bcrypt_safe_password(password)
        password_hash = bcrypt.hash(safe_pw)

        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash),
            )
            conn.commit()

        return True, "Account created."

    except sqlite3.IntegrityError:
        return False, "Username or email already exists."

    except Exception as e:
        return False, f"Signup failed: {e}"


def verify_user(username: str, password: str) -> tuple[bool, str]:
    username = username.strip()
    if not username or not password:
        return False, "Username and password are required."

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


def get_user_id(username: str) -> Optional[int]:
    username = username.strip()
    if not username:
        return None

    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE username = ?", (username,))
        row = cur.fetchone()

    return row[0] if row else None


def get_user_email(username: str) -> Optional[str]:
    username = username.strip()
    if not username:
        return None

    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT email FROM users WHERE username = ?", (username,))
        row = cur.fetchone()

    return row[0] if row else None


def update_user_email(username: str, new_email: str) -> tuple[bool, str]:
    username = username.strip()
    new_email = new_email.strip()

    if not username:
        return False, "User not found."
    if not new_email:
        return False, "Email cannot be empty."

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE users SET email = ? WHERE username = ?",
                (new_email, username),
            )
            if cur.rowcount == 0:
                return False, "User not found."
            conn.commit()

        return True, "Email updated."

    except sqlite3.IntegrityError:
        return False, "That email is already in use."

    except Exception as e:
        return False, f"Update failed: {e}"


def add_connection(username: str, name: str, email: str, company: str, notes: str) -> tuple[bool, str]:
    username = username.strip()
    name = name.strip()
    email = (email or "").strip()
    company = (company or "").strip()
    notes = (notes or "").strip()

    if not username:
        return False, "User not found."
    if not name:
        return False, "Name is required."

    user_id = get_user_id(username)
    if user_id is None:
        return False, "User not found."

    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO connections (user_id, name, email, company, notes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, name, email, company, notes),
        )
        conn.commit()

    return True, "Connection added."


def list_connections(username: str) -> list[dict]:
    username = username.strip()
    user_id = get_user_id(username)
    if user_id is None:
        return []

    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, name, email, company, notes, created_at
            FROM connections
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,),
        )
        rows = cur.fetchall()

    return [
        {
            "id": r[0],
            "name": r[1],
            "email": r[2] or "",
            "company": r[3] or "",
            "notes": r[4] or "",
            "created_at": r[5],
        }
        for r in rows
    ]
# -----------------------------
# Resume (PDF) storage helpers
# -----------------------------
def _ensure_resumes_dir() -> str:
    resumes_dir = os.path.join(os.path.dirname(__file__), "resumes")
    os.makedirs(resumes_dir, exist_ok=True)
    return resumes_dir

def save_resume_pdf(username: str, file_bytes: bytes) -> tuple[bool, str]:
    username = username.strip()
    if not username:
        return False, "User not found."

    if not file_bytes:
        return False, "Empty file."

    path = os.path.join(_ensure_resumes_dir(), f"{username}.pdf")
    try:
        with open(path, "wb") as f:
            f.write(file_bytes)
        return True, "Resume uploaded."
    except Exception as e:
        return False, f"Upload failed: {e}"

def get_resume_pdf_path(username: str) -> Optional[str]:
    username = username.strip()
    if not username:
        return None

    path = os.path.join(_ensure_resumes_dir(), f"{username}.pdf")
    return path if os.path.exists(path) else None

def delete_resume_pdf(username: str) -> tuple[bool, str]:
    path = get_resume_pdf_path(username)
    if not path:
        return False, "No resume found."

    try:
        os.remove(path)
        return True, "Resume deleted."
    except Exception as e:
        return False, f"Delete failed: {e}"
    
def delete_connection(connection_id: int, username: str) -> tuple[bool, str]:
    user_id = get_user_id(username)
    if user_id is None:
        return False, "User not found."

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM connections WHERE id = ? AND user_id = ?",
                (connection_id, user_id),
            )
            if cur.rowcount == 0:
                return False, "Connection not found."
            conn.commit()
        return True, "Connection deleted."
    except Exception as e:
        return False, f"Delete failed: {e}"