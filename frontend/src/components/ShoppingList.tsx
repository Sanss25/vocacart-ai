import React, { useState } from 'react';
import type { ShoppingItem } from '../types';
import { ShoppingItemCard } from './ShoppingItemCard';
import { ShoppingBag, RotateCcw, CheckCheck, Trash2, Plus } from 'lucide-react';

interface ShoppingListProps {
  items: ShoppingItem[];
  onTogglePurchased: (id: number, currentStatus: boolean) => void;
  onUpdateQuantity: (id: number, newQty: number) => void;
  onDelete: (id: number) => void;
  onClearAll: () => void;
  onClearPurchased: () => void;
  onUndo: () => void;
  onManualAdd: (name: string, quantity: number, unit: string) => void;
}

export const ShoppingList: React.FC<ShoppingListProps> = ({
  items,
  onTogglePurchased,
  onUpdateQuantity,
  onDelete,
  onClearAll,
  onClearPurchased,
  onUndo,
  onManualAdd,
}) => {
  const [showAddForm, setShowAddForm] = useState(false);
  const [newName, setNewName] = useState('');
  const [newQty, setNewQty] = useState(1);
  const [newUnit, setNewUnit] = useState('piece');

  const pendingItems = items.filter(i => !i.is_purchased);
  const purchasedItems = items.filter(i => i.is_purchased);

  const totalBudget = items.reduce((acc, i) => acc + (i.estimated_price || 0), 0);
  const pendingBudget = pendingItems.reduce((acc, i) => acc + (i.estimated_price || 0), 0);

  const categories = Array.from(new Set(items.map(i => i.category || 'Other'))).sort();

  const handleAddSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newName.trim()) return;
    onManualAdd(newName.trim(), newQty, newUnit);
    setNewName('');
    setNewQty(1);
    setShowAddForm(false);
  };

  return (
    <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm">
      {/* Header & Budget Summary */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-100">
        <div>
          <div className="flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-xl bg-brand-100 text-brand-700 flex items-center justify-center font-bold">
              <ShoppingBag className="w-4 h-4" />
            </div>
            <h2 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">Today's Shopping List</h2>
          </div>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            {pendingItems.length} pending · {purchasedItems.length} completed · {items.length} total items
          </p>
        </div>

        {/* Running Estimated Budget Badge */}
        <div className="flex items-center space-x-2 bg-slate-50 border border-slate-200 px-4 py-2 rounded-2xl">
          <div className="text-right">
            <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">Estimated Total</span>
            <span className="text-base font-extrabold text-slate-900">₹{totalBudget.toFixed(0)}</span>
          </div>
          {pendingBudget > 0 && pendingBudget !== totalBudget && (
            <span className="text-[11px] font-medium text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-lg border border-emerald-200">
              ₹{pendingBudget.toFixed(0)} left
            </span>
          )}
        </div>
      </div>

      {/* Action Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-2 py-4">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowAddForm(prev => !prev)}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-brand-50 hover:bg-brand-100 text-brand-800 text-xs font-bold border border-brand-200 transition-all active:scale-95"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Add Item</span>
          </button>

          <button
            onClick={onUndo}
            title="Undo last action"
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold border border-slate-200 transition-all active:scale-95"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Undo</span>
          </button>
        </div>

        <div className="flex items-center gap-2">
          {purchasedItems.length > 0 && (
            <button
              onClick={onClearPurchased}
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-medium border border-slate-200 transition-all"
            >
              <CheckCheck className="w-3.5 h-3.5 text-brand-600" />
              <span>Clear Done ({purchasedItems.length})</span>
            </button>
          )}

          {items.length > 0 && (
            <button
              onClick={onClearAll}
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl text-rose-600 hover:bg-rose-50 text-xs font-medium border border-transparent hover:border-rose-200 transition-all"
            >
              <Trash2 className="w-3.5 h-3.5" />
              <span>Clear All</span>
            </button>
          )}
        </div>
      </div>

      {/* Inline Add Item Form */}
      {showAddForm && (
        <form onSubmit={handleAddSubmit} className="mb-6 p-4 rounded-2xl bg-slate-50 border border-slate-200 animate-fade-in flex flex-wrap gap-2.5 items-center">
          <input
            type="text"
            placeholder="Item name (e.g., Greek Yogurt, Basmati Rice)"
            value={newName}
            onChange={e => setNewName(e.target.value)}
            className="flex-1 min-w-[180px] px-3.5 py-2 rounded-xl bg-white border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
            autoFocus
          />
          <input
            type="number"
            min="1"
            value={newQty}
            onChange={e => setNewQty(Math.max(1, parseInt(e.target.value) || 1))}
            className="w-20 px-3.5 py-2 rounded-xl bg-white border border-slate-300 text-sm text-center focus:outline-none focus:ring-2 focus:ring-brand-500"
          />
          <select
            value={newUnit}
            onChange={e => setNewUnit(e.target.value)}
            className="px-3.5 py-2 rounded-xl bg-white border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
          >
            <option value="piece">piece</option>
            <option value="packet">packet</option>
            <option value="bottle">bottle</option>
            <option value="kg">kg</option>
            <option value="g">g</option>
            <option value="litre">litre</option>
            <option value="dozen">dozen</option>
            <option value="box">box</option>
            <option value="loaf">loaf</option>
          </select>
          <button
            type="submit"
            disabled={!newName.trim()}
            className="px-4 py-2 rounded-xl bg-brand-600 hover:bg-brand-500 disabled:opacity-40 text-white font-bold text-sm shadow-sm transition-all"
          >
            Add
          </button>
        </form>
      )}

      {/* Empty State */}
      {items.length === 0 ? (
        <div className="text-center py-16 px-4">
          <div className="w-16 h-16 rounded-3xl bg-slate-100 text-slate-400 flex items-center justify-center mx-auto mb-4 border border-slate-200">
            <ShoppingBag className="w-8 h-8" />
          </div>
          <h3 className="text-lg font-bold text-slate-800">Your cart is empty</h3>
          <p className="text-sm text-slate-500 max-w-sm mx-auto mt-1 mb-6">
            Tap the microphone above and speak: "Add 2 packets of milk and 5 apples" to start building your list!
          </p>
        </div>
      ) : (
        <div className="space-y-6">
          {categories.map(category => {
            const categoryItems = items.filter(i => (i.category || 'Other') === category);
            if (categoryItems.length === 0) return null;

            return (
              <div key={category} className="space-y-2.5">
                <div className="flex items-center space-x-2">
                  <span className="text-xs font-extrabold uppercase tracking-wider text-slate-500">
                    {category}
                  </span>
                  <span className="text-[10px] font-bold bg-slate-100 text-slate-600 px-2 py-0.5 rounded-full">
                    {categoryItems.length}
                  </span>
                  <div className="flex-1 border-t border-slate-100" />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5">
                  {categoryItems.map(item => (
                    <ShoppingItemCard
                      key={item.id}
                      item={item}
                      onTogglePurchased={onTogglePurchased}
                      onUpdateQuantity={onUpdateQuantity}
                      onDelete={onDelete}
                    />
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
