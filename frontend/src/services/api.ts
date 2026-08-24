import type {
  CommandResponse,
  ShoppingItem,
  Product,
  RecommendationItem,
  SeasonalItem,
  SubstituteItem,
  InsightSummary,
  HistoryItem
} from '../types';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errData = await response.json().catch(() => ({}));
    throw new Error(errData.detail || `Request failed with status ${response.status}`);
  }
  return response.json();
}

export const api = {
  // 1. Natural Language Command
  async sendCommand(text: string, languageHint = 'auto'): Promise<CommandResponse> {
    const res = await fetch(`${API_BASE}/command`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, language_hint: languageHint }),
    });
    return handleResponse<CommandResponse>(res);
  },

  // 2. Shopping List CRUD
  async getShoppingList(): Promise<ShoppingItem[]> {
    const res = await fetch(`${API_BASE}/shopping-list`);
    return handleResponse<ShoppingItem[]>(res);
  },

  async addShoppingItem(item: { name: string; brand?: string; quantity: number; unit: string; category?: string; estimated_price?: number }): Promise<ShoppingItem> {
    const res = await fetch(`${API_BASE}/shopping-list`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(item),
    });
    return handleResponse<ShoppingItem>(res);
  },

  async updateShoppingItem(id: number, updates: Partial<ShoppingItem>): Promise<ShoppingItem> {
    const res = await fetch(`${API_BASE}/shopping-list/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates),
    });
    return handleResponse<ShoppingItem>(res);
  },

  async deleteShoppingItem(id: number): Promise<{ status: string; message: string }> {
    const res = await fetch(`${API_BASE}/shopping-list/${id}`, {
      method: 'DELETE',
    });
    return handleResponse<{ status: string; message: string }>(res);
  },

  async clearShoppingList(): Promise<{ status: string; message: string }> {
    const res = await fetch(`${API_BASE}/shopping-list/clear`, {
      method: 'POST',
    });
    return handleResponse<{ status: string; message: string }>(res);
  },

  async clearPurchasedItems(): Promise<{ status: string; message: string }> {
    const res = await fetch(`${API_BASE}/shopping-list/clear-purchased`, {
      method: 'POST',
    });
    return handleResponse<{ status: string; message: string }>(res);
  },

  async undoLastAction(): Promise<{ status: string; message: string }> {
    const res = await fetch(`${API_BASE}/shopping-list/undo`, {
      method: 'POST',
    });
    return handleResponse<{ status: string; message: string }>(res);
  },

  // 3. Recommendations & Seasonal
  async getRecommendations(): Promise<RecommendationItem[]> {
    const res = await fetch(`${API_BASE}/recommendations`);
    return handleResponse<RecommendationItem[]>(res);
  },

  async getSeasonalPicks(): Promise<SeasonalItem[]> {
    const res = await fetch(`${API_BASE}/seasonal`);
    return handleResponse<SeasonalItem[]>(res);
  },

  // 4. Products & Search
  async getProducts(category?: string): Promise<Product[]> {
    const url = category ? `${API_BASE}/products?category=${encodeURIComponent(category)}` : `${API_BASE}/products`;
    const res = await fetch(url);
    return handleResponse<Product[]>(res);
  },

  async searchProducts(query: string, minPrice?: number, maxPrice?: number): Promise<Product[]> {
    const params = new URLSearchParams();
    if (query) params.append('query', query);
    if (minPrice !== undefined) params.append('min_price', minPrice.toString());
    if (maxPrice !== undefined) params.append('max_price', maxPrice.toString());

    const res = await fetch(`${API_BASE}/products/search?${params.toString()}`);
    return handleResponse<Product[]>(res);
  },

  async getSubstitutes(productName: string): Promise<SubstituteItem[]> {
    const res = await fetch(`${API_BASE}/substitutes/${encodeURIComponent(productName)}`);
    return handleResponse<SubstituteItem[]>(res);
  },

  // 5. Insights & History
  async getInsights(): Promise<InsightSummary> {
    const res = await fetch(`${API_BASE}/insights`);
    return handleResponse<InsightSummary>(res);
  },

  async getHistory(): Promise<{ commands: HistoryItem[]; purchases: any[] }> {
    const res = await fetch(`${API_BASE}/history`);
    return handleResponse<{ commands: HistoryItem[]; purchases: any[] }>(res);
  },

  async checkoutPurchased(): Promise<{ status: string; message: string }> {
    const res = await fetch(`${API_BASE}/purchase`, {
      method: 'POST',
    });
    return handleResponse<{ status: string; message: string }>(res);
  }
};
