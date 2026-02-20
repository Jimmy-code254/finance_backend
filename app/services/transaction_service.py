from app.extensions import mysql

# Add a transaction
def add_transaction(user_id, category_id, amount, description="", date=None):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO transactions (user_id, category_id, amount, description, date) VALUES (%s,%s,%s,%s,%s)",
        (user_id, category_id, amount, description, date)
    )
    mysql.connection.commit()
    cur.close()
    return {"message": "Transaction added successfully"}, 201

# Get all transactions for a user
def get_transactions(user_id):
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT t.id, t.amount, t.description, t.date, t.created_at, c.name AS category, c.type AS category_type "
        "FROM transactions t LEFT JOIN categories c ON t.category_id=c.id "
        "WHERE t.user_id=%s ORDER BY t.date DESC", 
        (user_id,)
    )
    transactions = cur.fetchall()
    cur.close()
    return transactions

# Delete a transaction
def delete_transaction(transaction_id, user_id):
    cur = mysql.connection.cursor()
    cur.execute(
        "DELETE FROM transactions WHERE id=%s AND user_id=%s", 
        (transaction_id, user_id)
    )
    mysql.connection.commit()
    cur.close()
    return {"message": "Transaction deleted successfully"}, 200

def filter_transactions(user_id, start_date=None, end_date=None, category_id=None, min_amount=None, max_amount=None):
    cur = mysql.connection.cursor()

    query = "SELECT t.id, t.amount, t.description, t.date, c.name AS category, c.type AS category_type " \
            "FROM transactions t JOIN categories c ON t.category_id=c.id WHERE t.user_id=%s"
    params = [user_id]

    # Add filters dynamically
    if start_date:
        query += " AND t.date >= %s"
        params.append(start_date)
    if end_date:
        query += " AND t.date <= %s"
        params.append(end_date)
    if category_id:
        query += " AND t.category_id = %s"
        params.append(category_id)
    if min_amount:
        query += " AND t.amount >= %s"
        params.append(min_amount)
    if max_amount:
        query += " AND t.amount <= %s"
        params.append(max_amount)

    query += " ORDER BY t.date DESC"

    cur.execute(query, tuple(params))
    results = cur.fetchall()
    cur.close()

    # Format results for JSON
    transactions = []
    for row in results:
        transactions.append({
            "id": row[0],
            "amount": float(row[1]),
            "description": row[2],
            "date": str(row[3]),
            "category": row[4],
            "category_type": row[5]
        })

    return transactions


