"""SQLite layer: users + OTP tables."""
import os, sqlite3
from contextlib import contextmanager

DB_PATH = os.getenv("DB_PATH", "franchiseops.db")

@contextmanager
def conn():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    try:
        yield c
        c.commit()
    finally:
        c.close()

def init_db():
    with conn() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash BLOB NOT NULL,
            role TEXT NOT NULL DEFAULT 'staff',
            outlet TEXT,
            is_verified INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS otps (
            email TEXT NOT NULL,
            purpose TEXT NOT NULL,          -- 'signup' | 'login'
            otp_hash TEXT NOT NULL,
            expires_at REAL NOT NULL,
            attempts INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (email, purpose)
        );
        """)

def get_user(email):
    with conn() as c:
        return c.execute("SELECT * FROM users WHERE email=?", (email.lower(),)).fetchone()

def create_user(name, email, pw_hash, role, outlet, verified=0):
    with conn() as c:
        c.execute(
            "INSERT INTO users(name,email,password_hash,role,outlet,is_verified) VALUES(?,?,?,?,?,?)",
            (name, email.lower(), pw_hash, role, outlet, verified))

def delete_user(email):
    with conn() as c:
        c.execute("DELETE FROM users WHERE email=?", (email.lower(),))

def mark_verified(email):
    with conn() as c:
        c.execute("UPDATE users SET is_verified=1 WHERE email=?", (email.lower(),))

def save_otp(email, purpose, otp_hash, expires_at):
    with conn() as c:
        c.execute("REPLACE INTO otps(email,purpose,otp_hash,expires_at,attempts) VALUES(?,?,?,?,0)",
                  (email.lower(), purpose, otp_hash, expires_at))

def get_otp(email, purpose):
    with conn() as c:
        return c.execute("SELECT * FROM otps WHERE email=? AND purpose=?",
                         (email.lower(), purpose)).fetchone()

def bump_otp_attempts(email, purpose):
    with conn() as c:
        c.execute("UPDATE otps SET attempts=attempts+1 WHERE email=? AND purpose=?",
                  (email.lower(), purpose))

def delete_otp(email, purpose):
    with conn() as c:
        c.execute("DELETE FROM otps WHERE email=? AND purpose=?", (email.lower(), purpose))