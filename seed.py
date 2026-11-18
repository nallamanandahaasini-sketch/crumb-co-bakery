from app import app
from extensions import db
from models import User, Category, Product, Supplier, Ingredient

with app.app_context():
    db.create_all()
    if not Category.query.first():
        cats=[Category(name=n) for n in ["Cakes","Breads","Pastries","Cookies","Cupcakes"]]
        db.session.add_all(cats); db.session.flush()
        samples=[
          ("Chocolate Truffle Cake","Rich chocolate layers finished with silky ganache.",649,"https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800",0),
          ("Strawberry Celebration Cake","Vanilla sponge with fresh strawberry cream.",799,"https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=800",0),
          ("Sourdough Loaf","Slow-fermented artisan bread with a crisp crust.",180,"https://images.unsplash.com/photo-1585478259715-876acc5be8eb?w=800",1),
          ("Butter Croissant","Flaky, buttery pastry baked fresh every morning.",95,"https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=800",2),
          ("Choco Chip Cookies","Golden cookies loaded with chocolate chips.",120,"https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800",3),
          ("Vanilla Cupcakes","Soft vanilla cupcakes with whipped frosting.",85,"https://images.unsplash.com/photo-1486427944299-d1955d23e34d?w=800",4)]
        for n,d,p,img,c in samples: db.session.add(Product(name=n,description=d,price=p,image=img,category=cats[c]))
        db.session.add(User(name="Bakery Admin",email="admin@crumbandco.com",role="admin",password_hash=""))
        admin=User.query.filter_by(email="admin@crumbandco.com").first(); admin.set_password("Admin@12345")
        sup=Supplier(name="Sunrise Food Supplies",phone="9876543210",address="Guntur")
        db.session.add(sup); db.session.flush()
        db.session.add_all([Ingredient(name="Flour",quantity=18,unit="kg",reorder_level=10,supplier=sup),
                            Ingredient(name="Sugar",quantity=7,unit="kg",reorder_level=8,supplier=sup)])
        db.session.commit()
    print("Database ready. Demo admin: admin@crumbandco.com / Admin@12345")
