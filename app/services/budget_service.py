from app.extensions import mysql
from datetime import datetime


def add_budget(user_id, category_id, amount, month):
    cur = mysql.connection.cursor()

    # Insert or update if already exists
    cur.execute("""
        INSERT INTO budgets (user_id, category_id, amount, month)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE amount = VALUES(amount)
    """, (user_id, category_id, amount, month))

    mysql.connection.commit()
    cur.close()

    return {"message": "Budget saved successfully"}, 201


def get_budget_progress(user_id, month):
    cur = mysql.connection.cursor()

    # Get budgets
    cur.execute("""
        SELECT b.category_id, c.name, b.amount
        FROM budgets b
        JOIN categories c ON b.category_id = c.id
        WHERE b.user_id = %s AND b.month = %s
    """, (user_id, month))

    budgets = cur.fetchall()

    results = []

    for category_id, category_name, budget_amount in budgets:

        # Calculate total spent in that category for that month
        cur.execute("""
            SELECT COALESCE(SUM(t.amount), 0)
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE t.user_id = %s
            AND t.category_id = %s
            AND c.type = 'expense'
            AND DATE_FORMAT(t.date, '%Y-%m-01') = %s
        """, (user_id, category_id, month))

        spent = cur.fetchone()[0]

        results.append({
            "category_id": category_id,
            "category": category_name,
            "budget": float(budget_amount),
            "spent": float(spent),
            "remaining": float(budget_amount - spent)
        })

    cur.close()

    return results