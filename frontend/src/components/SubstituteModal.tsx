import React from 'react';
import type { SubstituteItem } from '../types';
import { X, RefreshCw, Plus, AlertCircle } from 'lucide-react';

interface SubstituteModalProps {
  originalProductName: string;
  substitutes: SubstituteItem[];
  isOpen: boolean;
  onClose: () => void;
  onSelectSubstitute: (sub: SubstituteItem) => void;
}

export const SubstituteModal: React.FC<SubstituteModalProps> = ({
  originalProductName,
  substitutes,
  isOpen,
  onClose,
  onSelectSubstitute,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-sm animate-fade-in">
      <div className="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-7 shadow-2xl border border-slate-200 overflow-hidden relative">
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-100 mb-4">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 rounded-xl bg-orange-100 text-orange-600 flex items-center justify-center font-bold">
              <RefreshCw className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-lg font-extrabold text-slate-900">Suggested Substitutes</h3>
              <p className="text-xs text-slate-500">
                Alternative recommendations for <span className="font-semibold text-rose-600">"{originalProductName}"</span>
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-slate-700 rounded-lg hover:bg-slate-100 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Unavailable Banner */}
        <div className="p-3 rounded-2xl bg-rose-50 border border-rose-200 text-xs text-rose-800 flex items-center space-x-2 mb-4">
          <AlertCircle className="w-4 h-4 flex-shrink-0 text-rose-600" />
          <span>The requested item is currently out of stock. Here are top-rated in-stock alternatives:</span>
        </div>

        {/* Substitutes List */}
        <div className="space-y-3 max-h-96 overflow-y-auto pr-1">
          {substitutes.length === 0 ? (
            <p className="text-sm text-slate-500 text-center py-6">No specific substitutes found.</p>
          ) : (
            substitutes.map((sub, idx) => (
              <div
                key={idx}
                className="p-4 rounded-2xl bg-slate-50 hover:bg-brand-50/40 border border-slate-200 hover:border-brand-300 transition-all flex flex-col justify-between space-y-2.5"
              >
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h4 className="font-bold text-slate-900 text-sm sm:text-base">{sub.substitute_name}</h4>
                    {sub.substitute_brand && (
                      <span className="text-[11px] font-semibold text-slate-500 bg-white px-2 py-0.5 rounded border border-slate-200 inline-block mt-0.5">
                        {sub.substitute_brand}
                      </span>
                    )}
                  </div>
                  <div className="text-right">
                    <span className="text-sm font-extrabold text-slate-900">₹{sub.substitute_price}</span>
                    {sub.original_price && (
                      <span className="text-[10px] text-slate-400 block line-through">₹{sub.original_price}</span>
                    )}
                  </div>
                </div>

                {/* Reason */}
                <p className="text-xs text-slate-600 bg-white p-2.5 rounded-xl border border-slate-200/80 leading-relaxed">
                  💡 <strong className="text-slate-800">Reason:</strong> {sub.reason}
                </p>

                {/* Attributes Tags & Add Button */}
                <div className="flex items-center justify-between pt-1">
                  <div className="flex flex-wrap gap-1">
                    {sub.attributes.map((attr, aIdx) => (
                      <span key={aIdx} className="text-[10px] font-medium bg-emerald-100/70 text-emerald-800 px-2 py-0.5 rounded-md">
                        {attr}
                      </span>
                    ))}
                  </div>

                  <button
                    onClick={() => {
                      onSelectSubstitute(sub);
                      onClose();
                    }}
                    className="py-1.5 px-3 rounded-xl bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold flex items-center space-x-1 shadow-sm transition-all active:scale-95"
                  >
                    <Plus className="w-3 h-3" />
                    <span>Choose This</span>
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
