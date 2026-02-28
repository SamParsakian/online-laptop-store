# app/routes/admin.py
"""Admin login, logout, and admin tools."""
import sqlite3

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from data.database import get_connection

bp = Blueprint("admin", __name__, url_prefix="/admin")

_ORDER_STATUSES = {"PENDING", "PROCESSING", "SHIPPED"}


def _require_admin():
    if not session.get("admin_logged"):
        return redirect(url_for("admin_panel"))
    return None


def _valid_admin_credentials(username: str, password: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    row = cur.execute(
        "SELECT AdminID FROM Admin WHERE Username = ? AND Password = ?",
        (username, password),
    ).fetchone()
    conn.close()
    return bool(row)


def _get_product(product_id: int):
    conn = get_connection()
    cur = conn.cursor()
    row = cur.execute(
        """SELECT ProductID, Name, Type, ProduceYear, Price, Total,
           Model, Cpu, Gpu, Motherboard, Ram, Description FROM Product WHERE ProductID = ?""",
        (product_id,),
    ).fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row[0], "name": row[1], "type": row[2], "year": row[3], "price": row[4], "total": row[5],
        "model": row[6], "cpu": row[7], "gpu": row[8], "motherboard": row[9], "ram": row[10], "description": row[11],
    }


def _get_order(order_id: int):
    conn = get_connection()
    cur = conn.cursor()
    row = cur.execute(
        """SELECT OrderID, CustomerName, CustomerPhone, CustomerAddress, OrderDate, TotalAmount, Status
           FROM Orders WHERE OrderID = ?""",
        (order_id,),
    ).fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row[0], "customer": row[1], "phone": row[2], "address": row[3],
        "date": row[4], "total": row[5], "status": row[6],
    }


def _product_form_payload(form):
    name = form.get("name", "").strip()
    ptype = form.get("type", "").strip()
    model = form.get("model", "").strip()
    cpu = form.get("cpu", "").strip()
    gpu = form.get("gpu", "").strip()
    motherboard = form.get("motherboard", "").strip()
    ram = form.get("ram", "").strip()
    desc = form.get("description", "").strip()
    if not name or not ptype:
        raise ValueError("Name and Type are required")
    try:
        year = int(form.get("year", 0))
        total = int(form.get("total", 0))
        price = float(form.get("price", 0))
    except ValueError:
        raise ValueError("Year, Total, and Price must be numeric")
    return {
        "name": name, "type": ptype, "year": year, "price": price, "total": total,
        "model": model, "cpu": cpu, "gpu": gpu, "motherboard": motherboard, "ram": ram, "description": desc,
    }


# --- Login / Logout ---
@bp.post("/login")
def login():
    u = request.form.get("username", "")
    p = request.form.get("password", "")
    if not u or not p:
        flash("Username and password are required", "error")
        return redirect(url_for("admin_panel"))
    if _valid_admin_credentials(u, p):
        session["admin_logged"] = True
        return redirect(url_for("admin_dashboard"))
    flash("Wrong login", "error")
    return redirect(url_for("admin_panel"))


@bp.get("/logout")
def logout():
    session.clear()
    return redirect("/")


# --- New admin ---
@bp.get("/admins/new")
def admin_new_form():
    if _require_admin():
        return _require_admin()
    return render_template("admin_new_admin.html")


@bp.post("/admins/new")
def admin_new_save():
    if _require_admin():
        return _require_admin()
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    if not username or not password:
        flash("Username and password are required", "error")
        return redirect(url_for("admin.admin_new_form"))
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO Admin (Username, Password) VALUES (?, ?)", (username, password))
        conn.commit()
        flash("Admin user created", "success")
    except sqlite3.IntegrityError:
        flash("Username already exists", "error")
    finally:
        conn.close()
    return redirect(url_for("admin.admin_new_form"))


