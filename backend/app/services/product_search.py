"""
Product Search Service with multi-attribute filtering, price bounds,
and integrated substitute recommendations for out-of-stock items.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.models import Product
from app.services.substitute_engine import substitute_engine


class ProductSearchService:
    def search(
        self,
        db: Session,
        query: Optional[str] = None,
        category: Optional[str] = None,
        brand: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        attributes: Optional[List[str]] = None,
        in_stock_only: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Execute flexible search over product catalog with filter criteria.
        """
        db_query = db.query(Product)

        if category:
            db_query = db_query.filter(Product.category.ilike(f"%{category}%"))

        if brand:
            db_query = db_query.filter(Product.brand.ilike(f"%{brand}%"))

        if min_price is not None:
            db_query = db_query.filter(Product.price >= min_price)

        if max_price is not None:
            db_query = db_query.filter(Product.price <= max_price)

        if in_stock_only:
            db_query = db_query.filter(Product.availability == True)

        results = db_query.all()

        formatted_results = []
        q_clean = query.lower().strip() if query else ""

        for prod in results:
            # Text matching on name, hindi_name, description, brand
            if q_clean:
                matches_name = q_clean in prod.name.lower()
                matches_hindi = prod.hindi_name and q_clean in prod.hindi_name.lower()
                matches_brand = prod.brand and q_clean in prod.brand.lower()
                matches_cat = prod.category and q_clean in prod.category.lower()
                matches_desc = prod.description and q_clean in prod.description.lower()
                matches_attr = any(q_clean in attr.lower() for attr in (prod.attributes or []))

                if not (matches_name or matches_hindi or matches_brand or matches_cat or matches_desc or matches_attr):
                    # Check individual token matches
                    tokens = q_clean.split()
                    token_matches = any(t in prod.name.lower() or (prod.brand and t in prod.brand.lower()) for t in tokens if len(t) > 2)
                    if not token_matches:
                        continue

            # Attribute list filtering if requested
            if attributes:
                prod_attrs = [a.lower() for a in (prod.attributes or [])]
                if not any(attr.lower() in prod_attrs for attr in attributes):
                    continue

            # Check for substitutes if out of stock
            substitutes = []
            if not prod.availability:
                substitutes = substitute_engine.get_substitutes(prod.name, prod.category)

            formatted_results.append({
                "id": prod.id,
                "name": prod.name,
                "hindi_name": prod.hindi_name,
                "brand": prod.brand,
                "category": prod.category,
                "price": prod.price,
                "unit": prod.unit,
                "attributes": prod.attributes or [],
                "availability": prod.availability,
                "image_url": prod.image_url,
                "description": prod.description,
                "substitutes": substitutes
            })

        return formatted_results


product_search_service = ProductSearchService()
