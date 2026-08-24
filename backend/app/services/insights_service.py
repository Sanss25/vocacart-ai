"""
AI Insights Service
Calculates real-time shopping analytics, budget estimation, category distribution,
and actionable shopping habit intelligence.
"""

from collections import defaultdict
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.models.models import ShoppingItem, UserPreference, PurchaseHistory


class InsightsService:
    def calculate_insights(self, db: Session) -> Dict[str, Any]:
        """Compute full AI insights summary from shopping list and user profile."""
        all_items = db.query(ShoppingItem).all()
        preferences = db.query(UserPreference).all()
        history = db.query(PurchaseHistory).all()

        total_items = len(all_items)
        pending_items = len([i for i in all_items if not i.is_purchased])
        purchased_items = len([i for i in all_items if i.is_purchased])

        total_estimated_budget = sum((i.estimated_price or 0.0) for i in all_items)
        purchased_budget = sum((i.estimated_price or 0.0) for i in all_items if i.is_purchased)
        pending_budget = total_estimated_budget - purchased_budget

        category_counts = defaultdict(int)
        category_spend = defaultdict(float)

        for item in all_items:
            cat = item.category or "Other"
            category_counts[cat] += 1
            category_spend[cat] += (item.estimated_price or 0.0)

        # Frequent items / Urgent restock alerts
        urgent_count = 0
        frequent_items = []
        for pref in preferences:
            is_urgent = pref.last_purchased_days_ago >= pref.frequency_days
            if is_urgent:
                urgent_count += 1
            frequent_items.append({
                "product_name": pref.product_name,
                "preferred_brand": pref.preferred_brand,
                "frequency_days": pref.frequency_days,
                "last_purchased_days_ago": pref.last_purchased_days_ago,
                "is_urgent": is_urgent,
                "category": pref.category
            })

        # Generate intelligent summary text
        top_cat = max(category_counts.items(), key=lambda x: x[1])[0] if category_counts else "Groceries"
        weekly_summary = (
            f"You usually restock dairy every 7 days and staples bi-weekly. "
            f"Your current shopping list is approximately ₹{round(total_estimated_budget, 2):g} with {pending_items} pending items, "
            f"dominated by {top_cat} items."
        )

        return {
            "total_items": total_items,
            "pending_items": pending_items,
            "purchased_items": purchased_items,
            "total_estimated_budget": round(total_estimated_budget, 2),
            "purchased_budget": round(purchased_budget, 2),
            "pending_budget": round(pending_budget, 2),
            "category_breakdown": dict(category_counts),
            "category_spend": {k: round(v, 2) for k, v in category_spend.items()},
            "urgent_recommendations_count": urgent_count,
            "frequent_items": frequent_items,
            "weekly_shopping_habit": weekly_summary
        }


insights_service = InsightsService()
