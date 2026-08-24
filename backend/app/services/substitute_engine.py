from typing import List, Dict, Any, Optional
from app.services.product_catalog_data import SUBSTITUTE_RULES, CATALOG_PRODUCTS
from app.services.category_classifier import classify_category


class SubstituteEngine:
    def __init__(self):
        self.rules = SUBSTITUTE_RULES

    def get_substitutes(self, product_name: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Find intelligent substitutes for a product.
        Checks direct substitute rules first; if none, searches available products in the same category.
        """
        if not product_name:
            return []

        search_term = product_name.lower().strip()

        # 1. Match direct substitute rules
        for original_key, subs in self.rules.items():
            if search_term in original_key.lower() or original_key.lower() in search_term:
                return subs

        # 2. Dynamic category-based fallback if unavailable
        cat = category or classify_category(product_name)
        alternatives = []
        for p in CATALOG_PRODUCTS:
            # Must be available and not the exact same item
            if p["category"].lower() == cat.lower() and p["availability"] and p["name"].lower() != search_term:
                alternatives.append({
                    "substitute_name": p["name"],
                    "substitute_brand": p.get("brand"),
                    "category": p["category"],
                    "substitute_price": p["price"],
                    "original_price": None,
                    "reason": f"Available option in the {cat} category with high customer ratings.",
                    "attributes": p.get("attributes", []),
                    "availability": True,
                    "image_url": p.get("image_url")
                })
            if len(alternatives) >= 3:
                break

        return alternatives


substitute_engine = SubstituteEngine()
