# data/orders_data.py
from .database import get_connection


def create_order(customer_name: str, customer_phone: str, customer_address: str, total_amount: float) -> int:
    """Insert a new order and a PaymentStatus row; return order ID."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO Orders (CustomerName, CustomerPhone, CustomerAddress, TotalAmount)
        VALUES (?, ?, ?, ?)
        """,
        (customer_name, customer_phone, customer_address, total_amount),
    )
    order_id = cur.lastrowid
    cur.execute(
        "INSERT INTO PaymentStatus (OrderID, Status) VALUES (?, ?)",
        (order_id, "PENDING"),
    )
    conn.commit()
    conn.close()
    return order_id


def create_order_item(order_id: int, product_id: int, quantity: int, price: float) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO OrderItems (OrderID, ProductID, Quantity, Price) VALUES (?, ?, ?, ?)",
        (order_id, product_id, quantity, price),
    )
    conn.commit()
    conn.close()
