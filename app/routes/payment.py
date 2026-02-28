# app/routes/payment.py (stub for Step 4; full logic in Step 5)
from flask import Blueprint

bp = Blueprint("payment", __name__)


@bp.route("/buy/confirm", methods=["POST"])
def confirm_payment():
    """Placeholder until Step 5: order creation and confirm.html."""
    return "Order confirmation (Step 5 will implement full flow).", 200
