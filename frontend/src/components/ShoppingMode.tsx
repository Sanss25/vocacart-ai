import React from 'react';
import type { ShoppingItem, VoiceState } from '../types';
import { Mic, ShoppingCart, Check, Sparkles, Trophy, Loader2 } from 'lucide-react';
import confetti from 'canvas-confetti';

interface ShoppingModeProps {
  items: ShoppingItem[];
  voiceState: VoiceState;
  interimTranscript: string;
  onStartListening: () => void;
  onStopListening: () => void;
  onTogglePurchased: (id: number, currentStatus: boolean) => void;
  onCompleteTrip: () => void;
  onExitShoppingMode: () => void;
}

export const ShoppingMode: React.FC<ShoppingModeProps> = ({
  items,
  voiceState,
  interimTranscript,
  onStartListening,
  onStopListening,
  onTogglePurchased,
  onCompleteTrip,
  onExitShoppingMode,
}) => {
  const pendingItems = items.filter(i => !i.is_purchased);
  const purchasedItems = items.filter(i => i.is_purchased);

  const currentItem = pendingItems[0] || null;
  const nextItem = pendingItems[1] || null;

  const totalCount = items.length;
  const completedCount = purchasedItems.length;
  const progressPercent = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 100;

  const isListening = voiceState === 'LISTENING';
  const isProcessing = voiceState === 'PROCESSING';

  const handleMarkCurrentBought = () => {
    if (currentItem) {
      confetti({
        particleCount: 35,
        spread: 50,
        origin: { y: 0.7 },
      });
      onTogglePurchased(currentItem.id, false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-950 text-white flex flex-col justify-between p-4 sm:p-8 overflow-y-auto animate-fade-in">
      {/* Top Bar: Progress and Exit */}
      <div className="max-w-3xl w-full mx-auto flex items-center justify-between pb-4 border-b border-slate-800">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-amber-500 to-orange-500 flex items-center justify-center font-bold text-white shadow-lg shadow-orange-500/20">
            <ShoppingCart className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h2 className="text-lg sm:text-xl font-black uppercase tracking-wider text-white">In-Store Shopping Mode</h2>
              <span className="text-[10px] font-bold bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded-full border border-amber-500/30">
                LIVE
              </span>
            </div>
            <p className="text-xs text-slate-400">
              {completedCount} of {totalCount} items in cart ({progressPercent}%)
            </p>
          </div>
        </div>

        <button
          onClick={onExitShoppingMode}
          className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold transition-all"
        >
          Exit Mode
        </button>
      </div>

      {/* Progress Bar */}
      <div className="max-w-3xl w-full mx-auto my-3">
        <div className="w-full h-2.5 bg-slate-800 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-brand-500 via-emerald-400 to-teal-400 transition-all duration-500"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
      </div>

      {/* Middle Focus Section */}
      <div className="max-w-2xl w-full mx-auto my-auto flex flex-col items-center text-center py-6">
        {currentItem ? (
          <>
            <span className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-2 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-amber-400" /> Current Item to Pick Up
            </span>

            <div className="w-full bg-gradient-to-b from-slate-900 to-slate-900/90 rounded-3xl p-6 sm:p-8 border-2 border-brand-500/50 shadow-2xl shadow-brand-500/10 mb-6">
              <h1 className="text-3xl sm:text-5xl font-black text-white tracking-tight mb-2">
                {currentItem.name}
              </h1>
              <div className="inline-flex items-center space-x-2 bg-brand-500/20 text-brand-300 px-4 py-1.5 rounded-full text-base font-bold border border-brand-400/30">
                <span>Quantity: {currentItem.quantity} {currentItem.unit}{currentItem.quantity > 1 ? 's' : ''}</span>
                {currentItem.brand && <span>· Brand: {currentItem.brand}</span>}
              </div>

              {nextItem && (
                <div className="mt-6 pt-4 border-t border-slate-800 flex items-center justify-center space-x-2 text-xs sm:text-sm text-slate-400">
                  <span className="text-slate-500">Up Next:</span>
                  <strong className="text-slate-200">{nextItem.name}</strong>
                  <span className="text-slate-500">({nextItem.quantity} {nextItem.unit})</span>
                </div>
              )}
            </div>

            <button
              onClick={handleMarkCurrentBought}
              className="w-full max-w-sm py-4 px-6 rounded-2xl bg-gradient-to-r from-brand-500 to-emerald-500 hover:from-brand-400 hover:to-emerald-400 text-slate-950 font-black text-base flex items-center justify-center space-x-2 shadow-lg shadow-brand-500/20 active:scale-95 transition-all mb-4"
            >
              <Check className="w-5 h-5 stroke-[3]" />
              <span>Mark "{currentItem.name}" as Bought</span>
            </button>
          </>
        ) : (
          <div className="w-full bg-gradient-to-b from-emerald-950/60 to-slate-900 rounded-3xl p-8 border border-emerald-500/40 text-center shadow-2xl">
            <div className="w-16 h-16 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center mx-auto mb-4 border border-emerald-500/40">
              <Trophy className="w-8 h-8 animate-bounce" />
            </div>
            <h2 className="text-3xl font-black text-white">All Items Complete! 🎉</h2>
            <p className="text-sm text-slate-300 mt-2 mb-6">
              You picked up everything on your shopping list. Ready to finish your trip?
            </p>
            <button
              onClick={onCompleteTrip}
              className="py-3.5 px-8 rounded-2xl bg-brand-500 hover:bg-brand-400 text-slate-950 font-extrabold text-sm shadow-lg shadow-brand-500/30 transition-all active:scale-95"
            >
              Complete Trip & Log to History
            </button>
          </div>
        )}

        <div className="text-center my-3">
          <p className="text-xs text-slate-400">
            Say: <strong className="text-brand-300 font-mono">"I've bought the {currentItem?.name || 'items'}"</strong> or <strong className="text-brand-300 font-mono">"{currentItem?.name || 'milk'} khareed liya"</strong>
          </p>
          {interimTranscript && (
            <div className="mt-2 text-xs font-mono text-brand-300 bg-brand-950/80 px-3 py-1.5 rounded-xl border border-brand-500/40 animate-pulse">
              🎙️ "{interimTranscript}"
            </div>
          )}
        </div>

        <button
          onClick={isListening ? onStopListening : onStartListening}
          disabled={isProcessing}
          className={`relative group w-20 h-20 rounded-full flex flex-col items-center justify-center transition-all duration-300 transform active:scale-95 shadow-2xl ${
            isListening
              ? 'bg-red-500 ring-4 ring-rose-400/40 shadow-red-500/50 scale-110'
              : 'bg-brand-500 hover:bg-brand-400 text-slate-950 shadow-brand-500/40'
          }`}
        >
          {isProcessing ? (
            <Loader2 className="w-8 h-8 text-white animate-spin" />
          ) : isListening ? (
            <Mic className="w-8 h-8 text-white animate-pulse" />
          ) : (
            <Mic className="w-8 h-8 text-slate-950" />
          )}
        </button>
      </div>

      {/* Bottom Checklist Quick Bar */}
      <div className="max-w-3xl w-full mx-auto pt-4 border-t border-slate-800">
        <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-2">
          Cart Checklist ({completedCount}/{totalCount})
        </span>
        <div className="flex items-center space-x-2 overflow-x-auto pb-2 scrollbar-none">
          {items.map(item => (
            <button
              key={item.id}
              onClick={() => onTogglePurchased(item.id, item.is_purchased)}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-xl text-xs font-bold whitespace-nowrap transition-all border ${
                item.is_purchased
                  ? 'bg-emerald-950/60 border-emerald-500/40 text-emerald-300 line-through'
                  : 'bg-slate-900 border-slate-700 text-white hover:border-brand-400'
              }`}
            >
              <span className={`w-4 h-4 rounded flex items-center justify-center text-[10px] ${
                item.is_purchased ? 'bg-emerald-500 text-slate-950' : 'border border-slate-500'
              }`}>
                {item.is_purchased && '✓'}
              </span>
              <span>{item.name}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
