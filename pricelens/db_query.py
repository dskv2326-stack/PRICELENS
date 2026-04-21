from app import create_app
from models import db, Product, Price
app = create_app()
with app.app_context():
    print("PRODUCTS:")
    for p in Product.query.all():
        prices = ', '.join(f"{pr.platform}:₹{pr.price}" for pr in p.prices)
        print(f"- {p.name} ({p.category}) - {prices}")
    print("\nTotal products:", Product.query.count())
print("Run: python db_query.py")
