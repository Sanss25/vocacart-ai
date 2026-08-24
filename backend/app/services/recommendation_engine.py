"""
Smart Explainable Recommendation Engine
Calculates dynamic recommendation scores based on:
- purchase_frequency_score (how often user buys it)
- recency_score (days since last purchase relative to average cycle)
- seasonal_score (alignment with current season)
- preference_score (historical brand/quantity loyalty)
Filters out items already present in the active shopping list.
Provides transparent human-readable reasoning for each suggestion.
"""

from datetime import datetime
from typing import List, Dict, Any, Set
from sqlalchemy.orm import Session
from app.models.models import UserPreference, PurchaseHistory, ShoppingItem
from app.services.product_catalog_data import SEASONAL_CATALOG


class RecommendationEngine:
    def __init__(self):
        pass

    def get_current_season(self) -> str:
        """Determine current season based on month."""
        month = datetime.now().month
        if month in [3, 4, 5, 6]:
            return "Summer"
        elif month in [7, 8, 9]:
            return "Monsoon"
        else:
            return "Winter"

    def get_active_list_names(self, db: Session) -> Set[str]:
        """Get set of normalized product names currently on the active (unpurchased) shopping list."""
        active_items = db.query(ShoppingItem).filter(ShoppingItem.is_purchased == False).all()
        return {item.name.lower().strip() for item in active_items}

    def generate_recommendations(self, db: Session, limit: int = 6) -> List[Dict[str, Any]]:
        """
        Generate prioritized recommendations with mathematical scores and explainable rationale.
        """
        active_names = self.get_active_list_names(db)
        preferences = db.query(UserPreference).all()
        current_season = self.get_current_season()
        seasonal_items_names = [item["name"].lower() for item in SEASONAL_CATALOG.get(current_season, [])]

        recommendations = []

        for pref in preferences:
            prod_name_norm = pref.product_name.lower().strip()

            # Skip if already in shopping list
            if any(prod_name_norm in active or active in prod_name_norm for active in active_names):
                continue

            freq = max(1, pref.frequency_days)
            days_since = pref.last_purchased_days_ago

            # 1. Recency score: Ratio of (days elapsed / expected frequency)
            # If days_since >= freq, ratio >= 1.0 (very high urgency)
            recency_ratio = days_since / freq
            recency_score = min(1.0, recency_ratio * 0.8)

            # 2. Purchase frequency score: Higher for items bought frequently (e.g. every 5-7 days vs 30 days)
            freq_score = max(0.2, min(1.0, 10.0 / freq))

            # 3. Seasonal score
            is_seasonal = any(prod_name_norm in s or s in prod_name_norm for s in seasonal_items_names)
            seasonal_score = 0.9 if is_seasonal else 0.4

            # 4. Preference score
            pref_score = 0.85 if pref.preferred_brand else 0.6

            # Composite weighted formula
            # recommendation_score = freq_score * 0.35 + recency_score * 0.35 + seasonal_score * 0.15 + pref_score * 0.15
            total_score = round(
                (freq_score * 0.35) +
                (recency_score * 0.35) +
                (seasonal_score * 0.15) +
                (pref_score * 0.15),
                2
            )

            is_urgent = days_since >= freq

            # Generate explainable why rationale
            if is_urgent:
                explanation = f"You usually buy {pref.product_name} every {freq} days and it's been {days_since} days since your last purchase."
                reason = f"Running low on {pref.product_name}"
            elif days_since >= (freq - 2):
                explanation = f"You buy {pref.product_name} every {freq} days. It's been {days_since} days, so you might need it soon."
                reason = f"Upcoming replenishment for {pref.product_name}"
            else:
                explanation = f"Frequent staple item in your {pref.category} purchases."
                reason = f"Recommended {pref.category} staple"

            recommendations.append({
                "product_name": pref.product_name.title(),
                "category": pref.category,
                "reason": reason,
                "explanation": explanation,
                "score": total_score,
                "frequency_days": freq,
                "days_since_last": days_since,
                "preferred_brand": pref.preferred_brand,
                "preferred_quantity": pref.preferred_quantity,
                "preferred_unit": pref.preferred_unit,
                "estimated_price": self.estimate_price(pref.product_name, pref.preferred_quantity),
                "is_seasonal": is_seasonal,
                "is_urgent": is_urgent
            })

        # Sort descending by score
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        return recommendations[:limit]

    def get_seasonal_picks(self) -> List[Dict[str, Any]]:
        """Return curated seasonal recommendations with current season metadata."""
        season = self.get_current_season()
        items = SEASONAL_CATALOG.get(season, [])
        return [{**item, "season": season} for item in items]

    def estimate_price(self, product_name: str, quantity: float) -> float:
        from app.services.product_catalog_data import CATALOG_PRODUCTS
        target = product_name.lower()
        for p in CATALOG_PRODUCTS:
            if target in p["name"].lower():
                return round(p["price"] * quantity, 2)
        return round(40.0 * quantity, 2)


recommendation_engine = RecommendationEngine()
