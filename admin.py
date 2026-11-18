from functools import wraps
from datetime import datetime, timedelta
from decimal import Decimal
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from models import User, Product, Category, Order, Ingredient, Supplier, Bill
from extensions import db
admin_bp=Blueprint("admin",__name__,url_prefix="/manage")

def roles(*allowed):
    def deco(fn):
        @wraps(fn)
        def wrapped(*a,**kw):
            user=User.query.get(session.get("user_id")) if session.get("user_id") else None
            if not user: return redirect(url_for("auth.login"))
            if user.role not in allowed: abort(403)
            return fn(*a,**kw)
        return wrapped
    return deco

@admin_bp.route("/")
@roles("admin","manager","cashier","baker","storekeeper")
def dashboard():
    user=User.query.get(session["user_id"])
    return render_template("dashboard.html", user=user, orders=Order.query.order_by(Order.created_at.desc()).limit(8).all(),
        products=Product.query.count(), pending=Order.query.filter_by(status="Pending").count(),
        low=Ingredient.query.filter(Ingredient.quantity <= Ingredient.reorder_level).all(),
        sales=db.session.query(db.func.coalesce(db.func.sum(Bill.total),0)).scalar())

@admin_bp.route("/products",methods=["GET","POST"])
@roles("admin","manager")
def manage_products():
    if request.method=="POST":
        p=Product(name=request.form["name"],description=request.form.get("description"),price=Decimal(request.form["price"]),
                  category_id=request.form.get("category_id") or None,image=request.form.get("image"),is_available=True)
        db.session.add(p); db.session.commit(); flash("Product added.","success")
    return render_template("manage_products.html",products=Product.query.all(),categories=Category.query.all())

@admin_bp.route("/products/<int:pid>/delete",methods=["POST"])
@roles("admin","manager")
def delete_product(pid):
    p=Product.query.get_or_404(pid); p.is_available=False; db.session.commit()
    flash("Product marked unavailable.","info"); return redirect(url_for("admin.manage_products"))

@admin_bp.route("/orders")
@roles("admin","manager","cashier","baker")
def manage_orders():
    return render_template("manage_orders.html",orders=Order.query.order_by(Order.created_at.desc()).all())

@admin_bp.route("/orders/<int:oid>/status",methods=["POST"])
@roles("admin","manager","baker","cashier")
def update_status(oid):
    order=Order.query.get_or_404(oid); status=request.form.get("status")
    if status in ["Pending","Preparing","Ready","Delivered","Cancelled"]:
        order.status=status; db.session.commit(); flash("Order status updated.","success")
    return redirect(url_for("admin.manage_orders"))

@admin_bp.route("/orders/<int:oid>/bill",methods=["POST"])
@roles("admin","manager","cashier")
def create_bill(oid):
    order=Order.query.get_or_404(oid)
    if Bill.query.filter_by(order_id=oid).first():
        flash("A bill already exists for this order.","warning"); return redirect(url_for("admin.manage_orders"))
    discount=max(Decimal("0"),Decimal(request.form.get("discount","0")))
    tax_rate=max(Decimal("0"),Decimal(request.form.get("tax","0")))
    subtotal=Decimal(order.total); discount=min(discount,subtotal)
    tax=(subtotal-discount)*tax_rate/Decimal("100"); total=subtotal-discount+tax
    bill=Bill(order_id=oid,subtotal=subtotal,discount=discount,tax=tax,total=total,payment_mode=request.form.get("payment_mode","Cash"))
    db.session.add(bill); db.session.commit(); flash("Bill generated.","success")
    return redirect(url_for("admin.manage_orders"))

@admin_bp.route("/inventory",methods=["GET","POST"])
@roles("admin","manager","storekeeper")
def inventory():
    if request.method=="POST":
        item=Ingredient(name=request.form["name"],quantity=float(request.form["quantity"]),unit=request.form.get("unit","kg"),
                        reorder_level=float(request.form.get("reorder_level",5)),supplier_id=request.form.get("supplier_id") or None)
        db.session.add(item); db.session.commit(); flash("Ingredient saved.","success")
    return render_template("inventory.html",items=Ingredient.query.all(),suppliers=Supplier.query.all())

@admin_bp.route("/suppliers",methods=["GET","POST"])
@roles("admin","manager","storekeeper")
def suppliers():
    if request.method=="POST":
        db.session.add(Supplier(name=request.form["name"],phone=request.form.get("phone"),address=request.form.get("address")))
        db.session.commit(); flash("Supplier added.","success")
    return render_template("suppliers.html",suppliers=Supplier.query.all())

@admin_bp.route("/reports")
@roles("admin","manager")
def reports():
    start=request.args.get("start"); end=request.args.get("end")
    q=Bill.query
    if start: q=q.filter(Bill.created_at >= datetime.fromisoformat(start))
    if end: q=q.filter(Bill.created_at < datetime.fromisoformat(end)+timedelta(days=1))
    bills=q.order_by(Bill.created_at.desc()).all()
    return render_template("reports.html",bills=bills,total=sum((b.total for b in bills),Decimal("0.00")))
