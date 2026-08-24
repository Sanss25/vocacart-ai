from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.models import Product, ShoppingItem, PurchaseHistory, UserPreference, VoiceCommandLog
from app.schemas.schemas import (
    CommandRequest,
    CommandResponse,
    ShoppingItemCreate,
    ShoppingItemUpdate,
    ShoppingItemResponse,
    ProductResponse,
    RecommendationItem,
    SubstituteItem,
    InsightSummary,
)
from app.services.command_parser import parse_command
from app.services.category_classifier import classify_category
from app.services.recommendation_engine import recommendation_engine
from app.services.product_search import product_search_service
from app.services.substitute_engine import substitute_engine
from app.services.insights_service import insights_service

router = APIRouter()

# Keep track of recent action for Undo support
LAST_ACTIONS = []


@router.post("/command", response_model=CommandResponse)
def execute_voice_or_text_command(
    request: CommandRequest,
    db: Session = Depends(get_db)
):
    """
    Main Natural Language Pipeline Endpoint.
    Accepts text or voice transcripts, executes NLU intent & entity extraction,
    applies business logic against the database, and returns confirmation + pipeline telemetry.
    """
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Command text cannot be empty.")

    # 1. Parse natural language
    parsed = parse_command(request.text, language_hint=request.language_hint or "auto")
    intent = parsed["intent"]
    entities = parsed["entities"]
    pipeline = parsed["pipeline"]
    message = parsed["confirmation_message"]
    tts_message = parsed["tts_text"]

    items_affected = []
    search_results = None

    # 2. Execute Business Logic based on Intent
    if intent == "ADD_ITEMS":
        for item_data in entities.get("items", []):
            name = item_data["name"]
            brand = item_data.get("brand")
            qty = item_data.get("quantity", 1.0)
            unit = item_data.get("unit", "piece")
            cat = item_data.get("category") or classify_category(name, brand)
            est_price = item_data.get("estimated_price")

            # Check if matching unpurchased item already exists
            existing = db.query(ShoppingItem).filter(
                ShoppingItem.name.ilike(name),
                ShoppingItem.is_purchased == False
            ).first()

            if existing and existing.unit == unit:
                existing.quantity += qty
                if est_price:
                    existing.estimated_price = (existing.estimated_price or 0.0) + est_price
                db.commit()
                db.refresh(existing)
                items_affected.append({"id": existing.id, "name": existing.name, "quantity": existing.quantity, "action": "updated_quantity"})
                LAST_ACTIONS.append({"type": "ADD_INCREMENT", "id": existing.id, "added_qty": qty})
            else:
                new_item = ShoppingItem(
                    name=name,
                    brand=brand,
                    quantity=qty,
                    unit=unit,
                    category=cat,
                    estimated_price=est_price,
                    is_purchased=False,
                    added_at=datetime.utcnow()
                )
                db.add(new_item)
                db.commit()
                db.refresh(new_item)
                items_affected.append({"id": new_item.id, "name": new_item.name, "quantity": new_item.quantity, "action": "added"})
                LAST_ACTIONS.append({"type": "ADD_NEW", "id": new_item.id})

    elif intent == "REMOVE_ITEM":
        prod_target = entities.get("product", "")
        if prod_target:
            items_to_remove = db.query(ShoppingItem).filter(
                ShoppingItem.name.ilike(f"%{prod_target}%")
            ).all()

            if not items_to_remove:
                message = f"Could not find '{prod_target}' on your shopping list."
                tts_message = f"{prod_target} was not found on your list."
            else:
                for item in items_to_remove:
                    items_affected.append({"id": item.id, "name": item.name, "action": "deleted"})
                    LAST_ACTIONS.append({
                        "type": "DELETE",
                        "item_data": {
                            "name": item.name,
                            "brand": item.brand,
                            "quantity": item.quantity,
                            "unit": item.unit,
                            "category": item.category,
                            "estimated_price": item.estimated_price,
                            "is_purchased": item.is_purchased
                        }
                    })
                    db.delete(item)
                db.commit()

    elif intent == "UPDATE_QUANTITY":
        prod_target = entities.get("product", "")
        new_qty = entities.get("quantity", 1.0)
        new_unit = entities.get("unit")

        if prod_target:
            item = db.query(ShoppingItem).filter(
                ShoppingItem.name.ilike(f"%{prod_target}%"),
                ShoppingItem.is_purchased == False
            ).first()

            if item:
                old_qty = item.quantity
                item.quantity = new_qty
                if new_unit:
                    item.unit = new_unit
                db.commit()
                db.refresh(item)
                items_affected.append({"id": item.id, "name": item.name, "quantity": item.quantity, "action": "quantity_updated"})
                LAST_ACTIONS.append({"type": "UPDATE_QTY", "id": item.id, "old_qty": old_qty, "new_qty": new_qty})
            else:
                # If item not on list, add it with requested quantity
                cat = classify_category(prod_target)
                new_item = ShoppingItem(
                    name=prod_target,
                    quantity=new_qty,
                    unit=new_unit or "piece",
                    category=cat,
                    is_purchased=False,
                    added_at=datetime.utcnow()
                )
                db.add(new_item)
                db.commit()
                db.refresh(new_item)
                message = f"'{prod_target}' was not on your list, so I added {new_qty:g} {new_unit or 'piece'}s."
                tts_message = f"Added {new_qty:g} {new_unit or 'piece'}s of {prod_target}."
                items_affected.append({"id": new_item.id, "name": new_item.name, "quantity": new_item.quantity, "action": "added"})

    elif intent == "CLEAR_LIST":
        all_items = db.query(ShoppingItem).all()
        saved_items = [
            {"name": i.name, "brand": i.brand, "quantity": i.quantity, "unit": i.unit, "category": i.category, "estimated_price": i.estimated_price, "is_purchased": i.is_purchased}
            for i in all_items
        ]
        LAST_ACTIONS.append({"type": "CLEAR_ALL", "items": saved_items})
        db.query(ShoppingItem).delete()
        db.commit()

    elif intent == "CLEAR_PURCHASED":
        purchased = db.query(ShoppingItem).filter(ShoppingItem.is_purchased == True).all()
        saved_purchased = [
            {"name": i.name, "brand": i.brand, "quantity": i.quantity, "unit": i.unit, "category": i.category, "estimated_price": i.estimated_price, "is_purchased": True}
            for i in purchased
        ]
        LAST_ACTIONS.append({"type": "CLEAR_PURCHASED", "items": saved_purchased})
        db.query(ShoppingItem).filter(ShoppingItem.is_purchased == True).delete()
        db.commit()

    elif intent == "MARK_PURCHASED":
        prod_target = entities.get("product", "")
        if prod_target:
            item = db.query(ShoppingItem).filter(
                ShoppingItem.name.ilike(f"%{prod_target}%"),
                ShoppingItem.is_purchased == False
            ).first()

            if item:
                item.is_purchased = True
                item.purchased_at = datetime.utcnow()
                db.commit()
                db.refresh(item)
                items_affected.append({"id": item.id, "name": item.name, "action": "marked_purchased"})
                LAST_ACTIONS.append({"type": "MARK_PURCHASED", "id": item.id})

                # In Shopping Mode: find next remaining item to suggest
                next_item = db.query(ShoppingItem).filter(ShoppingItem.is_purchased == False).first()
                if next_item:
                    message = f"✓ {item.name} marked as purchased. Next item: {next_item.name}."
                    tts_message = f"{item.name} marked as purchased. Next item: {next_item.name}."
                else:
                    message = f"✓ {item.name} marked as purchased. All items in your list are complete!"
                    tts_message = f"{item.name} marked as purchased. All shopping items are complete! Great job."
            else:
                message = f"Could not find an unpurchased item matching '{prod_target}'."
                tts_message = f"No pending item matching {prod_target} was found."

    elif intent == "SEARCH_PRODUCT":
        q = entities.get("query")
        min_p = entities.get("min_price")
        max_p = entities.get("max_price")
        brand = entities.get("brand")
        attrs = entities.get("attributes", [])

        results = product_search_service.search(
            db=db,
            query=q,
            brand=brand,
            min_price=min_p,
            max_price=max_p,
            attributes=attrs
        )
        search_results = results
        count = len(results)
        message = f"Found {count} product{'s' if count != 1 else ''} matching your search."
        tts_message = f"Found {count} products matching your search."

    elif intent == "UNDO":
        if LAST_ACTIONS:
            last = LAST_ACTIONS.pop()
            act_type = last.get("type")
            if act_type == "ADD_NEW":
                db.query(ShoppingItem).filter(ShoppingItem.id == last["id"]).delete()
                db.commit()
                message = "Undid: Removed newly added item."
                tts_message = "Removed recently added item."
            elif act_type == "ADD_INCREMENT":
                item = db.query(ShoppingItem).filter(ShoppingItem.id == last["id"]).first()
                if item:
                    item.quantity = max(1.0, item.quantity - last["added_qty"])
                    db.commit()
                message = "Undid: Reverted item quantity."
                tts_message = "Reverted item quantity."
            elif act_type == "DELETE":
                data = last["item_data"]
                restored = ShoppingItem(**data, added_at=datetime.utcnow())
                db.add(restored)
                db.commit()
                message = f"Undid: Restored '{data['name']}' to list."
                tts_message = f"Restored {data['name']} to list."
            elif act_type in ["CLEAR_ALL", "CLEAR_PURCHASED"]:
                for item_dict in last.get("items", []):
                    restored = ShoppingItem(**item_dict, added_at=datetime.utcnow())
                    db.add(restored)
                db.commit()
                message = f"Undid: Restored {len(last.get('items', []))} items to list."
                tts_message = "Restored shopping list items."
            elif act_type == "MARK_PURCHASED":
                item = db.query(ShoppingItem).filter(ShoppingItem.id == last["id"]).first()
                if item:
                    item.is_purchased = False
                    item.purchased_at = None
                    db.commit()
                message = "Undid: Unmarked item purchase status."
                tts_message = "Reverted purchase status."
        else:
            message = "No recent action to undo."
            tts_message = "No recent action to undo."

    # 3. Log Command for History
    log_entry = VoiceCommandLog(
        raw_transcript=request.text,
        normalized_text=pipeline["normalized_text"],
        language=pipeline["detected_language"],
        intent=intent,
        entities=entities,
        action_status="success",
        action_message=message,
        pipeline_details=pipeline,
        created_at=datetime.utcnow()
    )
    db.add(log_entry)
    db.commit()

    return CommandResponse(
        success=True,
        intent=intent,
        message=message,
        tts_message=tts_message,
        entities=entities,
        pipeline=pipeline,
        items_affected=items_affected,
        search_results=search_results
    )


