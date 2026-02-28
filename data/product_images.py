# data/product_images.py
from .database import get_connection


def get_images_for_product(product_id):
    conn = get_connection()
    cur = conn.cursor()
    rows = cur.execute(
        "SELECT ImageID, ImageURL, AltText FROM ProductImages WHERE ProductID = ?",
        (product_id,),
    ).fetchall()
    conn.close()
    return [{"id": r[0], "url": r[1], "alt": r[2] or ""} for r in rows]
