# data/database.py
import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv

_DATA_DIR = Path(__file__).resolve().parent
_ROOT_DIR = _DATA_DIR.parent


def _load_env():
    """Load .env from project root."""
    load_dotenv(_ROOT_DIR / ".env")


_load_env()

DB_PATH = _DATA_DIR / "shop.db"
SCHEMA_PATH = _DATA_DIR / "schema.sql"
SEED_PATH = _DATA_DIR / "seed.sql"


def get_connection():
    """Return a DB connection with foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create tables from schema and seed if Product table is empty. Sync admin from env."""
    conn = get_connection()
    cur = conn.cursor()

    cur.executescript(SCHEMA_PATH.read_text())
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM Product;")
    if cur.fetchone()[0] == 0 and SEED_PATH.exists():
        cur.executescript(SEED_PATH.read_text())
        conn.commit()

    _load_env()
    admin_user = (os.getenv("ADMIN_USER") or "admin").strip() or "admin"
    admin_pass = (os.getenv("ADMIN_PASS") or "1234").strip() or "1234"
    cur.execute("SELECT AdminID FROM Admin WHERE Username = ?", (admin_user,))
    if cur.fetchone() is None:
        cur.execute("INSERT INTO Admin (Username, Password) VALUES (?, ?)", (admin_user, admin_pass))
        conn.commit()
    else:
        cur.execute("UPDATE Admin SET Password = ? WHERE Username = ?", (admin_pass, admin_user))
        conn.commit()

    conn.close()
