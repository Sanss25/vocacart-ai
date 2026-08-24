import React, { useState } from 'react';
import { Mic, Send, Sparkles, Loader2, CheckCircle2, AlertCircle, Play } from 'lucide-react';
import type { VoiceState, LanguageMode } from '../types';

interface VoiceHeroProps {
  voiceState: VoiceState;
  interimTranscript: string;
  onStartListening: () => void;
  onStopListening: () => void;
  onSubmitText: (text: string) => void;
  permissionError: string | null;
  lastMessage: string | null;
  language: LanguageMode;
}

export const VoiceHero: React.FC<VoiceHeroProps> = ({
  voiceState,
  interimTranscript,
  onStartListening,
  onStopListening,
  onSubmitText,
  permissionError,
  lastMessage,
  language,
}) => {
  const [inputText, setInputText] = useState('');

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim()) return;
    onSubmitText(inputText.trim());
    setInputText('');
  };

  const handleDemoClick = (command: string) => {
    onSubmitText(command);
  };

  const isListening = voiceState === 'LISTENING';
  const isProcessing = voiceState === 'PROCESSING';

  const demoCommands = language === 'hi'
    ? [
        "दो पैकेट अमूल दूध और पांच सेब जोड़ो",
        "ब्रेड हटा दो",
        "300 रुपये के अंदर सेब ढूंढो",
        "मुझे क्या खरीदना चाहिए?",
        "दूध खरीद लिया",
      ]
    : language === 'hinglish'
    ? [
        "Do packet Amul milk aur 5 apples add karo",
        "Bread hata do",
        "Find organic apples under 300 rupees",
        "Kya khareedna chahiye?",
        "Milk khareed liya",
      ]
    : [
        "I need two packets of milk, five apples and a loaf of bread",
        "Remove bread",
        "Find organic apples under ₹300",
        "What should I buy?",
        "I've bought the milk",
      ];

  return (
    <div className="relative overflow-hidden rounded-3xl bg-gradient-to-b from-emerald-900 via-slate-900 to-slate-950 text-white p-6 sm:p-10 shadow-xl border border-emerald-800/40">
      <div className="absolute -top-24 -left-24 w-72 h-72 bg-brand-500/20 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-24 -right-24 w-72 h-72 bg-emerald-500/15 rounded-full blur-3xl pointer-events-none" />

      <div className="relative z-10 max-w-3xl mx-auto text-center flex flex-col items-center">
        <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-brand-500/10 border border-brand-400/30 text-brand-300 text-xs font-semibold tracking-wide mb-4">
          <Sparkles className="w-3.5 h-3.5 text-brand-400 animate-spin-slow" />
          <span>Voice-Powered Intelligent Supermarket Cart</span>
        </div>

        <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-white mb-2">
          Speak Naturally. <span className="bg-clip-text text-transparent bg-gradient-to-r from-brand-300 via-emerald-200 to-teal-200">Shop Smarter.</span>
        </h1>
        <p className="text-slate-300 text-sm sm:text-base max-w-xl mb-8">
          Manage your grocery list, discover low-stock essentials, and compare items hands-free in English, हिन्दी, or Hinglish.
        </p>

        {/* Big Microphone Button */}
        <div className="relative my-4 flex flex-col items-center">
          {isListening && (
            <>
              <div className="absolute inset-0 rounded-full bg-brand-400/30 animate-ping pointer-events-none scale-125" />
              <div className="absolute -inset-4 rounded-full bg-emerald-500/20 animate-pulse pointer-events-none" />
            </>
          )}

          <button
            onClick={isListening ? onStopListening : onStartListening}
            disabled={isProcessing}
            aria-label={isListening ? 'Stop listening' : 'Start voice recognition'}
            className={`relative group w-28 h-28 sm:w-32 sm:h-32 rounded-full flex flex-col items-center justify-center transition-all duration-300 transform active:scale-95 shadow-2xl ${
              isListening
                ? 'bg-gradient-to-tr from-red-500 to-rose-600 shadow-red-500/50 scale-105 ring-4 ring-rose-300/40'
                : isProcessing
                ? 'bg-gradient-to-tr from-amber-500 to-amber-600 shadow-amber-500/40'
                : 'bg-gradient-to-tr from-brand-500 to-emerald-600 hover:from-brand-400 hover:to-emerald-500 shadow-brand-500/40 hover:scale-105'
            }`}
          >
            {isProcessing ? (
              <Loader2 className="w-12 h-12 text-white animate-spin" />
            ) : isListening ? (
              <div className="flex items-center space-x-1.5 h-10 px-2">
                <span className="w-1.5 bg-white rounded-full animate-wave-1" />
                <span className="w-1.5 bg-white rounded-full animate-wave-2" />
                <span className="w-1.5 bg-white rounded-full animate-wave-3" />
                <span className="w-1.5 bg-white rounded-full animate-wave-4" />
                <span className="w-1.5 bg-white rounded-full animate-wave-5" />
              </div>
            ) : (
              <Mic className="w-12 h-12 text-white group-hover:scale-110 transition-transform" />
            )}

            <span className="text-[11px] font-bold uppercase tracking-wider text-white/90 mt-1">
              {isListening ? 'Listening...' : isProcessing ? 'Thinking...' : 'Tap to speak'}
            </span>
          </button>

          {/* Voice State Badge */}
          <div className="mt-4 flex items-center space-x-2">
            <span
              className={`inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-bold border ${
                voiceState === 'LISTENING'
                  ? 'bg-rose-500/20 text-rose-300 border-rose-500/40 animate-pulse'
                  : voiceState === 'PROCESSING'
                  ? 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                  : voiceState === 'SUCCESS'
                  ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
                  : voiceState === 'ERROR'
                  ? 'bg-red-500/20 text-red-300 border-red-500/40'
                  : 'bg-slate-800/80 text-slate-300 border-slate-700'
              }`}
            >
              <span className={`w-2 h-2 rounded-full ${
                voiceState === 'LISTENING' ? 'bg-rose-400 animate-ping' :
                voiceState === 'PROCESSING' ? 'bg-amber-400' :
                voiceState === 'SUCCESS' ? 'bg-emerald-400' :
                voiceState === 'ERROR' ? 'bg-red-400' : 'bg-slate-400'
              }`} />
              <span>{voiceState}</span>
            </span>

            <span className="text-xs text-slate-400 font-medium">
              Lang: <strong className="text-white uppercase">{language}</strong>
            </span>
          </div>
        </div>

        {/* Live Transcript Bubble */}
        {interimTranscript && (
          <div className="w-full max-w-xl my-3 p-3 rounded-2xl bg-white/10 backdrop-blur-md border border-white/20 text-sm text-brand-200 font-medium animate-fade-in flex items-center justify-center space-x-2">
            <span className="text-brand-400">🎙️</span>
            <span>"{interimTranscript}"</span>
          </div>
        )}

        {/* Status Confirmation / Error Messages */}
        {lastMessage && !interimTranscript && (
          <div className="w-full max-w-xl my-2 p-3 rounded-2xl bg-emerald-950/80 border border-emerald-600/40 text-xs sm:text-sm text-emerald-200 flex items-center justify-center space-x-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
            <span>{lastMessage}</span>
          </div>
        )}

        {permissionError && (
          <div className="w-full max-w-xl my-2 p-3 rounded-2xl bg-rose-950/80 border border-rose-600/40 text-xs sm:text-sm text-rose-200 flex items-center justify-center space-x-2">
            <AlertCircle className="w-4 h-4 text-rose-400 flex-shrink-0" />
            <span>{permissionError}</span>
          </div>
        )}

        {/* Fallback Text Input */}
        <form onSubmit={handleFormSubmit} className="w-full max-w-xl mt-4 flex items-center gap-2">
          <div className="relative flex-1">
            <input
              type="text"
              value={inputText}
              onChange={e => setInputText(e.target.value)}
              placeholder="Or type here: 'Add 2 packets of milk' or 'दूध जोड़ो'..."
              className="w-full px-4 py-3 rounded-2xl bg-white/10 border border-white/20 text-white placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400 focus:bg-white/15 transition-all"
            />
          </div>
          <button
            type="submit"
            disabled={!inputText.trim()}
            className="px-5 py-3 rounded-2xl bg-brand-500 hover:bg-brand-400 disabled:opacity-40 disabled:hover:bg-brand-500 text-slate-950 font-bold text-sm flex items-center gap-1.5 transition-all shadow-md active:scale-95"
          >
            <span>Send</span>
            <Send className="w-4 h-4" />
          </button>
        </form>

        {/* Quick Demo Chips */}
        <div className="w-full max-w-2xl mt-6 pt-5 border-t border-white/10 text-left">
          <div className="flex items-center justify-between mb-2.5">
            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <Play className="w-3 h-3 text-brand-400 fill-brand-400" />
              Quick Demo Evaluator Prompts (Click to Run)
            </span>
          </div>
          <div className="flex flex-wrap gap-2">
            {demoCommands.map((cmd, idx) => (
              <button
                key={idx}
                onClick={() => handleDemoClick(cmd)}
                className="text-xs bg-white/10 hover:bg-white/20 text-slate-200 hover:text-white px-3 py-1.5 rounded-xl border border-white/10 transition-all active:scale-95 flex items-center gap-1.5"
              >
                <span>🎙️</span>
                <span>"{cmd}"</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
