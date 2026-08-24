from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class ItemEntity(BaseModel):
    name: str
    quantity: float = 1.0
    unit: str = "piece"
    brand: Optional[str] = None
    category: Optional[str] = "Other"
    attributes: List[str] = Field(default_factory=list)
    estimated_price: Optional[float] = None


class SearchFilters(BaseModel):
    query: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    attributes: List[str] = Field(default_factory=list)
    in_stock_only: bool = False


class PipelineInspection(BaseModel):
    raw_transcript: str
    normalized_text: str
    detected_language: str
    intent: str
    confidence: float = 1.0
    entities: Dict[str, Any] = Field(default_factory=dict)
    reasoning: str
    action_executed: str
    confirmation_message: str
    tts_text: str


class CommandRequest(BaseModel):
    text: str
    language_hint: Optional[str] = "auto"  # "en", "hi", "hinglish", "auto"


class CommandResponse(BaseModel):
    success: bool
    intent: str
    message: str
    tts_message: str
    entities: Dict[str, Any] = Field(default_factory=dict)
    pipeline: PipelineInspection
    items_affected: List[Dict[str, Any]] = Field(default_factory=list)
    search_results: Optional[List[Dict[str, Any]]] = None
    suggestions: Optional[List[str]] = None


class ShoppingItemBase(BaseModel):
    name: str
    brand: Optional[str] = None
    quantity: float = 1.0
    unit: str = "piece"
    category: str = "Other"
    estimated_price: Optional[float] = None
    notes: Optional[str] = None


class ShoppingItemCreate(ShoppingItemBase):
    pass


class ShoppingItemUpdate(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    category: Optional[str] = None
    estimated_price: Optional[float] = None
    is_purchased: Optional[bool] = None
    notes: Optional[str] = None


class ShoppingItemResponse(ShoppingItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_purchased: bool
    added_at: datetime
    purchased_at: Optional[datetime] = None


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    hindi_name: Optional[str] = None
    brand: Optional[str] = None
    category: str
    price: float
    unit: str
    attributes: List[str] = Field(default_factory=list)
    availability: bool
    image_url: Optional[str] = None
    description: Optional[str] = None


class RecommendationItem(BaseModel):
    product_name: str
    category: str
    reason: str
    explanation: str
    score: float
    frequency_days: int
    days_since_last: int
    preferred_brand: Optional[str] = None
    preferred_quantity: float = 1.0
    preferred_unit: str = "piece"
    estimated_price: Optional[float] = None
    is_seasonal: bool = False
    is_urgent: bool = False


class SubstituteItem(BaseModel):
    original_product: str
    substitute_name: str
    substitute_brand: Optional[str] = None
    category: str
    substitute_price: float
    original_price: Optional[float] = None
    reason: str
    attributes: List[str] = Field(default_factory=list)
    availability: bool = True
    image_url: Optional[str] = None


class InsightSummary(BaseModel):
    total_items: int
    pending_items: int
    purchased_items: int
    total_estimated_budget: float
    purchased_budget: float
    pending_budget: float
    category_breakdown: Dict[str, int]
    category_spend: Dict[str, float]
    urgent_recommendations_count: int
    frequent_items: List[Dict[str, Any]]
    weekly_shopping_habit: str
