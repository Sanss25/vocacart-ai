import React from 'react';
import type { ShoppingItem } from '../types';
import { Plus, Minus, Trash2, Check } from 'lucide-react';
import confetti from 'canvas-confetti';

interface ShoppingItemCardProps {
  item: ShoppingItem;
  onTogglePurchased: (id: number, currentStatus: boolean) => void;
  onUpdateQuantity: (id: number, newQty: number) => void;
  onDelete: (id: number) => void;
}

const CATEGORY_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  Produce: { bg: 'bg-emerald-50', text: 'text-emerald-700', border: 'border-emerald-200' },
  Dairy: { bg: 'bg-sky-50', text: 'text-sky-700', border: 'border-sky-200' },
  Bakery: { bg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-200' },
  Beverages: { bg: 'bg-purple-50', text: 'text-purple-700', border: 'border-purple-200' },
  Snacks: { bg: 'bg-orange-50', text: 'text-orange-700', border: 'border-orange-200' },
  Pantry: { bg: 'bg-yellow-50', text: 'text-yellow-800', border: 'border-yellow-200' },
  Meat: { bg: 'bg-rose-50', text: 'text-rose-700', border: 'border-rose-200' },
  Household: { bg: 'bg-teal-50', text: 'text-teal-700', border: 'border-teal-200' },
  'Personal Care': { bg: 'bg-pink-50', text: 'text-pink-700', border: 'border-pink-200' },
  Frozen: { bg: 'bg-blue-50', text: 'text-blue-700', border: 'border-blue-200' },
  Other: { bg: 'bg-slate-50', text: 'text-slate-700', border: 'border-slate-200' },
};

export const ShoppingItemCard: React.FC<ShoppingItemCardProps> = ({
  item,
  onTogglePurchased,
  onUpdateQuantity,
  onDelete,
}) => {
  const catStyle = CATEGORY_COLORS[item.category] || CATEGORY_COLORS.Other;

  const handleCheckboxClick = () => {
    if (!item.is_purchased) {
      confetti({
        particleCount: 25,
        spread: 40,
        origin: { y: 0.8 },
      });
    }
    onTogglePurchased(item.id, item.is_purchased);
  };

  return (
    <div
      className={`group relative rounded-2xl p-4 transition-all duration-200 border ${
        item.is_purchased
          ? 'bg-slate-50/80 border-slate-200/80 opacity-60'
          : 'bg-white border-slate-200/80 hover:border-brand-300 hover:shadow-md'
      }`}
    >
      <div className="flex items-center justify-between gap-3">
        {/* Left Checkbox and Details */}
        <div className="flex items-center space-x-3.5 flex-1 min-w-0">
          <button
            onClick={handleCheckboxClick}
            aria-label={item.is_purchased ? 'Mark as not purchased' : 'Mark as purchased'}
            className={`w-6 h-6 rounded-lg flex items-center justify-center transition-all ${
              item.is_purchased
                ? 'bg-brand-600 text-white shadow-sm ring-2 ring-brand-200'
                : 'border-2 border-slate-300 hover:border-brand-500 bg-white text-transparent'
            }`}
          >
            <Check className="w-3.5 h-3.5 stroke-[3]" />
          </button>

          <div className="flex-1 min-w-0">
            <div className="flex items-center space-x-2">
              <h4
                className={`text-base font-bold truncate transition-all ${
                  item.is_purchased ? 'line-through text-slate-400 font-medium' : 'text-slate-900'
                }`}
              >
                {item.name}
              </h4>
              {item.brand && (
                <span className="text-[11px] font-semibold text-slate-500 bg-slate-100 px-2 py-0.5 rounded-md border border-slate-200">
                  {item.brand}
                </span>
              )}
            </div>

            <div className="flex items-center space-x-2 mt-1">
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-md border ${catStyle.bg} ${catStyle.text} ${catStyle.border}`}>
                {item.category}
              </span>
              {item.estimated_price && (
                <span className="text-xs font-semibold text-slate-700">
                  ₹{item.estimated_price}
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Right Quantity Controls and Delete */}
        <div className="flex items-center space-x-2.5">
          <div className="flex items-center bg-slate-100/90 rounded-xl p-1 border border-slate-200">
            <button
              onClick={() => onUpdateQuantity(item.id, Math.max(1, item.quantity - 1))}
              disabled={item.quantity <= 1}
              className="w-6 h-6 rounded-lg bg-white hover:bg-slate-200 disabled:opacity-30 flex items-center justify-center text-slate-700 transition-all"
            >
              <Minus className="w-3 h-3" />
            </button>
            <span className="text-xs font-bold text-slate-800 px-2.5 min-w-[2.5rem] text-center">
              {item.quantity} <span className="text-[10px] font-medium text-slate-500">{item.unit}</span>
            </span>
            <button
              onClick={() => onUpdateQuantity(item.id, item.quantity + 1)}
              className="w-6 h-6 rounded-lg bg-white hover:bg-slate-200 flex items-center justify-center text-slate-700 transition-all"
            >
              <Plus className="w-3 h-3" />
            </button>
          </div>

          <button
            onClick={() => onDelete(item.id)}
            title="Delete item"
            className="p-2 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-xl transition-all"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
