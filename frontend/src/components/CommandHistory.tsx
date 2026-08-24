import React from 'react';
import type { HistoryItem } from '../types';
import { History, RotateCcw, CheckCircle2 } from 'lucide-react';

interface CommandHistoryProps {
  history: HistoryItem[];
  onUndo: () => void;
}

export const CommandHistory: React.FC<CommandHistoryProps> = ({ history, onUndo }) => {
  if (!history || history.length === 0) return null;

  return (
    <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm">
      <div className="flex items-center justify-between pb-4 border-b border-slate-100 mb-4">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-xl bg-slate-100 text-slate-700 flex items-center justify-center font-bold">
            <History className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-xl font-extrabold text-slate-900 tracking-tight">Recent Voice & Text Activity</h3>
            <p className="text-xs text-slate-500">Live timeline of recent voice commands and NLU executions</p>
          </div>
        </div>

        <button
          onClick={onUndo}
          className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold border border-slate-200 transition-all active:scale-95"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>Undo Last</span>
        </button>
      </div>

      <div className="space-y-2.5">
        {history.slice(0, 6).map(cmd => (
          <div
            key={cmd.id}
            className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200/80 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs"
          >
            <div className="flex items-start space-x-2.5">
              <span className="text-slate-400 mt-0.5">🎙️</span>
              <div>
                <p className="font-semibold text-slate-800">"{cmd.raw_transcript}"</p>
                <div className="flex items-center space-x-2 mt-1">
                  <span className="text-[10px] font-bold bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded border border-indigo-200">
                    {cmd.intent}
                  </span>
                  <span className="text-[10px] text-slate-500 font-mono">
                    Lang: {cmd.language}
                  </span>
                </div>
              </div>
            </div>

            <div className="flex items-center space-x-2 text-emerald-700 font-medium bg-white px-3 py-1.5 rounded-xl border border-slate-200 self-start sm:self-center">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 flex-shrink-0" />
              <span>{cmd.action_message}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
