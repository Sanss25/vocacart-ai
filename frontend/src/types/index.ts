export type VoiceState = 'IDLE' | 'LISTENING' | 'PROCESSING' | 'SUCCESS' | 'ERROR';

export type LanguageMode = 'en' | 'hi' | 'hinglish';

export interface PipelineInspection {
  raw_transcript: string;
  normalized_text: string;
  detected_language: string;
  intent: string;
  confidence: number;
  entities: Record<string, any>;
  reasoning: string;
  action_executed: string;
  confirmation_message: string;
  tts_text: string;
}

export interface CommandResponse {
  success: boolean;
  intent: string;
  message: string;
  tts_message: string;
  entities: Record<string, any>;
  pipeline: PipelineInspection;
  items_affected: Array<{ id: number; name: string; quantity?: number; action: string }>;
  search_results?: Product[];
}

export interface ShoppingItem {
  id: number;
  name: string;
  brand?: string;
  quantity: number;
  unit: string;
  category: string;
  estimated_price?: number;
  is_purchased: boolean;
  added_at: string;
  purchased_at?: string;
  notes?: string;
}

export interface Product {
  id: number;
  name: string;
  hindi_name?: string;
  brand?: string;
  category: string;
  price: number;
  unit: string;
  attributes: string[];
  availability: boolean;
  image_url?: string;
  description?: string;
  substitutes?: SubstituteItem[];
}

export interface SubstituteItem {
  substitute_name: string;
  substitute_brand?: string;
  category: string;
  substitute_price: number;
  original_price?: number;
  reason: string;
  attributes: string[];
  availability: boolean;
  image_url?: string;
}

export interface RecommendationItem {
  product_name: string;
  category: string;
  reason: string;
  explanation: string;
  score: number;
  frequency_days: number;
  days_since_last: number;
  preferred_brand?: string;
  preferred_quantity: number;
  preferred_unit: string;
  estimated_price?: number;
  is_seasonal: boolean;
  is_urgent: boolean;
}

export interface SeasonalItem {
  name: string;
  category: string;
  price: number;
  unit: string;
  reason: string;
  image: string;
  season: string;
}

export interface InsightSummary {
  total_items: number;
  pending_items: number;
  purchased_items: number;
  total_estimated_budget: number;
  purchased_budget: number;
  pending_budget: number;
  category_breakdown: Record<string, number>;
  category_spend: Record<string, number>;
  urgent_recommendations_count: number;
  frequent_items: Array<{
    product_name: string;
    preferred_brand?: string;
    frequency_days: number;
    last_purchased_days_ago: number;
    is_urgent: boolean;
    category: string;
  }>;
  weekly_shopping_habit: string;
}

export interface HistoryItem {
  id: number;
  raw_transcript: string;
  normalized_text: string;
  language: string;
  intent: string;
  entities: Record<string, any>;
  action_status: string;
  action_message: string;
  pipeline_details: PipelineInspection;
  created_at: string;
}
