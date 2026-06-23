"""
database.py — SQLite database layer for Vehicle Spare Parts Store Management System
Handles all DB creation, CRUD operations, and queries.
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "spare_parts.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row          # lets us access columns by name
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database():
    """Create all tables if they don't exist yet."""
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS parts (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    NOT NULL,
                category    TEXT    NOT NULL,
                manufacturer TEXT   NOT NULL,
                quantity    INTEGER NOT NULL DEFAULT 0,
                price       REAL    NOT NULL DEFAULT 0.0,
                low_stock_threshold INTEGER NOT NULL DEFAULT 5,
                created_at  TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
                updated_at  TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
            );

            CREATE TABLE IF NOT EXISTS sales (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name   TEXT    NOT NULL,
                total_amount    REAL    NOT NULL DEFAULT 0.0,
                sale_date       TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
            );

            CREATE TABLE IF NOT EXISTS sale_items (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id     INTEGER NOT NULL REFERENCES sales(id) ON DELETE CASCADE,
                part_id     INTEGER NOT NULL REFERENCES parts(id),
                part_name   TEXT    NOT NULL,
                quantity    INTEGER NOT NULL,
                unit_price  REAL    NOT NULL,
                subtotal    REAL    NOT NULL
            );
        """)


# ─────────────────────────── PARTS CRUD ────────────────────────────

def add_part(name, category, manufacturer, quantity, price, low_stock_threshold=5):
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO parts (name, category, manufacturer, quantity, price, low_stock_threshold)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (name, category, manufacturer, quantity, price, low_stock_threshold)
        )


def get_all_parts():
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM parts ORDER BY name"
        ).fetchall()


def search_parts(query):
    """Search by name, category, or ID."""
    q = f"%{query}%"
    with get_connection() as conn:
        return conn.execute(
            """SELECT * FROM parts
               WHERE name LIKE ? OR category LIKE ? OR CAST(id AS TEXT) LIKE ?
               ORDER BY name""",
            (q, q, q)
        ).fetchall()


def get_part_by_id(part_id):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM parts WHERE id = ?", (part_id,)
        ).fetchone()


def update_part(part_id, name, category, manufacturer, quantity, price, low_stock_threshold=5):
    with get_connection() as conn:
        conn.execute(
            """UPDATE parts
               SET name=?, category=?, manufacturer=?, quantity=?, price=?,
                   low_stock_threshold=?, updated_at=datetime('now','localtime')
               WHERE id=?""",
            (name, category, manufacturer, quantity, price, low_stock_threshold, part_id)
        )


def delete_part(part_id):
    with get_connection() as conn:
        # A part that has been sold before still has rows in sale_items.
        # Hard-deleting it would violate the FOREIGN KEY constraint and
        # would also corrupt historical bills, so we block it with a
        # clear, catchable error instead of letting SQLite crash the app.
        used = conn.execute(
            "SELECT COUNT(*) AS cnt FROM sale_items WHERE part_id = ?", (part_id,)
        ).fetchone()["cnt"]

        if used > 0:
            raise ValueError(
                f"This part cannot be deleted because it appears in {used} "
                f"past sale record(s). Deleting it would corrupt sales history.\n\n"
                f"Instead, you can edit the part and set its quantity to 0 to "
                f"remove it from active stock."
            )

        conn.execute("DELETE FROM parts WHERE id = ?", (part_id,))


def get_low_stock_parts():
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM parts WHERE quantity <= low_stock_threshold ORDER BY quantity"
        ).fetchall()


# ─────────────────────────── SALES ────────────────────────────────

def create_sale(customer_name, cart_items):
    """
    cart_items: list of dicts
        { 'part_id': int, 'part_name': str, 'quantity': int, 'unit_price': float }
    Returns the new sale_id, or raises on error.
    """
    if not cart_items:
        raise ValueError("Cart is empty.")

    total = sum(item["quantity"] * item["unit_price"] for item in cart_items)

    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO sales (customer_name, total_amount) VALUES (?, ?)",
            (customer_name, total)
        )
        sale_id = cur.lastrowid

        for item in cart_items:
            subtotal = item["quantity"] * item["unit_price"]
            conn.execute(
                """INSERT INTO sale_items (sale_id, part_id, part_name, quantity, unit_price, subtotal)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (sale_id, item["part_id"], item["part_name"],
                 item["quantity"], item["unit_price"], subtotal)
            )
            # Deduct stock
            conn.execute(
                """UPDATE parts
                   SET quantity = quantity - ?, updated_at=datetime('now','localtime')
                   WHERE id = ?""",
                (item["quantity"], item["part_id"])
            )

    return sale_id


def get_all_sales():
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM sales ORDER BY sale_date DESC"
        ).fetchall()


def search_sales(query):
    """Search sales by customer name or sale ID."""
    q = f"%{query}%"
    with get_connection() as conn:
        return conn.execute(
            """SELECT * FROM sales
               WHERE customer_name LIKE ? OR CAST(id AS TEXT) LIKE ?
               ORDER BY sale_date DESC""",
            (q, q)
        ).fetchall()


def get_sale_items(sale_id):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM sale_items WHERE sale_id = ?", (sale_id,)
        ).fetchall()


def get_sale_by_id(sale_id):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM sales WHERE id = ?", (sale_id,)
        ).fetchone()


# ─────────────────────────── DASHBOARD STATS ──────────────────────

def get_dashboard_stats():
    with get_connection() as conn:
        parts_types = conn.execute(
            "SELECT COUNT(DISTINCT category) AS cnt FROM parts"
        ).fetchone()["cnt"]

        total_stock = conn.execute(
            "SELECT COALESCE(SUM(quantity), 0) AS cnt FROM parts"
        ).fetchone()["cnt"]

        inventory_value = conn.execute(
            "SELECT COALESCE(SUM(quantity * price), 0) AS val FROM parts"
        ).fetchone()["val"]

        total_revenue = conn.execute(
            "SELECT COALESCE(SUM(total_amount), 0) AS rev FROM sales"
        ).fetchone()["rev"]

        recent_sales = conn.execute(
            "SELECT * FROM sales ORDER BY sale_date DESC LIMIT 5"
        ).fetchall()

        low_stock = get_low_stock_parts()

    return {
        "parts_types": parts_types,
        "total_stock": total_stock,
        "inventory_value": inventory_value,
        "total_revenue": total_revenue,
        "recent_sales": recent_sales,
        "low_stock": low_stock,
    }


def get_sales_history_stats():
    with get_connection() as conn:
        total_sales = conn.execute(
            "SELECT COUNT(*) AS cnt FROM sales"
        ).fetchone()["cnt"]

        total_revenue = conn.execute(
            "SELECT COALESCE(SUM(total_amount), 0) AS rev FROM sales"
        ).fetchone()["rev"]

    return {
        "total_sales": total_sales,
        "total_revenue": total_revenue,
    }