# --- Products ---
@bp.get("/products")
def products_list():
    if _require_admin():
        return _require_admin()
    conn = get_connection()
    cur = conn.cursor()
    rows = cur.execute(
        """SELECT ProductID, Name, Type, ProduceYear, Price, Total, Model, Cpu, Gpu, Motherboard, Ram, Description
           FROM Product ORDER BY ProductID DESC"""
    ).fetchall()
    conn.close()
    products = [
        {"id": r[0], "name": r[1], "type": r[2], "year": r[3], "price": r[4], "total": r[5],
         "model": r[6], "cpu": r[7], "gpu": r[8], "motherboard": r[9], "ram": r[10], "description": r[11]}
        for r in rows
    ]
    return render_template("admin_products.html", products=products)


@bp.get("/products/new")
def product_new_form():
    if _require_admin():
        return _require_admin()
    return render_template("admin_product_form.html", product=None, mode="new")


@bp.post("/products/new")
def product_new_save():
    if _require_admin():
        return _require_admin()
    try:
        payload = _product_form_payload(request.form)
    except ValueError as e:
        flash(str(e), "error")
        return redirect(url_for("admin.product_new_form"))
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO Product (Name, Type, ProduceYear, Price, Total, Model, Cpu, Gpu, Motherboard, Ram, Description)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (payload["name"], payload["type"], payload["year"], payload["price"], payload["total"],
         payload["model"], payload["cpu"], payload["gpu"], payload["motherboard"], payload["ram"], payload["description"]),
    )
    conn.commit()
    conn.close()
    flash("Product created", "success")
    return redirect(url_for("admin.products_list"))


@bp.get("/products/<int:product_id>/edit")
def product_edit_form(product_id):
    if _require_admin():
        return _require_admin()
    product = _get_product(product_id)
    if not product:
        flash("Product not found", "error")
        return redirect(url_for("admin.products_list"))
    return render_template("admin_product_form.html", product=product, mode="edit")


@bp.post("/products/<int:product_id>/edit")
def product_edit_save(product_id):
    if _require_admin():
        return _require_admin()
    product = _get_product(product_id)
    if not product:
        flash("Product not found", "error")
        return redirect(url_for("admin.products_list"))
    try:
        payload = _product_form_payload(request.form)
    except ValueError as e:
        flash(str(e), "error")
        return redirect(url_for("admin.product_edit_form", product_id=product_id))
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """UPDATE Product SET Name=?, Type=?, ProduceYear=?, Price=?, Total=?, Model=?, Cpu=?, Gpu=?, Motherboard=?, Ram=?, Description=?
           WHERE ProductID=?""",
        (payload["name"], payload["type"], payload["year"], payload["price"], payload["total"],
         payload["model"], payload["cpu"], payload["gpu"], payload["motherboard"], payload["ram"], payload["description"], product_id),
    )
    conn.commit()
    conn.close()
    flash("Product updated", "success")
    return redirect(url_for("admin.products_list"))


@bp.post("/products/<int:product_id>/delete")
def product_delete(product_id):
    if _require_admin():
        return _require_admin()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Product WHERE ProductID = ?", (product_id,))
    conn.commit()
    conn.close()
    flash("Product deleted", "success")
    return redirect(url_for("admin.products_list"))


@bp.get("/products/<int:product_id>/images")
def product_images(product_id):
    if _require_admin():
        return _require_admin()
    product = _get_product(product_id)
    if not product:
        flash("Product not found", "error")
        return redirect(url_for("admin.products_list"))
    conn = get_connection()
    cur = conn.cursor()
    rows = cur.execute(
        "SELECT ImageID, ImageURL, AltText FROM ProductImages WHERE ProductID = ? ORDER BY ImageID DESC",
        (product_id,),
    ).fetchall()
    conn.close()
    images = [{"id": r[0], "url": r[1], "alt": r[2] or ""} for r in rows]
    return render_template("admin_product_images.html", product=product, images=images)


@bp.post("/products/<int:product_id>/images")
def product_images_add(product_id):
    if _require_admin():
        return _require_admin()
    product = _get_product(product_id)
    if not product:
        flash("Product not found", "error")
        return redirect(url_for("admin.products_list"))
    url = request.form.get("image_url", "").strip()
    alt = request.form.get("alt_text", "").strip()
    if not url:
        flash("Image URL is required", "error")
        return redirect(url_for("admin.product_images", product_id=product_id))
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO ProductImages (ProductID, ImageURL, AltText) VALUES (?, ?, ?)", (product_id, url, alt))
    conn.commit()
    conn.close()
    flash("Image added", "success")
    return redirect(url_for("admin.product_images", product_id=product_id))


