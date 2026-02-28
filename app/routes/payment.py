# app/routes/payment.py
from flask import Blueprint, abort, redirect, render_template, request, session, url_for

from data.database import get_connection
from data.orders_data import create_order, create_order_item
from data.products_data import get_product

bp = Blueprint("payment", __name__)


def _get_cart_items(cart_id: int):
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


@bp.get("/buy/<int:product_id>")
def handle_payment(product_id):
    """Direct purchase form (no UI link; for parity with original)."""
    product = get_product(product_id)
    if not product:
        abort(404)
    return render_template("payment.html", product=product)


@bp.route("/buy/confirm", methods=["POST"])
def confirm_payment():
    if session.get("checkout_cart_id"):
        return _process_cart_checkout()
    return _process_direct_purchase()


def _process_cart_checkout():
    cart_id = session.get("checkout_cart_id")
    name = (session.get("checkout_name") or "").strip()
    phone = (session.get("checkout_phone") or "").strip()
    address = (session.get("checkout_address") or "").strip()

    if not (cart_id and name and phone and address):
        return redirect(url_for("cart.view_cart"))

    items = _get_cart_items(cart_id)
    if not items:
        return redirect(url_for("cart.view_cart"))

    total_amount = sum(item["line_total"] for item in items)
    order_id = create_order(
        customer_name=name,
        customer_phone=phone,
        customer_address=address,
        total_amount=total_amount,
    )
    for item in items:
        create_order_item(
            order_id=order_id,
            product_id=item["id"],
            quantity=item["quantity"],
            price=item["price"],
        )

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM CartItems WHERE CartID = ?", (cart_id,))
    cur.execute("DELETE FROM ShoppingCart WHERE CartID = ?", (cart_id,))
    conn.commit()
    conn.close()

    session.pop("checkout_cart_id", None)
    session.pop("checkout_name", None)
    session.pop("checkout_phone", None)
    session.pop("checkout_address", None)
    session.pop("cart_id", None)

    return render_template(
        "confirm.html",
        name=name,
        phone=phone,
        address=address,
        order_id=order_id,
        total_amount=total_amount,
        items=items,
    )


def _process_direct_purchase():
    name = (request.form.get("name") or "").strip()
    phone = (request.form.get("phone") or "").strip()
    address = (request.form.get("address") or "").strip()
    try:
        product_id = int(request.form.get("product_id"))
    except (TypeError, ValueError):
        abort(400)

    product = get_product(product_id)
    if not product:
        abort(404)
    if not (name and phone and address):
        abort(400)

    order_id = create_order(
        customer_name=name,
        customer_phone=phone,
        customer_address=address,
        total_amount=product["price"],
    )
    create_order_item(
        order_id=order_id,
        product_id=product_id,
        quantity=1,
        price=product["price"],
    )

    return render_template(
        "confirm.html",
        name=name,
        phone=phone,
        address=address,
        product=product,
        product_id=product_id,
        order_id=order_id,
        total_amount=product["price"],
    )
