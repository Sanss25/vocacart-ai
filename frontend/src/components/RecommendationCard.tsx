import React from 'react';
import type { RecommendationItem } from '../types';
import { Plus, X, Sparkles, AlertTriangle, Lightbulb, Clock } from 'lucide-react';

interface RecommendationCardProps {
  rec: RecommendationItem;
  onAdd: (rec: RecommendationItem) => void;
  onDismiss: (productName: string) => void;
}

export const RecommendationCard: React.FC<RecommendationCardProps> = ({
  rec,
  onAdd,
  onDismiss,
}) => {
  const percentageScore = Math.min(100, Math.round(rec.score * 100));

  return (
    <div className={`relative rounded-3xl p-5 border transition-all duration-200 hover:shadow-lg flex flex-col justify-between ${
      rec.is_urgent
        ? 'bg-gradient-to-br from-rose-50/70 via-white to-amber-50/40 border-rose-200/80 shadow-rose-500/5'
        : 'bg-gradient-to-br from-brand-50/40 via-white to-emerald-50/30 border-brand-200/70 shadow-emerald-500/5'
    }`}>
      <div>
        <div className="flex items-center justify-between gap-2 mb-2">
          {rec.is_urgent ? (
            <span className="inline-flex items-center space-x-1 px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase tracking-wide bg-rose-500 text-white shadow-sm">
              <AlertTriangle className="w-3 h-3" />
              <span>Low Stock Alert</span>
            </span>
          ) : (
            <span className="inline-flex items-center space-x-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wide bg-brand-100 text-brand-800 border border-brand-200">
              <Sparkles className="w-3 h-3 text-brand-600" />
              <span>Smart Habit Pick</span>
            </span>
          )}

          <div className="flex items-center space-x-1.5">
            <span className="text-[11px] font-bold text-slate-500 bg-white/90 px-2 py-0.5 rounded-md border border-slate-200">
              Score {percentageScore}%
            </span>
            <button
              onClick={() => onDismiss(rec.product_name)}
              title="Dismiss suggestion"
              className="text-slate-400 hover:text-slate-600 p-1 rounded-md hover:bg-slate-100 transition-colors"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        <h4 className="text-lg font-extrabold text-slate-900 tracking-tight">
          {rec.product_name}
        </h4>
        <p className="text-xs font-semibold text-slate-600 mt-0.5">
          Suggested: {rec.preferred_quantity} {rec.preferred_unit}{rec.preferred_brand ? ` (${rec.preferred_brand})` : ''} · ₹{rec.estimated_price}
        </p>

        {/* Explainable Rationale Box */}
        <div className="my-3 p-3 rounded-2xl bg-white/90 border border-slate-200/90 text-xs text-slate-700 shadow-sm flex items-start space-x-2">
          <Lightbulb className="w-4 h-4 text-amber-500 flex-shrink-0 mt-0.5" />
          <div className="flex-1">
            <strong className="text-slate-900 block text-[11px] font-bold uppercase tracking-wider">Why this suggestion?</strong>
            <p className="text-slate-600 text-xs leading-relaxed mt-0.5">{rec.explanation}</p>
          </div>
        </div>

        <div className="flex items-center space-x-1.5 text-[11px] text-slate-500 mb-3">
          <Clock className="w-3.5 h-3.5 text-slate-400" />
          <span>Usual cycle: every <strong>{rec.frequency_days} days</strong> (Last bought: <strong>{rec.days_since_last}d ago</strong>)</span>
        </div>
      </div>

      <button
        onClick={() => onAdd(rec)}
        className="w-full py-2.5 px-4 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs sm:text-sm flex items-center justify-center space-x-1.5 shadow-sm transition-all active:scale-95"
      >
        <Plus className="w-4 h-4" />
        <span>Add {rec.product_name}</span>
      </button>
    </div>
  );
};
