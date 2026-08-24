"""
Database Seeder with rich demo dataset.
Prepopulates:
- Products catalog with realistic Indian & global grocery items, prices in ₹, and attributes
- Realistic user purchase history for pattern detection
- User recurring purchase habits / preferences for explainable recommendations
- Initial active shopping list items
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.models import Product, PurchaseHistory, UserPreference, ShoppingItem
from app.services.product_catalog_data import CATALOG_PRODUCTS


def seed_database(db: Session):
    """Seed initial data if tables are empty."""
    # 1. Seed Products
    if db.query(Product).count() == 0:
        for p_data in CATALOG_PRODUCTS:
            product = Product(
                name=p_data["name"],
                hindi_name=p_data.get("hindi_name"),
                brand=p_data.get("brand"),
                category=p_data["category"],
                price=p_data["price"],
                unit=p_data.get("unit", "piece"),
                attributes=p_data.get("attributes", []),
                availability=p_data.get("availability", True),
                image_url=p_data.get("image_url"),
                description=p_data.get("description")
            )
            db.add(product)
        db.commit()

    # 2. Seed User Preferences (Shopping Memory Profile)
    if db.query(UserPreference).count() == 0:
        user_preferences = [
            {
                "product_name": "Milk",
                "preferred_brand": "Amul",
                "preferred_quantity": 2.0,
                "preferred_unit": "packet",
                "category": "Dairy",
                "frequency_days": 7,
                "last_purchased_days_ago": 8  # Due / Urgent!
            },
            {
                "product_name": "Eggs",
                "preferred_brand": "Eggoz",
                "preferred_quantity": 1.0,
                "preferred_unit": "box",
                "category": "Meat",
                "frequency_days": 8,
                "last_purchased_days_ago": 9  # Due / Urgent!
            },
            {
                "product_name": "Bananas",
                "preferred_brand": "FreshFarm",
                "preferred_quantity": 1.0,
                "preferred_unit": "dozen",
                "category": "Produce",
                "frequency_days": 6,
                "last_purchased_days_ago": 6  # Due soon
            },
            {
                "product_name": "Whole Wheat Bread",
                "preferred_brand": "Britannia",
                "preferred_quantity": 1.0,
                "preferred_unit": "loaf",
                "category": "Bakery",
                "frequency_days": 5,
                "last_purchased_days_ago": 4  # 1 day remaining
            },
            {
                "product_name": "Tata Salt",
                "preferred_brand": "Tata",
                "preferred_quantity": 1.0,
                "preferred_unit": "packet",
                "category": "Pantry",
                "frequency_days": 30,
                "last_purchased_days_ago": 29  # Due in 1 day
            },
            {
                "product_name": "Basmati Rice",
                "preferred_brand": "Daawat",
                "preferred_quantity": 1.0,
                "preferred_unit": "bag",
                "category": "Pantry",
                "frequency_days": 25,
                "last_purchased_days_ago": 15
            },
            {
                "product_name": "Tata Tea Gold",
                "preferred_brand": "Tata",
                "preferred_quantity": 1.0,
                "preferred_unit": "packet",
                "category": "Beverages",
                "frequency_days": 20,
                "last_purchased_days_ago": 19  # Due soon
            },
            {
                "product_name": "Tomatoes",
                "preferred_brand": "FreshFarm",
                "preferred_quantity": 2.0,
                "preferred_unit": "kg",
                "category": "Produce",
                "frequency_days": 4,
                "last_purchased_days_ago": 5  # Due / Urgent!
            }
        ]

        for up in user_preferences:
            pref = UserPreference(
                product_name=up["product_name"],
                preferred_brand=up["preferred_brand"],
                preferred_quantity=up["preferred_quantity"],
                preferred_unit=up["preferred_unit"],
                category=up["category"],
                frequency_days=up["frequency_days"],
                last_purchased_days_ago=up["last_purchased_days_ago"]
            )
            db.add(pref)
        db.commit()

    # 3. Seed Purchase History
    if db.query(PurchaseHistory).count() == 0:
        now = datetime.utcnow()
        history_items = [
            ("Amul Taaza Toned Milk", "Amul", "Dairy", 2.0, "packet", 60.0, 8, 7),
            ("Amul Taaza Toned Milk", "Amul", "Dairy", 2.0, "packet", 60.0, 15, 7),
            ("Amul Taaza Toned Milk", "Amul", "Dairy", 2.0, "packet", 60.0, 22, 7),
            ("Eggoz Farm Fresh White Eggs", "Eggoz", "Meat", 1.0, "box", 58.0, 9, 8),
            ("Eggoz Farm Fresh White Eggs", "Eggoz", "Meat", 1.0, "box", 58.0, 17, 8),
            ("Britannia 100% Whole Wheat Bread", "Britannia", "Bakery", 1.0, "loaf", 55.0, 4, 5),
            ("Britannia 100% Whole Wheat Bread", "Britannia", "Bakery", 1.0, "loaf", 55.0, 9, 5),
            ("Britannia 100% Whole Wheat Bread", "Britannia", "Bakery", 1.0, "loaf", 55.0, 14, 5),
            ("Fresh Robusta Bananas", "FreshFarm", "Produce", 1.0, "dozen", 60.0, 6, 6),
            ("Fresh Robusta Bananas", "FreshFarm", "Produce", 1.0, "dozen", 60.0, 12, 6),
            ("Fresh Hybrid Tomatoes", "FreshFarm", "Produce", 2.0, "kg", 80.0, 5, 4),
            ("Fresh Hybrid Tomatoes", "FreshFarm", "Produce", 2.0, "kg", 80.0, 9, 4),
            ("Tata Salt Vacuum Evaporated 1kg", "Tata", "Pantry", 1.0, "packet", 28.0, 29, 30),
            ("Daawat Rozana Super Basmati Rice 5kg", "Daawat", "Pantry", 1.0, "bag", 395.0, 15, 25),
            ("Tata Tea Gold 500g", "Tata", "Beverages", 1.0, "packet", 290.0, 19, 20),
            ("Surf Excel Quick Wash 1kg", "Surf Excel", "Household", 1.0, "packet", 150.0, 20, 25),
            ("Colgate Strong Teeth 200g", "Colgate", "Personal Care", 1.0, "tube", 115.0, 24, 30),
            ("Fortune Sunlite Refined Sunflower Oil 1L", "Fortune", "Pantry", 2.0, "pouch", 290.0, 18, 20),
            ("Lay's India's Magic Masala Chips 50g", "Lay's", "Snacks", 3.0, "packet", 60.0, 3, 5),
            ("Amul Salted Butter 100g", "Amul", "Dairy", 1.0, "packet", 58.0, 10, 14),
            ("Aashirvaad Shudh Chakki Atta 5kg", "Aashirvaad", "Pantry", 1.0, "bag", 245.0, 16, 20),
        ]

        for name, brand, cat, qty, unit, price, days_ago, interval in history_items:
            p_date = now - timedelta(days=days_ago)
            rec = PurchaseHistory(
                product_name=name,
                brand=brand,
                category=cat,
                quantity=qty,
                unit=unit,
                price=price,
                purchased_at=p_date,
                days_interval=interval
            )
            db.add(rec)
        db.commit()

    # 4. Seed Starter Shopping List
    if db.query(ShoppingItem).count() == 0:
        starter_items = [
            {"name": "Milk", "brand": "Amul", "quantity": 2.0, "unit": "packet", "category": "Dairy", "estimated_price": 60.0, "is_purchased": False},
            {"name": "Apples", "brand": "FreshFarm", "quantity": 5.0, "unit": "piece", "category": "Produce", "estimated_price": 120.0, "is_purchased": False},
            {"name": "Whole Wheat Bread", "brand": "Britannia", "quantity": 1.0, "unit": "loaf", "category": "Bakery", "estimated_price": 55.0, "is_purchased": False},
        ]
        for itm in starter_items:
            db_item = ShoppingItem(
                name=itm["name"],
                brand=itm["brand"],
                quantity=itm["quantity"],
                unit=itm["unit"],
                category=itm["category"],
                estimated_price=itm["estimated_price"],
                is_purchased=itm["is_purchased"],
                added_at=datetime.utcnow()
            )
            db.add(db_item)
        db.commit()
