# app/routes/cart.py
"""Cart management routes."""
from uuid import uuid4

from flask import Blueprint, redirect, render_template, request, session, url_for

from data.database import get_connection
from data.products_data import get_product

bp = Blueprint("cart", __name__)


def _ensure_session_token():
    token = session.get("session_token")
    if not token:
        token = str(uuid4())
        session["session_token"] = token
    return token


def _get_or_create_cart_id():
    cart_id = session.get("cart_id")
    conn = get_connection()
    cur = conn.cursor()
    if cart_id:
        row = cur.execute("SELECT CartID FROM ShoppingCart WHERE CartID = ?", (cart_id,)).fetchone()
        if row:
            conn.close()
            return cart_id
    session_token = _ensure_session_token()
    cur.execute("INSERT INTO ShoppingCart (SessionID) VALUES (?)", (session_token,))
    cart_id = cur.lastrowid
    conn.commit()
    conn.close()
    session["cart_id"] = cart_id
    return cart_id


def _get_cart_items(cart_id):
    conn = get_connection()
    cur = conn.cursor()
    rows = cur.execute(
        """
        SELECT ci.CartItemID, p.ProductID, p.Name, p.Price, ci.Quantity,
               (p.Price * ci.Quantity) AS LineTotal
        FROM CartItems ci
        JOIN Product p ON p.ProductID = ci.ProductID
        WHERE ci.CartID = ?
        """,
        (cart_id,),
    ).fetchall()
    conn.close()
    return [
        {"cart_item_id": r[0], "id": r[1], "name": r[2], "price": r[3], "quantity": r[4], "line_total": r[5]}
        for r in rows
    ]


@bp.get("/cart/add/<int:product_id>")
def add_to_cart(product_id):
    product = get_product(product_id)
    if not product:
        return redirect(url_for("products.list_products"))
    cart_id = _get_or_create_cart_id()
    conn = get_connection()
    cur = conn.cursor()
    existing = cur.execute(
        "SELECT CartItemID, Quantity FROM CartItems WHERE CartID = ? AND ProductID = ?",
        (cart_id, product_id),
    ).fetchone()
    if existing:
        cur.execute("UPDATE CartItems SET Quantity = Quantity + 1 WHERE CartItemID = ?", (existing[0],))
    else:
        cur.execute("INSERT INTO CartItems (CartID, ProductID, Quantity) VALUES (?, ?, ?)", (cart_id, product_id, 1))
    conn.commit()
    conn.close()
    return redirect(url_for("products.product_details", product_id=product_id))


@bp.get("/cart")
def view_cart():
    cart_id = _get_or_create_cart_id()
    items = _get_cart_items(cart_id)
    cart_total = sum(item["line_total"] for item in items)
    return render_template("cart.html", items=items, cart_total=cart_total)


@bp.get("/cart/remove/<int:cart_item_id>")
def remove_from_cart(cart_item_id):
    cart_id = _get_or_create_cart_id()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM CartItems WHERE CartItemID = ? AND CartID = ?", (cart_item_id, cart_id))
    conn.commit()
    conn.close()
    return redirect(url_for("cart.view_cart"))


@bp.get("/checkout")
def checkout():
    cart_id = _get_or_create_cart_id()
    items = _get_cart_items(cart_id)
    if not items:
        return redirect(url_for("cart.view_cart"))
    cart_total = sum(item["line_total"] for item in items)
    return render_template("checkout.html", items=items, cart_total=cart_total)


@bp.post("/checkout")
def process_checkout():
    cart_id = _get_or_create_cart_id()
    items = _get_cart_items(cart_id)
    if not items:
        return redirect(url_for("cart.view_cart"))
    session["checkout_cart_id"] = cart_id
    session["checkout_name"] = request.form.get("name", "")
    session["checkout_phone"] = request.form.get("phone", "")
    session["checkout_address"] = request.form.get("address", "")
    return redirect(url_for("payment.confirm_payment"), code=307)
