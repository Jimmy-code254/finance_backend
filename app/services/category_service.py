from app.extensions import mysql

# Add category
def add_category(user_id, name, c_type):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO categories (user_id, name, type) VALUES (%s,%s,%s)",
        (user_id, name, c_type)
    )
    mysql.connection.commit()
    cur.close()
    return {"message": "Category added successfully"}, 201

# Get categories for a user
def get_categories(user_id):
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT id, name, type FROM categories WHERE user_id=%s ORDER BY name ASC",
        (user_id,)
    )
    categories = cur.fetchall()
    cur.close()
    return categories