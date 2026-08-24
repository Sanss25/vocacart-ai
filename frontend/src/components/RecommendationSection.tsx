import React from 'react';
import type { RecommendationItem } from '../types';
import { RecommendationCard } from './RecommendationCard';
import { BrainCircuit, RefreshCw } from 'lucide-react';

interface RecommendationSectionProps {
  recommendations: RecommendationItem[];
  onAdd: (rec: RecommendationItem) => void;
  onDismiss: (productName: string) => void;
  onRefresh: () => void;
  isLoading?: boolean;
}

export const RecommendationSection: React.FC<RecommendationSectionProps> = ({
  recommendations,
  onAdd,
  onDismiss,
  onRefresh,
  isLoading,
}) => {
  if (recommendations.length === 0) return null;

  return (
    <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm">
      <div className="flex items-center justify-between pb-4 border-b border-slate-100 mb-6">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-xl bg-purple-100 text-purple-700 flex items-center justify-center font-bold">
            <BrainCircuit className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-xl font-extrabold text-slate-900 tracking-tight">Smart Restock Recommendations</h3>
            <p className="text-xs text-slate-500">Calculated from your historical buying frequency & purchase intervals</p>
          </div>
        </div>

        <button
          onClick={onRefresh}
          disabled={isLoading}
          title="Recalculate recommendations"
          className="p-2 rounded-xl text-slate-500 hover:text-slate-900 hover:bg-slate-100 border border-slate-200 transition-all active:scale-95 disabled:opacity-40"
        >
          <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {recommendations.map(rec => (
          <RecommendationCard
            key={rec.product_name}
            rec={rec}
            onAdd={onAdd}
            onDismiss={onDismiss}
          />
        ))}
      </div>
    </div>
  );
};
