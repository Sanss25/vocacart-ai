import { useState, useCallback, useEffect } from 'react';
import type { LanguageMode } from '../types';

export function useTextToSpeech(initialMuted = false) {
  const [isMuted, setIsMuted] = useState<boolean>(() => {
    const saved = localStorage.getItem('vocacart_tts_muted');
    return saved !== null ? JSON.parse(saved) : initialMuted;
  });

  const [isSpeaking, setIsSpeaking] = useState(false);

  useEffect(() => {
    localStorage.setItem('vocacart_tts_muted', JSON.stringify(isMuted));
  }, [isMuted]);

  const speak = useCallback((text: string, language: LanguageMode = 'en') => {
    if (isMuted || !text || !('speechSynthesis' in window)) {
      return;
    }

    try {
      window.speechSynthesis.cancel();

      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 1.0;
      utterance.pitch = 1.0;

      const voices = window.speechSynthesis.getVoices();
      if (language === 'hi' || language === 'hinglish') {
        const hindiVoice = voices.find(v => v.lang.includes('hi') || v.name.toLowerCase().includes('hindi') || v.name.toLowerCase().includes('india'));
        if (hindiVoice) utterance.voice = hindiVoice;
        utterance.lang = 'hi-IN';
      } else {
        const engVoice = voices.find(v => (v.lang === 'en-IN' || v.lang === 'en-US' || v.lang === 'en-GB') && !v.name.includes('Google'));
        if (engVoice) utterance.voice = engVoice;
        utterance.lang = 'en-US';
      }

      utterance.onstart = () => setIsSpeaking(true);
      utterance.onend = () => setIsSpeaking(false);
      utterance.onerror = () => setIsSpeaking(false);

      window.speechSynthesis.speak(utterance);
    } catch (e) {
      console.warn('Speech synthesis failed:', e);
      setIsSpeaking(false);
    }
  }, [isMuted]);

  const stopSpeaking = useCallback(() => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    }
  }, []);

  const toggleMute = useCallback(() => {
    setIsMuted(prev => {
      if (!prev && 'speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
      return !prev;
    });
  }, []);

  return {
    isMuted,
    isSpeaking,
    toggleMute,
    speak,
    stopSpeaking
  };
}
