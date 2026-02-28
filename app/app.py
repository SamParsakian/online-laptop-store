"""Flask application entry point."""
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, render_template

# Load .env from project root
_root = Path(__file__).resolve().parent.parent
load_dotenv(_root / ".env")

from data.database import init_db

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-me")

init_db()


@app.get("/")
def home():
    """Simple home page."""
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