# =============================================================================
# SHOPPING LIST CRUD
# =============================================================================

@router.get("/shopping-list", response_model=List[ShoppingItemResponse])
def get_shopping_list(db: Session = Depends(get_db)):
    """Retrieve all shopping list items, ordered by category and added time."""
    return db.query(ShoppingItem).order_by(ShoppingItem.is_purchased.asc(), ShoppingItem.category.asc(), ShoppingItem.added_at.desc()).all()


@router.post("/shopping-list", response_model=ShoppingItemResponse)
def add_shopping_item(item_in: ShoppingItemCreate, db: Session = Depends(get_db)):
    """Manually add an item to the shopping list."""
    cat = item_in.category if item_in.category and item_in.category != "Other" else classify_category(item_in.name, item_in.brand)
    new_item = ShoppingItem(
        name=item_in.name.strip(),
        brand=item_in.brand.strip() if item_in.brand else None,
        quantity=item_in.quantity,
        unit=item_in.unit,
        category=cat,
        estimated_price=item_in.estimated_price,
        notes=item_in.notes,
        is_purchased=False,
        added_at=datetime.utcnow()
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    LAST_ACTIONS.append({"type": "ADD_NEW", "id": new_item.id})
    return new_item


@router.patch("/shopping-list/{item_id}", response_model=ShoppingItemResponse)
def update_shopping_item(item_id: int, item_update: ShoppingItemUpdate, db: Session = Depends(get_db)):
    """Update properties of an item on the shopping list."""
    item = db.query(ShoppingItem).filter(ShoppingItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    update_data = item_update.model_dump(exclude_unset=True)
    if "is_purchased" in update_data:
        if update_data["is_purchased"]:
            item.purchased_at = datetime.utcnow()
        else:
            item.purchased_at = None

    for key, value in update_data.items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return item


@router.delete("/shopping-list/{item_id}")
def delete_shopping_item(item_id: int, db: Session = Depends(get_db)):
    """Delete an item from the shopping list."""
    item = db.query(ShoppingItem).filter(ShoppingItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    LAST_ACTIONS.append({
        "type": "DELETE",
        "item_data": {
            "name": item.name,
            "brand": item.brand,
            "quantity": item.quantity,
            "unit": item.unit,
            "category": item.category,
            "estimated_price": item.estimated_price,
            "is_purchased": item.is_purchased
        }
    })
    db.delete(item)
    db.commit()
    return {"status": "success", "message": f"Deleted {item.name}"}


@router.post("/shopping-list/clear")
def clear_shopping_list(db: Session = Depends(get_db)):
    """Clear all items from shopping list."""
    all_items = db.query(ShoppingItem).all()
    saved = [
        {"name": i.name, "brand": i.brand, "quantity": i.quantity, "unit": i.unit, "category": i.category, "estimated_price": i.estimated_price, "is_purchased": i.is_purchased}
        for i in all_items
    ]
    LAST_ACTIONS.append({"type": "CLEAR_ALL", "items": saved})
    db.query(ShoppingItem).delete()
    db.commit()
    return {"status": "success", "message": "Shopping list cleared"}


@router.post("/shopping-list/clear-purchased")
def clear_purchased_items(db: Session = Depends(get_db)):
    """Remove only purchased/checked items from shopping list."""
    purchased = db.query(ShoppingItem).filter(ShoppingItem.is_purchased == True).all()
    saved = [
        {"name": i.name, "brand": i.brand, "quantity": i.quantity, "unit": i.unit, "category": i.category, "estimated_price": i.estimated_price, "is_purchased": True}
        for i in purchased
    ]
    LAST_ACTIONS.append({"type": "CLEAR_PURCHASED", "items": saved})
    db.query(ShoppingItem).filter(ShoppingItem.is_purchased == True).delete()
    db.commit()
    return {"status": "success", "message": "Cleared purchased items"}


@router.post("/shopping-list/undo")
def undo_last_action(db: Session = Depends(get_db)):
    """Undo the most recent action."""
    if not LAST_ACTIONS:
        return {"status": "noop", "message": "No action to undo"}

    last = LAST_ACTIONS.pop()
    act_type = last.get("type")

    if act_type == "ADD_NEW":
        db.query(ShoppingItem).filter(ShoppingItem.id == last["id"]).delete()
        db.commit()
        return {"status": "success", "message": "Removed newly added item"}
    elif act_type == "ADD_INCREMENT":
        item = db.query(ShoppingItem).filter(ShoppingItem.id == last["id"]).first()
        if item:
            item.quantity = max(1.0, item.quantity - last["added_qty"])
            db.commit()
        return {"status": "success", "message": "Reverted item quantity"}
    elif act_type == "DELETE":
        data = last["item_data"]
        restored = ShoppingItem(**data, added_at=datetime.utcnow())
        db.add(restored)
        db.commit()
        return {"status": "success", "message": f"Restored '{data['name']}'"}
    elif act_type in ["CLEAR_ALL", "CLEAR_PURCHASED"]:
        for itm in last.get("items", []):
            restored = ShoppingItem(**itm, added_at=datetime.utcnow())
            db.add(restored)
        db.commit()
        return {"status": "success", "message": f"Restored {len(last.get('items', []))} items"}
    elif act_type == "MARK_PURCHASED":
        item = db.query(ShoppingItem).filter(ShoppingItem.id == last["id"]).first()
        if item:
            item.is_purchased = False
            item.purchased_at = None
            db.commit()
        return {"status": "success", "message": "Reverted purchase mark"}

    return {"status": "noop", "message": "Nothing changed"}


# =============================================================================
# RECOMMENDATIONS & SEASONAL
# =============================================================================

@router.get("/recommendations", response_model=List[RecommendationItem])
def get_recommendations(limit: int = 6, db: Session = Depends(get_db)):
    """Get personalized recommendations with mathematical scores and human explanations."""
    return recommendation_engine.generate_recommendations(db, limit=limit)


@router.get("/seasonal")
def get_seasonal_picks():
    """Get seasonal grocery picks based on current weather/season."""
    return recommendation_engine.get_seasonal_picks()


# =============================================================================
# PRODUCTS & SUBSTITUTES
# =============================================================================

@router.get("/products", response_model=List[ProductResponse])
def list_products(
    category: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List catalog products with optional category filter."""
    query = db.query(Product)
    if category:
        query = query.filter(Product.category.ilike(f"%{category}%"))
    return query.limit(limit).all()


@router.get("/products/search")
def search_products(
    query: Optional[str] = None,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock_only: bool = False,
    db: Session = Depends(get_db)
):
    """Search products with fuzzy keyword and attribute filters."""
    return product_search_service.search(
        db=db,
        query=query,
        category=category,
        brand=brand,
        min_price=min_price,
        max_price=max_price,
        in_stock_only=in_stock_only
    )


@router.get("/substitutes/{product_name}")
def get_product_substitutes(product_name: str, category: Optional[str] = None):
    """Find intelligent substitutes for a product with reasoning and price diffs."""
    return substitute_engine.get_substitutes(product_name, category)


# =============================================================================
# INSIGHTS & HISTORY
# =============================================================================

@router.get("/insights", response_model=InsightSummary)
def get_ai_insights(db: Session = Depends(get_db)):
    """Retrieve full AI insights summary from shopping list and user patterns."""
    return insights_service.calculate_insights(db)


@router.get("/history")
def get_purchase_and_command_history(limit: int = 15, db: Session = Depends(get_db)):
    """Retrieve recent purchase history and recent voice commands."""
    commands = db.query(VoiceCommandLog).order_by(VoiceCommandLog.created_at.desc()).limit(limit).all()
    purchases = db.query(PurchaseHistory).order_by(PurchaseHistory.purchased_at.desc()).limit(limit).all()

    return {
        "commands": [
            {
                "id": c.id,
                "raw_transcript": c.raw_transcript,
                "normalized_text": c.normalized_text,
                "language": c.language,
                "intent": c.intent,
                "entities": c.entities,
                "action_status": c.action_status,
                "action_message": c.action_message,
                "pipeline_details": c.pipeline_details,
                "created_at": c.created_at
            }
            for c in commands
        ],
        "purchases": [
            {
                "id": p.id,
                "product_name": p.product_name,
                "brand": p.brand,
                "category": p.category,
                "quantity": p.quantity,
                "unit": p.unit,
                "price": p.price,
                "purchased_at": p.purchased_at,
                "days_interval": p.days_interval
            }
            for p in purchases
        ]
    }


@router.post("/purchase")
def complete_checkout_and_record_history(db: Session = Depends(get_db)):
    """
    Record all purchased items in shopping list into permanent PurchaseHistory,
    update user preference last_purchased_days_ago to 0, and clear purchased items.
    """
    purchased_items = db.query(ShoppingItem).filter(ShoppingItem.is_purchased == True).all()
    if not purchased_items:
        return {"status": "noop", "message": "No purchased items to record"}

    count = 0
    for item in purchased_items:
        # Create history record
        hist = PurchaseHistory(
            product_name=item.name,
            brand=item.brand,
            category=item.category,
            quantity=item.quantity,
            unit=item.unit,
            price=item.estimated_price or 50.0,
            purchased_at=datetime.utcnow(),
            days_interval=7
        )
        db.add(hist)

        # Update or create user preference
        pref = db.query(UserPreference).filter(UserPreference.product_name.ilike(item.name)).first()
        if pref:
            pref.last_purchased_days_ago = 0
        else:
            new_pref = UserPreference(
                product_name=item.name,
                preferred_brand=item.brand,
                preferred_quantity=item.quantity,
                preferred_unit=item.unit,
                category=item.category,
                frequency_days=7,
                last_purchased_days_ago=0
            )
            db.add(new_pref)

        db.delete(item)
        count += 1

    db.commit()
    return {"status": "success", "message": f"Successfully logged {count} purchased items to history"}


@router.get("/user-profile")
def get_user_profile(db: Session = Depends(get_db)):
    """Retrieve demo user shopping profile and frequency memory."""
    preferences = db.query(UserPreference).all()
    return {
        "user_name": "Alex Sharma",
        "email": "alex.sharma@example.com",
        "preferred_language": "English / Hinglish",
        "shopping_preferences": [
            {
                "product_name": p.product_name,
                "preferred_brand": p.preferred_brand,
                "preferred_quantity": p.preferred_quantity,
                "preferred_unit": p.preferred_unit,
                "frequency_days": p.frequency_days,
                "last_purchased_days_ago": p.last_purchased_days_ago,
                "category": p.category
            }
            for p in preferences
        ]
    }
