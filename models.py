from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="customer", nullable=False)
    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password_hash, password)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    image = db.Column(db.String(500))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10,2), nullable=False)
    image = db.Column(db.String(500))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    is_available = db.Column(db.Boolean, default=True)
    category = db.relationship("Category")

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    order_type = db.Column(db.String(20), default="online")
    status = db.Column(db.String(30), default="Pending")
    total = db.Column(db.Numeric(10,2), default=0)
    customer = db.relationship("User")
    items = db.relationship("OrderItem", cascade="all, delete-orphan")
    bill = db.relationship("Bill", uselist=False, back_populates="order")

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10,2), nullable=False)
    product = db.relationship("Product")

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, default=0)
    unit = db.Column(db.String(20), default="kg")
    reorder_level = db.Column(db.Float, default=5)
    supplier_id = db.Column(db.Integer, db.ForeignKey("supplier.id"))
    supplier = db.relationship("Supplier")

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), unique=True)
    subtotal = db.Column(db.Numeric(10,2), nullable=False)
    discount = db.Column(db.Numeric(10,2), default=0)
    tax = db.Column(db.Numeric(10,2), default=0)
    total = db.Column(db.Numeric(10,2), nullable=False)
    payment_mode = db.Column(db.String(30), default="Cash")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    order = db.relationship("Order", back_populates="bill")
