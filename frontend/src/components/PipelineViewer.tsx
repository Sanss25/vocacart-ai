import React from 'react';
import type { PipelineInspection } from '../types';
import { Cpu, FileText, CheckCircle2, Volume2, Database, Layers } from 'lucide-react';

interface PipelineViewerProps {
  pipeline: PipelineInspection | null;
  onClose?: () => void;
}

export const PipelineViewer: React.FC<PipelineViewerProps> = ({ pipeline, onClose }) => {
  if (!pipeline) {
    return (
      <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-sm text-center">
        <Layers className="w-8 h-8 text-slate-400 mx-auto mb-2" />
        <h3 className="text-sm font-bold text-slate-800">AI Pipeline Inspector</h3>
        <p className="text-xs text-slate-500 mt-1">
          Speak or type a command above to see the step-by-step NLU reasoning and entity extraction telemetry.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-slate-900 text-white rounded-3xl p-6 border border-slate-800 shadow-xl overflow-hidden relative">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
        <div className="flex items-center space-x-2">
          <div className="p-1.5 rounded-lg bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">
            <Cpu className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              NLU Processing Pipeline Telemetry
              <span className="text-[10px] font-semibold uppercase bg-indigo-500/20 text-indigo-300 px-2 py-0.5 rounded-full border border-indigo-500/30">
                Confidence {(pipeline.confidence * 100).toFixed(0)}%
              </span>
            </h3>
            <p className="text-[11px] text-slate-400">Transparent AI intent detection and structured entity extraction breakdown</p>
          </div>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            className="text-xs text-slate-400 hover:text-white px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 transition-colors"
          >
            Hide
          </button>
        )}
      </div>

      {/* Visual Pipeline Flow Stages */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {/* Stage 1: Input & Normalization */}
        <div className="bg-slate-950/60 rounded-2xl p-3.5 border border-slate-800/80">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
              <FileText className="w-3 h-3 text-brand-400" />
              1. Input Normalization
            </span>
            <span className="text-[10px] bg-slate-800 text-brand-300 px-2 py-0.5 rounded-md font-mono">
              Lang: {pipeline.detected_language}
            </span>
          </div>
          <div className="space-y-1.5">
            <div>
              <span className="text-[10px] text-slate-500 block">Raw Transcript:</span>
              <p className="text-xs font-mono text-slate-200 bg-slate-900 p-1.5 rounded border border-slate-800">
                "{pipeline.raw_transcript}"
              </p>
            </div>
            <div>
              <span className="text-[10px] text-slate-500 block">Normalized:</span>
              <p className="text-xs font-mono text-emerald-300 bg-slate-900 p-1.5 rounded border border-slate-800">
                {pipeline.normalized_text}
              </p>
            </div>
          </div>
        </div>

        {/* Stage 2: Intent & Entity Parsing */}
        <div className="bg-slate-950/60 rounded-2xl p-3.5 border border-slate-800/80">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
              <Cpu className="w-3 h-3 text-indigo-400" />
              2. Intent & Entities
            </span>
            <span className="text-[10px] bg-indigo-500/20 text-indigo-300 px-2 py-0.5 rounded-md font-bold font-mono">
              {pipeline.intent}
            </span>
          </div>
          <div className="bg-slate-900 p-2 rounded-lg border border-slate-800 font-mono text-[11px] text-slate-300 max-h-28 overflow-y-auto">
            <pre className="text-xs text-indigo-200 whitespace-pre-wrap">
              {JSON.stringify(pipeline.entities, null, 2)}
            </pre>
          </div>
        </div>

        {/* Stage 3: Execution & Output */}
        <div className="bg-slate-950/60 rounded-2xl p-3.5 border border-slate-800/80">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
              <Database className="w-3 h-3 text-amber-400" />
              3. Execution & Voice
            </span>
            <span className="text-[10px] bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded-md font-mono">
              {pipeline.action_executed}
            </span>
          </div>
          <div className="space-y-1.5">
            <div className="flex items-start gap-1.5 text-xs text-slate-300 bg-slate-900 p-1.5 rounded border border-slate-800">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0 mt-0.5" />
              <span>{pipeline.confirmation_message}</span>
            </div>
            <div className="flex items-start gap-1.5 text-xs text-brand-300 bg-slate-900 p-1.5 rounded border border-slate-800">
              <Volume2 className="w-3.5 h-3.5 text-brand-400 flex-shrink-0 mt-0.5" />
              <span className="italic font-mono">"{pipeline.tts_text}"</span>
            </div>
          </div>
        </div>
      </div>

      {/* Reasoning Footer */}
      <div className="mt-3 pt-2.5 border-t border-slate-800/80 flex items-center gap-2 text-xs text-slate-400">
        <span className="font-bold text-slate-300">💡 Reasoning Logic:</span>
        <span>{pipeline.reasoning}</span>
      </div>
    </div>
  );
};
