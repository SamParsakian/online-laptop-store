# data/products_data.py
from .database import get_connection


def get_all_products():
    conn = get_connection()
    cur = conn.cursor()
    rows = cur.execute("""
        SELECT ProductID, Name, Type, ProduceYear, Price, Total,
               Model, Cpu, Gpu, Motherboard, Ram, Description,
               (SELECT ImageURL FROM ProductImages
                WHERE ProductID = Product.ProductID ORDER BY ImageID DESC LIMIT 1) AS ImageURL
        FROM Product
    """).fetchall()
    conn.close()
    return [
        {
            "id": r[0], "name": r[1], "type": r[2], "year": r[3], "price": r[4], "total": r[5],
            "model": r[6], "cpu": r[7], "gpu": r[8], "motherboard": r[9], "ram": r[10],
            "description": r[11], "image_url": r[12],
        }
        for r in rows
    ]


def get_product(product_id):
    conn = get_connection()
    cur = conn.cursor()
    row = cur.execute("""
        SELECT ProductID, Name, Type, ProduceYear, Price, Total,
               Model, Cpu, Gpu, Motherboard, Ram, Description
        FROM Product WHERE ProductID = ?
    """, (product_id,)).fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row[0], "name": row[1], "type": row[2], "year": row[3], "price": row[4], "total": row[5],
        "model": row[6], "cpu": row[7], "gpu": row[8], "motherboard": row[9], "ram": row[10],
        "description": row[11],
    }
