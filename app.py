from flask import Flask, render_template, redirect, url_for, request, session, flash
from config import Config
from extensions import db
from models import User, Category, Product, Order, OrderItem, Ingredient, Supplier, Bill
from auth import auth_bp
from shop import shop_bp
from admin import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(admin_bp)

    @app.context_processor
    def inject_user():
        return {"current_user": User.query.get(session.get("user_id")) if session.get("user_id") else None}

    @app.route("/")
    def home():
        featured = Product.query.filter_by(is_available=True).limit(8).all()
        categories = Category.query.all()
        return render_template("home.html", featured=featured, categories=categories)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
