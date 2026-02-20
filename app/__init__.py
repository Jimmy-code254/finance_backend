from flask import Flask
from .config import Config
from .extensions import mysql, bcrypt, jwt
from app.routes.budget_routes import budget_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mysql.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from .routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    
    from .routes.dashboard_routes import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")

    from .routes.category_routes import category_bp
    app.register_blueprint(category_bp, url_prefix="/api/categories")

    app.register_blueprint(budget_bp, url_prefix="/api/budgets")

    from .routes.transaction_routes import transaction_bp
    app.register_blueprint(transaction_bp, url_prefix="/api/transactions")
    return app
 
    
