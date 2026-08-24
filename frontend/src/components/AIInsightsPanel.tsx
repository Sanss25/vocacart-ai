import React from 'react';
import type { InsightSummary } from '../types';
import { Sparkles, TrendingUp, AlertCircle, IndianRupee } from 'lucide-react';

interface AIInsightsPanelProps {
  insights: InsightSummary | null;
}

export const AIInsightsPanel: React.FC<AIInsightsPanelProps> = ({ insights }) => {
  if (!insights) return null;

  const categories = Object.entries(insights.category_breakdown);

  return (
    <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm">
      {/* Header */}
      <div className="flex items-center justify-between pb-5 border-b border-slate-100 mb-6">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center font-bold">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-xl font-extrabold text-slate-900 tracking-tight">AI Shopping Insights & Habit Memory</h3>
            <p className="text-xs text-slate-500">Autonomous analytics derived from your purchasing frequency and patterns</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        {/* Habit Summary Card */}
        <div className="p-4 rounded-2xl bg-gradient-to-br from-purple-50 via-indigo-50/40 to-white border border-purple-100 flex flex-col justify-between">
          <div>
            <span className="text-[10px] font-extrabold uppercase tracking-wider text-purple-700 flex items-center gap-1 mb-1.5">
              <TrendingUp className="w-3.5 h-3.5" />
              🧠 Shopping Pattern Insight
            </span>
            <p className="text-xs font-medium text-slate-700 leading-relaxed">
              {insights.weekly_shopping_habit}
            </p>
          </div>
        </div>

        {/* Budget Insight Card */}
        <div className="p-4 rounded-2xl bg-gradient-to-br from-emerald-50 via-teal-50/40 to-white border border-emerald-100 flex flex-col justify-between">
          <div>
            <span className="text-[10px] font-extrabold uppercase tracking-wider text-emerald-700 flex items-center gap-1 mb-1.5">
              <IndianRupee className="w-3.5 h-3.5" />
              💰 Estimated Cart Budget
            </span>
            <div className="flex items-baseline space-x-2 mt-1">
              <span className="text-2xl font-black text-slate-900">₹{insights.total_estimated_budget}</span>
              <span className="text-xs text-slate-500 font-medium">({insights.pending_items} pending items)</span>
            </div>
            <div className="mt-2 text-[11px] text-emerald-800 font-medium">
              ₹{insights.purchased_budget} completed · ₹{insights.pending_budget} remaining
            </div>
          </div>
        </div>

        {/* Overdue / Urgent Restock Alerts Card */}
        <div className="p-4 rounded-2xl bg-gradient-to-br from-amber-50 via-orange-50/40 to-white border border-amber-100 flex flex-col justify-between">
          <div>
            <span className="text-[10px] font-extrabold uppercase tracking-wider text-amber-700 flex items-center gap-1 mb-1.5">
              <AlertCircle className="w-3.5 h-3.5" />
              ⏰ Restock Forecast
            </span>
            <div className="flex items-baseline space-x-2 mt-1">
              <span className="text-2xl font-black text-slate-900">{insights.urgent_recommendations_count}</span>
              <span className="text-xs text-slate-500 font-medium">items due for replenishment</span>
            </div>
            <p className="text-[11px] text-amber-800 mt-2 font-medium">
              Based on historical purchase intervals (e.g. Milk & Eggs cycle)
            </p>
          </div>
        </div>
      </div>

      {/* Category Breakdown & Spend Meters */}
      <div className="pt-4 border-t border-slate-100">
        <span className="text-xs font-extrabold uppercase tracking-wider text-slate-500 block mb-3">
          Category Distribution in Active List
        </span>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {categories.map(([category, count]) => {
            const spend = insights.category_spend[category] || 0;
            return (
              <div key={category} className="p-3 rounded-2xl bg-slate-50 border border-slate-200">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs font-bold text-slate-800 truncate">{category}</span>
                  <span className="text-[10px] font-bold bg-white text-slate-600 px-1.5 py-0.5 rounded border border-slate-200">
                    {count}
                  </span>
                </div>
                <span className="text-xs font-semibold text-slate-500">₹{spend.toFixed(0)}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
