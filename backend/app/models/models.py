from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON, Text
from app.database.session import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False, index=True)
    hindi_name = Column(String(150), nullable=True)
    brand = Column(String(100), nullable=True, index=True)
    category = Column(String(100), nullable=False, index=True)
    price = Column(Float, nullable=False)
    unit = Column(String(50), default="piece")
    attributes = Column(JSON, default=list)  # e.g., ["organic", "whole wheat", "sugar-free", "toned"]
    availability = Column(Boolean, default=True)
    image_url = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)


class ShoppingItem(Base):
    __tablename__ = "shopping_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    brand = Column(String(100), nullable=True)
    quantity = Column(Float, default=1.0)
    unit = Column(String(50), default="piece")
    category = Column(String(100), default="Other")
    estimated_price = Column(Float, nullable=True)
    is_purchased = Column(Boolean, default=False)
    added_at = Column(DateTime, default=datetime.utcnow)
    purchased_at = Column(DateTime, nullable=True)
    notes = Column(String(255), nullable=True)


class PurchaseHistory(Base):
    __tablename__ = "purchase_history"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(150), nullable=False)
    brand = Column(String(100), nullable=True)
    category = Column(String(100), nullable=False)
    quantity = Column(Float, default=1.0)
    unit = Column(String(50), default="piece")
    price = Column(Float, nullable=False)
    purchased_at = Column(DateTime, default=datetime.utcnow)
    days_interval = Column(Integer, default=7)


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(150), unique=True, nullable=False)
    preferred_brand = Column(String(100), nullable=True)
    preferred_quantity = Column(Float, default=1.0)
    preferred_unit = Column(String(50), default="piece")
    category = Column(String(100), default="Other")
    frequency_days = Column(Integer, default=7)
    last_purchased_days_ago = Column(Integer, default=0)


class VoiceCommandLog(Base):
    __tablename__ = "voice_commands"

    id = Column(Integer, primary_key=True, index=True)
    raw_transcript = Column(Text, nullable=False)
    normalized_text = Column(Text, nullable=True)
    language = Column(String(50), default="en")
    intent = Column(String(100), nullable=True)
    entities = Column(JSON, default=dict)
    action_status = Column(String(50), default="success")
    action_message = Column(Text, nullable=True)
    pipeline_details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
