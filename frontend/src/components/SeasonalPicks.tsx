import React from 'react';
import type { SeasonalItem } from '../types';
import { Leaf, Plus, Sun, CloudRain, Snowflake } from 'lucide-react';

interface SeasonalPicksProps {
  items: SeasonalItem[];
  onAddSeasonal: (item: SeasonalItem) => void;
}

export const SeasonalPicks: React.FC<SeasonalPicksProps> = ({ items, onAddSeasonal }) => {
  if (!items || items.length === 0) return null;

  const currentSeason = items[0]?.season || 'Summer';

  const getSeasonIcon = (season: string) => {
    if (season === 'Monsoon') return <CloudRain className="w-4 h-4 text-sky-500" />;
    if (season === 'Winter') return <Snowflake className="w-4 h-4 text-blue-500" />;
    return <Sun className="w-4 h-4 text-amber-500" />;
  };

  return (
    <div className="bg-gradient-to-r from-emerald-50 via-teal-50/60 to-emerald-50/40 rounded-3xl p-6 sm:p-8 border border-emerald-200/80 shadow-sm">
      <div className="flex items-center justify-between pb-4 border-b border-emerald-200/60 mb-5">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-xl bg-emerald-600 text-white flex items-center justify-center font-bold shadow-sm">
            <Leaf className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="text-xl font-extrabold text-slate-900 tracking-tight">🌱 Seasonal Picks</h3>
              <span className="inline-flex items-center space-x-1 px-2.5 py-0.5 rounded-full text-xs font-bold bg-white text-emerald-800 border border-emerald-200">
                {getSeasonIcon(currentSeason)}
                <span>{currentSeason} Specials</span>
              </span>
            </div>
            <p className="text-xs text-slate-600">Fresh in season now — hand-picked for the current weather</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5">
        {items.map((item, idx) => (
          <div
            key={idx}
            className="bg-white rounded-2xl p-4 border border-emerald-200/80 shadow-sm hover:shadow-md transition-all flex flex-col justify-between"
          >
            <div>
              <div className="flex items-start justify-between gap-2 mb-2">
                <h4 className="font-bold text-slate-900 text-sm">{item.name}</h4>
                <span className="text-xs font-extrabold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">
                  ₹{item.price}
                </span>
              </div>
              <p className="text-xs text-slate-500 leading-relaxed mb-3">{item.reason}</p>
            </div>

            <button
              onClick={() => onAddSeasonal(item)}
              className="w-full py-2 px-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold flex items-center justify-center space-x-1 shadow-sm transition-all active:scale-95"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>Add to List</span>
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};
