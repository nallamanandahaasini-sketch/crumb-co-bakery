from decimal import Decimal
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import Product, Order, OrderItem, Bill
from extensions import db
shop_bp = Blueprint("shop", __name__)

@shop_bp.route("/products")
def products():
    category = request.args.get("category", type=int)
    q = Product.query.filter_by(is_available=True)
    if category: q = q.filter_by(category_id=category)
    return render_template("products.html", products=q.all())

@shop_bp.route("/cart")
def cart():
    cart = session.get("cart", {})
    items, total = [], Decimal("0.00")
    for pid, qty in cart.items():
        p = Product.query.get(int(pid))
        if p:
            line = p.price * int(qty); total += line
            items.append({"product":p, "qty":int(qty), "line":line})
    return render_template("cart.html", items=items, total=total)

@shop_bp.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    p = Product.query.get_or_404(product_id)
    if not p.is_available: flash("This product is currently unavailable.", "warning")
    else:
        cart = session.get("cart", {}); key = str(product_id)
        cart[key] = int(cart.get(key, 0)) + max(1, int(request.form.get("quantity",1)))
        session["cart"] = cart; flash(f"{p.name} added to your basket.", "success")
    return redirect(request.referrer or url_for("shop.products"))

@shop_bp.route("/cart/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart=session.get("cart",{}); cart.pop(str(product_id),None); session["cart"]=cart
    return redirect(url_for("shop.cart"))

@shop_bp.route("/checkout", methods=["POST"])
def checkout():
    if not session.get("user_id"):
        flash("Please log in before placing your order.", "warning"); return redirect(url_for("auth.login"))
    cart=session.get("cart",{})
    if not cart: return redirect(url_for("shop.products"))
    order=Order(customer_id=session["user_id"], order_type="online", status="Pending")
    total=Decimal("0.00")
    for pid, qty in cart.items():
        p=Product.query.get(int(pid))
        if p and p.is_available:
            qty=int(qty); total += p.price*qty
            order.items.append(OrderItem(product=p, quantity=qty, unit_price=p.price))
    if not order.items:
        flash("Your basket is empty.", "warning"); return redirect(url_for("shop.cart"))
    order.total=total; db.session.add(order); db.session.commit()
    session["cart"]={}
    flash(f"Order #{order.id} placed. Payment is recorded at the bakery (online gateway not included).", "success")
    return redirect(url_for("shop.my_orders"))

@shop_bp.route("/my-orders")
def my_orders():
    if not session.get("user_id"): return redirect(url_for("auth.login"))
    from models import Order
    orders=Order.query.filter_by(customer_id=session["user_id"]).order_by(Order.created_at.desc()).all()
    return render_template("my_orders.html", orders=orders)

@shop_bp.route("/about")
def about(): return render_template("about.html")
@shop_bp.route("/contact")
def contact(): return render_template("contact.html")
