from app.extensions import mysql
from datetime import datetime

def get_dashboard(user_id, month=None):
    """
    Returns a full dashboard including:
    - Total income/expense
    - Balance
    - Savings rate
    - Monthly chart (last 12 months)
    - Category chart
    - Budgets with spent/remaining
    - Top expense category
    """
    cur = mysql.connection.cursor()

    # Total income and expenses
    cur.execute(
        "SELECT IFNULL(SUM(amount),0) FROM transactions WHERE user_id=%s AND type='income'",
        (user_id,)
    )
    total_income = cur.fetchone()[0]

    cur.execute(
        "SELECT IFNULL(SUM(amount),0) FROM transactions WHERE user_id=%s AND type='expense'",
        (user_id,)
    )
    total_expense = cur.fetchone()[0]

    balance = total_income - total_expense

    # Savings rate
    savings_rate = ((total_income - total_expense) / total_income * 100) if total_income > 0 else 0

    # Monthly breakdown for last 12 months
    cur.execute(
        """
        SELECT DATE_FORMAT(date,'%Y-%m') AS month,
               SUM(CASE WHEN type='income' THEN amount ELSE 0 END) AS income,
               SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) AS expense
        FROM transactions
        WHERE user_id=%s
        GROUP BY month
        ORDER BY month ASC
        """,
        (user_id,)
    )
    monthly_data = cur.fetchall()
    monthly_chart = [
        {"month": row[0], "income": float(row[1]), "expense": float(row[2])} 
        for row in monthly_data
    ]

    # Category breakdown for pie chart
    cur.execute(
        """
        SELECT c.name AS category, c.type, IFNULL(SUM(t.amount),0) AS total
        FROM categories c
        LEFT JOIN transactions t ON t.category_id=c.id AND t.user_id=%s
        GROUP BY c.id
        """,
        (user_id,)
    )
    category_data = cur.fetchall()
    category_chart = [
        {"category": row[0], "type": row[1], "total": float(row[2])} 
        for row in category_data
    ]

    # Top expense category
    cur.execute(
        """
        SELECT c.name, IFNULL(SUM(t.amount),0) as total
        FROM categories c
        LEFT JOIN transactions t ON t.category_id=c.id AND t.user_id=%s AND c.type='expense'
        GROUP BY c.id
        ORDER BY total DESC
        LIMIT 1
        """,
        (user_id,)
    )
    top_expense_row = cur.fetchone()
    top_expense_category = top_expense_row[0] if top_expense_row else None

    # Budgets for the month
    if not month:
        month = datetime.now().strftime("%Y-%m-01")  # default to current month

    cur.execute(
        """
        SELECT b.category_id, c.name, b.amount
        FROM budgets b
        JOIN categories c ON b.category_id=c.id
        WHERE b.user_id=%s AND b.month=%s
        """,
        (user_id, month)
    )
    budgets = []
    for category_id, category_name, budget_amount in cur.fetchall():
        # total spent in that category
        cur.execute(
            """
            SELECT IFNULL(SUM(t.amount),0)
            FROM transactions t
            JOIN categories c ON t.category_id=c.id
            WHERE t.user_id=%s AND t.category_id=%s AND c.type='expense'
              AND DATE_FORMAT(t.date, '%%Y-%%m-01') = %s
            """,
            (user_id, category_id, month)
        )
        spent = cur.fetchone()[0]
        budgets.append({
            "category_id": category_id,
            "category": category_name,
            "budget": float(budget_amount),
            "spent": float(spent),
            "remaining": float(budget_amount - spent)
        })

    cur.close()

    return {
        "total_income": float(total_income),
        "total_expense": float(total_expense),
        "balance": float(balance),
        "savings_rate": round(savings_rate, 2),
        "monthly_chart": monthly_chart,
        "category_chart": category_chart,
        "top_expense_category": top_expense_category,
        "budgets": budgets
    }