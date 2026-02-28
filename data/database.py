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


def _upgrade_6_to_17(cur, conn):
    """When DB has exactly 6 products (old seed), add 11 more and fix image variety."""
    cur.execute("UPDATE ProductImages SET ImageURL = '/static/img/laptop-02.jpg', AltText = 'HP Pavilion Image' WHERE ProductID = 4")
    cur.execute("UPDATE ProductImages SET ImageURL = '/static/img/laptop-03.jpg', AltText = 'Asus Zenbook Image' WHERE ProductID = 5")
    cur.execute("UPDATE ProductImages SET ImageURL = '/static/img/laptop-04.jpg', AltText = 'Lenovo IdeaPad Image' WHERE ProductID = 6")
    cur.executescript("""
        INSERT INTO Product (Name, Type, ProduceYear, Price, Total, Model, Cpu, Gpu, Motherboard, Ram, Description)
        VALUES
        ('Acer Swift 3', 'Laptop', 2023, 699, 14, 'SF314-512', 'Intel i5', 'Intel Iris', 'Acer Board', '8GB', 'Thin and light'),
        ('MSI Modern 14', 'Laptop', 2023, 949, 9, 'B14', 'Intel i5', 'Intel Iris', 'MSI Board', '16GB', 'Professional style'),
        ('Razer Blade 14', 'Laptop', 2023, 1899, 5, 'RZ09-0482', 'AMD Ryzen 9', 'NVIDIA RTX 4060', 'Razer Board', '16GB', 'Gaming performance'),
        ('LG Gram 17', 'Laptop', 2023, 1599, 7, '17Z90Q', 'Intel i7', 'Intel Iris', 'LG Board', '16GB', 'Large lightweight display'),
        ('Surface Laptop 5', 'Laptop', 2023, 1299, 11, 'Surface Laptop 5', 'Intel i5', 'Intel Iris', 'Microsoft Board', '8GB', 'Premium Windows experience'),
        ('Framework Laptop 13', 'Laptop', 2023, 1099, 8, 'Framework 13', 'Intel i5', 'Intel Iris', 'Framework Board', '8GB', 'Repairable and upgradeable'),
        ('HP EliteBook 840', 'Laptop', 2023, 1349, 10, 'EliteBook 840 G10', 'Intel i5', 'Intel Iris', 'HP Board', '16GB', 'Enterprise reliability'),
        ('Dell Inspiron 15', 'Laptop', 2022, 599, 18, 'Inspiron 3520', 'Intel i3', 'Intel UHD', 'Dell Board', '8GB', 'Affordable everyday use'),
        ('Lenovo Slim 7', 'Laptop', 2023, 1149, 8, 'Slim 7 14', 'AMD Ryzen 7', 'AMD Radeon', 'Lenovo Board', '16GB', 'Balanced performance'),
        ('Asus VivoBook 15', 'Laptop', 2022, 549, 22, 'X1504', 'Intel i3', 'Intel UHD', 'Asus Board', '8GB', 'Entry-level value'),
        ('MacBook Pro 14', 'Laptop', 2023, 1999, 6, 'Pro 14 M3', 'Apple M3', 'Integrated', 'Apple Board', '18GB', 'Pro power and portability');
        INSERT INTO ProductImages (ProductID, ImageURL, AltText) VALUES
        (7, '/static/img/laptop-05.jpg', 'Acer Swift Image'),
        (8, '/static/img/laptop-06.jpg', 'MSI Modern Image'),
        (9, '/static/img/laptop-07.jpg', 'Razer Blade Image'),
        (10, '/static/img/x1.jpg', 'LG Gram Image'),
        (11, '/static/img/airm2.jpg', 'Surface Laptop Image'),
        (12, '/static/img/xps13.jpg', 'Framework Laptop Image'),
        (13, '/static/img/laptop-02.jpg', 'HP EliteBook Image'),
        (14, '/static/img/laptop-03.jpg', 'Dell Inspiron Image'),
        (15, '/static/img/laptop-04.jpg', 'Lenovo Slim Image'),
        (16, '/static/img/laptop-05.jpg', 'Asus VivoBook Image'),
        (17, '/static/img/laptop-06.jpg', 'MacBook Pro Image');
    """)
    conn.commit()


def init_db():
    """Create tables from schema and seed if Product table is empty. Sync admin from env."""
    conn = get_connection()
    cur = conn.cursor()

    cur.executescript(SCHEMA_PATH.read_text())
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM Product;")
    n = cur.fetchone()[0]
    if n == 0 and SEED_PATH.exists():
        cur.executescript(SEED_PATH.read_text())
        conn.commit()
    elif n == 6:
        _upgrade_6_to_17(cur, conn)

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
