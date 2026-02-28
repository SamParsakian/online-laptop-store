"""Flask application entry point."""
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, session, url_for

# Load .env from project root
_root = Path(__file__).resolve().parent.parent
load_dotenv(_root / ".env")

from data.database import init_db
from app.routes.products import bp as products_bp
from app.routes.cart import bp as cart_bp
from app.routes.payment import bp as payment_bp
from app.routes.admin import bp as admin_bp

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-me")

init_db()
app.register_blueprint(products_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(admin_bp)


@app.get("/")
def home():
    """Simple home page."""
    return render_template("home.html")


@app.get("/admin")
def admin_panel():
    if session.get("admin_logged"):
        return redirect(url_for("admin_dashboard"))
    return render_template("admin_login.html")


@app.get("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_logged"):
        return redirect(url_for("admin_panel"))
    return render_template("admin_dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
