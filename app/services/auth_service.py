from app.extensions import mysql, bcrypt

def register_user(username, email, password):
    cur = mysql.connection.cursor()

    # Check if email exists
    cur.execute("SELECT id FROM users WHERE email = %s", (email,))
    existing_user = cur.fetchone()

    if existing_user:
        return {"error": "Email already exists"}, 400

    # Hash password
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    # Insert user
    cur.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
        (username, email, hashed_password),
    )
    mysql.connection.commit()

    cur.close()

    return {"message": "User registered successfully"}, 201



def login_user(email, password):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, password_hash FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()

    if not user:
        return {"error": "Invalid credentials"}, 401

    user_id, username, password_hash = user

    if not bcrypt.check_password_hash(password_hash, password):
        return {"error": "Invalid credentials"}, 401

    from flask_jwt_extended import create_access_token
    access_token = create_access_token(identity=str(user_id))  # convert to string

    return {"message": "Login successful", "access_token": access_token, "username": username}, 200