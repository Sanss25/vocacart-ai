import React, { useState } from 'react';
import type { Product, SubstituteItem } from '../types';
import { Search, Plus, RefreshCw } from 'lucide-react';
import { SubstituteModal } from './SubstituteModal';

interface ProductSearchProps {
  products: Product[];
  searchResults: Product[] | null;
  onSearch: (query: string, minPrice?: number, maxPrice?: number) => void;
  onAddToCart: (product: Product) => void;
  onSelectSubstitute: (sub: SubstituteItem) => void;
}

export const ProductSearch: React.FC<ProductSearchProps> = ({
  products,
  searchResults,
  onSearch,
  onAddToCart,
  onSelectSubstitute,
}) => {
  const [query, setQuery] = useState('');
  const [maxPrice, setMaxPrice] = useState<number | ''>('');
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [selectedSubstituteProduct, setSelectedSubstituteProduct] = useState<Product | null>(null);

  const displayList = searchResults !== null ? searchResults : products;

  const categories = ['All', 'Produce', 'Dairy', 'Bakery', 'Beverages', 'Snacks', 'Pantry', 'Meat', 'Personal Care', 'Household'];

  const filteredList = displayList.filter(p => {
    if (selectedCategory !== 'All' && p.category !== selectedCategory) return false;
    if (maxPrice !== '' && p.price > Number(maxPrice)) return false;
    return true;
  });

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(query, undefined, maxPrice === '' ? undefined : Number(maxPrice));
  };

  return (
    <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 border-b border-slate-100 mb-6">
        <div>
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center font-bold">
              <Search className="w-4 h-4" />
            </div>
            <h3 className="text-xl font-extrabold text-slate-900 tracking-tight">Product Catalog & Voice Search</h3>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Search 40+ catalog items by name, category, brand, or price filter (e.g. "under ₹300")
          </p>
        </div>
      </div>

      {/* Search Input and Max Price Filter */}
      <form onSubmit={handleSearchSubmit} className="grid grid-cols-1 sm:grid-cols-12 gap-3 mb-5">
        <div className="sm:col-span-7 relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
          <input
            type="text"
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="Search catalog (e.g., Organic Apples, Amul Milk, Tata Salt)..."
            className="w-full pl-10 pr-4 py-2.5 rounded-2xl bg-slate-50 border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:bg-white transition-all"
          />
        </div>

        <div className="sm:col-span-3">
          <input
            type="number"
            value={maxPrice}
            onChange={e => setMaxPrice(e.target.value === '' ? '' : Number(e.target.value))}
            placeholder="Max Price (₹)"
            className="w-full px-3.5 py-2.5 rounded-2xl bg-slate-50 border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:bg-white transition-all"
          />
        </div>

        <div className="sm:col-span-2">
          <button
            type="submit"
            className="w-full py-2.5 px-4 rounded-2xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-sm shadow-sm transition-all active:scale-95"
          >
            Filter
          </button>
        </div>
      </form>

      {/* Category Pills */}
      <div className="flex items-center space-x-1.5 overflow-x-auto pb-3 mb-5 scrollbar-none">
        {categories.map(cat => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-all ${
              selectedCategory === cat
                ? 'bg-brand-600 text-white shadow-sm'
                : 'bg-slate-100 text-slate-600 hover:bg-slate-200 hover:text-slate-900'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Products Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5">
        {filteredList.map(product => (
          <div
            key={product.id}
            className={`rounded-2xl p-4 border transition-all flex flex-col justify-between ${
              product.availability
                ? 'bg-slate-50/70 hover:bg-white border-slate-200 hover:border-brand-300 hover:shadow-md'
                : 'bg-rose-50/40 border-rose-200'
            }`}
          >
            <div>
              {/* Product Header & Stock Badge */}
              <div className="flex items-start justify-between gap-2 mb-1.5">
                <div>
                  <h4 className="font-bold text-slate-900 text-sm">{product.name}</h4>
                  {product.hindi_name && (
                    <span className="text-[11px] text-slate-400 font-medium">{product.hindi_name}</span>
                  )}
                </div>
                <div className="text-right">
                  <span className="text-sm font-extrabold text-slate-900">₹{product.price}</span>
                  <span className="text-[10px] text-slate-400 block">/{product.unit}</span>
                </div>
              </div>

              {/* Brand and Category */}
              <div className="flex items-center space-x-1.5 my-2">
                {product.brand && (
                  <span className="text-[10px] font-semibold bg-white text-slate-700 px-2 py-0.5 rounded border border-slate-200">
                    {product.brand}
                  </span>
                )}
                <span className="text-[10px] font-semibold bg-slate-200 text-slate-700 px-2 py-0.5 rounded">
                  {product.category}
                </span>

                {!product.availability && (
                  <span className="text-[10px] font-bold bg-rose-100 text-rose-700 px-2 py-0.5 rounded border border-rose-200">
                    Out of Stock
                  </span>
                )}
              </div>

              {/* Attributes */}
              {product.attributes && product.attributes.length > 0 && (
                <div className="flex flex-wrap gap-1 mb-3">
                  {product.attributes.map((attr, aIdx) => (
                    <span key={aIdx} className="text-[9px] font-medium bg-emerald-50 text-emerald-700 px-1.5 py-0.5 rounded border border-emerald-100">
                      {attr}
                    </span>
                  ))}
                </div>
              )}
            </div>

            {/* Action Buttons */}
            {product.availability ? (
              <button
                onClick={() => onAddToCart(product)}
                className="w-full py-2 px-3 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold flex items-center justify-center space-x-1 shadow-sm transition-all active:scale-95"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>Add to Shopping List</span>
              </button>
            ) : (
              <button
                onClick={() => setSelectedSubstituteProduct(product)}
                className="w-full py-2 px-3 rounded-xl bg-orange-600 hover:bg-orange-700 text-white text-xs font-bold flex items-center justify-center space-x-1 shadow-sm transition-all active:scale-95 animate-pulse"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                <span>View Suggested Alternatives</span>
              </button>
            )}
          </div>
        ))}
      </div>

      {/* Substitutes Modal */}
      {selectedSubstituteProduct && (
        <SubstituteModal
          originalProductName={selectedSubstituteProduct.name}
          substitutes={selectedSubstituteProduct.substitutes || []}
          isOpen={true}
          onClose={() => setSelectedSubstituteProduct(null)}
          onSelectSubstitute={onSelectSubstitute}
        />
      )}
    </div>
  );
};