@bp.post("/products/<int:product_id>/images/<int:image_id>/delete")
def product_images_delete(product_id, image_id):
    if _require_admin():
        return _require_admin()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM ProductImages WHERE ImageID = ? AND ProductID = ?", (image_id, product_id))
    conn.commit()
    conn.close()
    flash("Image removed", "success")
    return redirect(url_for("admin.product_images", product_id=product_id))


# --- Orders ---
@bp.get("/orders")
def orders_list():
    if _require_admin():
        return _require_admin()
    conn = get_connection()
    cur = conn.cursor()
    rows = cur.execute(
        """SELECT OrderID, CustomerName, CustomerPhone, CustomerAddress, OrderDate, TotalAmount, Status
           FROM Orders ORDER BY OrderID DESC"""
    ).fetchall()
    conn.close()
    orders = [
        {"id": r[0], "customer": r[1], "phone": r[2], "address": r[3], "date": r[4], "total": r[5], "status": r[6]}
        for r in rows
    ]
    return render_template("admin_orders.html", orders=orders, statuses=sorted(_ORDER_STATUSES))


@bp.get("/orders/<int:order_id>")
def order_detail(order_id):
    if _require_admin():
        return _require_admin()
    order = _get_order(order_id)
    if not order:
        flash("Order not found", "error")
        return redirect(url_for("admin.orders_list"))
    conn = get_connection()
    cur = conn.cursor()
    rows = cur.execute(
        """SELECT oi.OrderItemID, oi.ProductID, p.Name, oi.Quantity, oi.Price
           FROM OrderItems oi LEFT JOIN Product p ON p.ProductID = oi.ProductID WHERE oi.OrderID = ?""",
        (order_id,),
    ).fetchall()
    conn.close()
    items = [
        {"id": r[0], "product_id": r[1], "name": r[2] or "(deleted product)", "qty": r[3], "price": r[4], "subtotal": r[3] * r[4]}
        for r in rows
    ]
    return render_template("admin_order_detail.html", order=order, items=items, statuses=sorted(_ORDER_STATUSES))


@bp.post("/orders/<int:order_id>/status")
def order_update_status(order_id):
    if _require_admin():
        return _require_admin()
    new_status = request.form.get("status", "").upper()
    if new_status not in _ORDER_STATUSES:
        flash("Invalid status", "error")
        return redirect(url_for("admin.order_detail", order_id=order_id))
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Orders SET Status = ? WHERE OrderID = ?", (new_status, order_id))
    conn.commit()
    conn.close()
    flash("Order status updated", "success")
    return redirect(url_for("admin.order_detail", order_id=order_id))


# --- Payments ---
@bp.get("/payments")
def payments_list():
    if _require_admin():
        return _require_admin()
    conn = get_connection()
    cur = conn.cursor()
    rows = cur.execute(
        """SELECT ps.PaymentID, ps.OrderID, ps.Status, ps.BankRef, ps.PaidAt, ps.AdminApproved, o.CustomerName, o.TotalAmount
           FROM PaymentStatus ps JOIN Orders o ON o.OrderID = ps.OrderID ORDER BY ps.PaymentID DESC"""
    ).fetchall()
    conn.close()
    payments = [
        {"id": r[0], "order_id": r[1], "status": r[2], "bank_ref": r[3], "paid_at": r[4],
         "approved": bool(r[5]), "customer": r[6], "total": r[7]}
        for r in rows
    ]
    return render_template("admin_payments.html", payments=payments)


@bp.post("/payments/<int:payment_id>/approve")
def payment_approve(payment_id):
    if _require_admin():
        return _require_admin()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE PaymentStatus SET AdminApproved = 1 WHERE PaymentID = ?", (payment_id,))
    conn.commit()
    conn.close()
    flash("Payment approved", "success")
    return redirect(url_for("admin.payments_list"))
