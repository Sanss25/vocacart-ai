import { useState, useEffect, useRef, useCallback } from 'react';
import type { VoiceState, LanguageMode } from '../types';

interface UseSpeechRecognitionProps {
  language: LanguageMode;
  onResult: (transcript: string) => void;
  onError?: (error: string) => void;
}

export function useSpeechRecognition({ language, onResult, onError }: UseSpeechRecognitionProps) {
  const [voiceState, setVoiceState] = useState<VoiceState>('IDLE');
  const [interimTranscript, setInterimTranscript] = useState('');
  const [isSupported, setIsSupported] = useState(true);
  const [permissionError, setPermissionError] = useState<string | null>(null);

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setIsSupported(false);
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;

    if (language === 'hi') {
      recognition.lang = 'hi-IN';
    } else if (language === 'hinglish') {
      recognition.lang = 'hi-IN';
    } else {
      recognition.lang = 'en-IN';
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    recognition.onstart = () => {
      setVoiceState('LISTENING');
      setPermissionError(null);
      setInterimTranscript('');
    };

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    recognition.onresult = (event: any) => {
      let currentInterim = '';
      let finalTranscript = '';

      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript;
        } else {
          currentInterim += event.results[i][0].transcript;
        }
      }

      if (currentInterim) {
        setInterimTranscript(currentInterim);
      }

      if (finalTranscript) {
        setInterimTranscript(finalTranscript);
        setVoiceState('PROCESSING');
        onResult(finalTranscript.trim());
      }
    };

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    recognition.onerror = (event: any) => {
      console.warn('Speech recognition error event:', event.error);
      let msg = 'Speech recognition failed. Try speaking again or typing.';
      if (event.error === 'not-allowed' || event.error === 'permission-denied') {
        msg = 'Microphone permission was denied. Please allow microphone access or use the text box below.';
        setPermissionError(msg);
      } else if (event.error === 'no-speech') {
        msg = 'No speech was detected. Please try speaking again.';
      }
      setVoiceState('ERROR');
      if (onError) onError(msg);
    };

    recognition.onend = () => {
      setVoiceState(prev => (prev === 'PROCESSING' || prev === 'SUCCESS' ? prev : 'IDLE'));
    };

    recognitionRef.current = recognition;

    return () => {
      if (recognitionRef.current) {
        try {
          recognitionRef.current.abort();
        } catch {
          // ignore
        }
      }
    };
  }, [language, onResult, onError]);

  const startListening = useCallback(() => {
    if (!isSupported) {
      if (onError) onError('Speech recognition is not supported in this browser. Please use the text input.');
      return;
    }

    try {
      setPermissionError(null);
      setVoiceState('LISTENING');
      recognitionRef.current?.start();
    } catch {
      try {
        recognitionRef.current?.stop();
        setTimeout(() => recognitionRef.current?.start(), 100);
      } catch (err) {
        console.error(err);
      }
    }
  }, [isSupported, onError]);

  const stopListening = useCallback(() => {
    try {
      recognitionRef.current?.stop();
    } catch {
      // ignore
    }
  }, []);

  return {
    voiceState,
    setVoiceState,
    interimTranscript,
    isSupported,
    permissionError,
    startListening,
    stopListening,
  };
}
