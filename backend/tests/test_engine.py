"""
Comprehensive Unit and Integration Test Suite for VocaCart AI Backend
Tests NLU intent parser, entity extractor, category classifier, recommendation engine,
substitute engine, and FastAPI REST endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.command_parser import parse_command, extract_price_limits
from app.services.category_classifier import classify_category
from app.services.substitute_engine import substitute_engine
from app.services.recommendation_engine import recommendation_engine
from app.services.seed_data import seed_database
from app.database.session import SessionLocal, Base, engine


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


# =============================================================================
# 1. NLU Intent and Entity Extraction Tests
# =============================================================================

def test_add_single_item():
    result = parse_command("Add 3 bottles of Coca Cola")
    assert result["intent"] == "ADD_ITEMS"
    items = result["entities"]["items"]
    assert len(items) == 1
    assert items[0]["quantity"] == 3.0
    assert items[0]["unit"] == "bottle"
    assert "Coca" in items[0]["brand"] or "Coca" in items[0]["name"]
    assert items[0]["category"] == "Beverages"


def test_add_multi_items():
    result = parse_command("I need two packets of milk, five apples and a loaf of bread")
    assert result["intent"] == "ADD_ITEMS"
    items = result["entities"]["items"]
    assert len(items) == 3
    # Check item 1 (milk)
    assert items[0]["quantity"] == 2.0
    assert items[0]["unit"] == "packet"
    assert "Milk" in items[0]["name"]
    # Check item 2 (apples)
    assert items[1]["quantity"] == 5.0
    assert "Apple" in items[1]["name"]
    # Check item 3 (bread)
    assert items[2]["quantity"] == 1.0
    assert items[2]["unit"] == "loaf"
    assert "Bread" in items[2]["name"]


def test_natural_language_variations():
    variations = [
        "Add milk",
        "I need milk",
        "Put milk on my shopping list",
        "Don't forget milk",
        "Buy some milk"
    ]
    for text in variations:
        res = parse_command(text)
        assert res["intent"] == "ADD_ITEMS"
        assert any("Milk" in item["name"] for item in res["entities"]["items"])


def test_remove_item():
    variations = [
        "Remove bread",
        "Take bread off my list",
        "I don't need bread anymore",
        "Bread hata do"
    ]
    for text in variations:
        res = parse_command(text)
        assert res["intent"] == "REMOVE_ITEM"
        assert "Bread" in res["entities"]["product"]


def test_update_quantity():
    res = parse_command("Actually, make that 3 bottles of milk")
    assert res["intent"] == "UPDATE_QUANTITY"
    assert res["entities"]["quantity"] == 3.0
    assert res["entities"]["unit"] == "bottle"


def test_multilingual_hinglish_add():
    res = parse_command("Do packet doodh add karo")
    assert res["intent"] == "ADD_ITEMS"
    item = res["entities"]["items"][0]
    assert item["quantity"] == 2.0
    assert item["unit"] == "packet"
    assert "Milk" in item["name"]
    assert item["category"] == "Dairy"


def test_multilingual_devanagari_add():
    res = parse_command("मुझे दो किलो चावल चाहिए")
    assert res["intent"] == "ADD_ITEMS"
    item = res["entities"]["items"][0]
    assert item["quantity"] == 2.0
    assert item["unit"] == "kg"
    assert "Rice" in item["name"]
    assert item["category"] == "Pantry"


def test_price_extraction():
    min_p, max_p = extract_price_limits("Find organic apples under ₹300")
    assert min_p is None
    assert max_p == 300.0

    min_p2, max_p2 = extract_price_limits("Find shampoo between 300 and 500 rupees")
    assert min_p2 == 300.0
    assert max_p2 == 500.0


def test_search_intent():
    res = parse_command("Find organic apples under 300 rupees")
    assert res["intent"] == "SEARCH_PRODUCT"
    assert res["entities"]["max_price"] == 300.0
    assert "organic" in res["entities"]["attributes"]


# =============================================================================
# 2. Category Classification Tests
# =============================================================================

def test_category_classification():
    assert classify_category("Amul Taaza Milk") == "Dairy"
    assert classify_category("Royal Gala Apple") == "Produce"
    assert classify_category("Whole Wheat Bread") == "Bakery"
    assert classify_category("Colgate Strong Teeth Toothpaste") == "Personal Care"
    assert classify_category("Surf Excel Detergent") == "Household"
    assert classify_category("Lay's Magic Masala Chips") == "Snacks"
    assert classify_category("Tata Salt") == "Pantry"
    assert classify_category("Eggoz Eggs") == "Meat"


# =============================================================================
# 3. Substitute Engine Tests
# =============================================================================

def test_substitutes_for_out_of_stock_item():
    subs = substitute_engine.get_substitutes("Regular Cow Milk 1L", "Dairy")
    assert len(subs) >= 1
    assert any("Almond Milk" in s["substitute_name"] or "Soy Milk" in s["substitute_name"] for s in subs)
    assert subs[0]["reason"] != ""


# =============================================================================
# 4. Recommendation Engine Tests
# =============================================================================

def test_recommendation_scoring():
    db = SessionLocal()
    try:
        recs = recommendation_engine.generate_recommendations(db, limit=5)
        assert len(recs) > 0
        for r in recs:
            assert "score" in r
            assert 0.0 <= r["score"] <= 1.5
            assert "explanation" in r
            assert "You" in r["explanation"] or "Frequent" in r["explanation"]
    finally:
        db.close()


# =============================================================================
# 5. API Endpoints Integration Tests
# =============================================================================

def test_api_command_add_and_list(client):
    response = client.post("/api/command", json={"text": "Add 2 packets of Amul milk"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["intent"] == "ADD_ITEMS"
    assert "pipeline" in data
    assert data["pipeline"]["detected_language"] in ["en", "hinglish"]

    # Verify shopping list contains the item
    list_res = client.get("/api/shopping-list")
    assert list_res.status_code == 200
    items = list_res.json()
    assert any("Milk" in itm["name"] for itm in items)


def test_api_product_search(client):
    response = client.get("/api/products/search?query=apples&max_price=300")
    assert response.status_code == 200
    results = response.json()
    assert len(results) >= 1
    assert all(r["price"] <= 300 for r in results)


def test_api_insights(client):
    response = client.get("/api/insights")
    assert response.status_code == 200
    data = response.json()
    assert "total_items" in data
    assert "total_estimated_budget" in data
    assert "category_breakdown" in data
