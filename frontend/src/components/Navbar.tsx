import React from 'react';
import { Volume2, VolumeX, ShoppingCart, Sparkles, SlidersHorizontal } from 'lucide-react';
import type { LanguageMode } from '../types';

interface NavbarProps {
  language: LanguageMode;
  onLanguageChange: (lang: LanguageMode) => void;
  isMuted: boolean;
  onToggleMute: () => void;
  isShoppingMode: boolean;
  onToggleShoppingMode: () => void;
  showPipeline: boolean;
  onTogglePipeline: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  language,
  onLanguageChange,
  isMuted,
  onToggleMute,
  isShoppingMode,
  onToggleShoppingMode,
  showPipeline,
  onTogglePipeline,
}) => {
  return (
    <header className="sticky top-0 z-40 glass-panel border-b border-slate-200/80 shadow-sm transition-all duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand Logo & Name */}
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-brand-600 to-emerald-400 flex items-center justify-center shadow-md shadow-brand-500/20 text-white">
            <ShoppingCart className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center space-x-1.5">
              <span className="font-extrabold text-xl tracking-tight text-slate-900">VocaCart</span>
              <span className="bg-brand-100 text-brand-800 text-xs font-bold px-1.5 py-0.5 rounded-md flex items-center gap-1 border border-brand-200">
                <Sparkles className="w-3 h-3 text-brand-600" /> AI
              </span>
            </div>
            <p className="text-[11px] font-medium text-slate-500 hidden sm:block">Multilingual Voice Shopping Companion</p>
          </div>
        </div>

        {/* Right Controls */}
        <div className="flex items-center space-x-2 sm:space-x-3">
          {/* Language Selector */}
          <div className="flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200 text-xs font-semibold">
            <button
              onClick={() => onLanguageChange('en')}
              className={`px-2.5 py-1 rounded-lg transition-all ${
                language === 'en'
                  ? 'bg-white text-brand-700 shadow-sm font-bold'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              EN
            </button>
            <button
              onClick={() => onLanguageChange('hi')}
              className={`px-2.5 py-1 rounded-lg transition-all ${
                language === 'hi'
                  ? 'bg-white text-brand-700 shadow-sm font-bold'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              हिन्दी
            </button>
            <button
              onClick={() => onLanguageChange('hinglish')}
              className={`px-2.5 py-1 rounded-lg transition-all ${
                language === 'hinglish'
                  ? 'bg-white text-brand-700 shadow-sm font-bold'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Hinglish
            </button>
          </div>

          {/* Audio TTS Toggle */}
          <button
            onClick={onToggleMute}
            title={isMuted ? 'Unmute voice feedback' : 'Mute voice feedback'}
            className={`p-2 rounded-xl border transition-all ${
              isMuted
                ? 'bg-slate-100 text-slate-400 border-slate-200 hover:bg-slate-200'
                : 'bg-brand-50 text-brand-700 border-brand-200 hover:bg-brand-100'
            }`}
          >
            {isMuted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
          </button>

          {/* Pipeline Inspector Toggle */}
          <button
            onClick={onTogglePipeline}
            title="Inspect AI NLU Pipeline"
            className={`hidden md:flex items-center space-x-1.5 px-3 py-1.5 rounded-xl border text-xs font-semibold transition-all ${
              showPipeline
                ? 'bg-indigo-50 text-indigo-700 border-indigo-200 shadow-sm'
                : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'
            }`}
          >
            <SlidersHorizontal className="w-3.5 h-3.5" />
            <span>AI Pipeline</span>
          </button>

          {/* Shopping Session Mode Switch */}
          <button
            onClick={onToggleShoppingMode}
            className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-xl font-bold text-xs sm:text-sm transition-all shadow-sm ${
              isShoppingMode
                ? 'bg-gradient-to-r from-amber-500 to-orange-500 text-white shadow-orange-500/20 animate-pulse'
                : 'bg-slate-900 hover:bg-slate-800 text-white'
            }`}
          >
            <ShoppingCart className="w-4 h-4" />
            <span>{isShoppingMode ? 'Exit Shopping' : '🛒 Shopping Mode'}</span>
          </button>
        </div>
      </div>
    </header>
  );
};
