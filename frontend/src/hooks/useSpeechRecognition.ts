import { useState, useEffect, useRef, useCallback } from 'react';
import type { VoiceState, LanguageMode } from '../types';

interface UseSpeechRecognitionProps {
  language: LanguageMode;
  onResult: (transcript: string) => void;
  onError?: (error: string) => void;
}

export function useSpeechRecognition({
  language,
  onResult,
  onError,
}: UseSpeechRecognitionProps) {
  const [voiceState, setVoiceState] = useState<VoiceState>('IDLE');
  const [interimTranscript, setInterimTranscript] = useState('');
  const [isSupported, setIsSupported] = useState(true);
  const [permissionError, setPermissionError] = useState<string | null>(null);

  // Keep latest callbacks without recreating SpeechRecognition
  const onResultRef = useRef(onResult);
  const onErrorRef = useRef(onError);

  useEffect(() => {
    onResultRef.current = onResult;
  }, [onResult]);

  useEffect(() => {
    onErrorRef.current = onError;
  }, [onError]);

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const recognitionRef = useRef<any>(null);
const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
const manuallyStoppedRef = useRef(false);



  const clearRecognitionTimeout = () => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
  };

  useEffect(() => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const SpeechRecognition =
      (window as any).SpeechRecognition ||
      (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setIsSupported(false);
      return;
    }

    setIsSupported(true);

    const recognition = new SpeechRecognition();

    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;

    if (language === 'hi') {
      recognition.lang = 'hi-IN';
    } else if (language === 'hinglish') {
      recognition.lang = 'en-IN';
    } else {
      recognition.lang = 'en-IN';
   }
    recognition.onstart = () => {
      console.log('[Speech] Started');

      manuallyStoppedRef.current = false;

      setVoiceState('LISTENING');
      setPermissionError(null);
      setInterimTranscript('');

      clearRecognitionTimeout();

      // Safety timeout.
      // Chrome sometimes keeps SpeechRecognition alive indefinitely.
      timeoutRef.current = setTimeout(() => {
        console.log('[Speech] Safety timeout - stopping');

        try {
          manuallyStoppedRef.current = true;
          recognition.stop();
        } catch {
          // ignore
        }

        setVoiceState('IDLE');
      }, 10000);
    };

    recognition.onresult = (event: any) => {
      let interim = '';
      let finalTranscript = '';

      for (
        let i = event.resultIndex;
        i < event.results.length;
        i++
      ) {
        const transcript = event.results[i][0].transcript;

        if (event.results[i].isFinal) {
          finalTranscript += transcript;
        } else {
          interim += transcript;
        }
      }

      if (interim) {
        setInterimTranscript(interim);
      }

      if (finalTranscript.trim()) {
        const text = finalTranscript.trim();

        console.log('[Speech] Final:', text);

        clearRecognitionTimeout();

        setInterimTranscript(text);
        setVoiceState('PROCESSING');

        // Stop immediately after receiving final speech
        try {
          manuallyStoppedRef.current = true;
          recognition.stop();
        } catch {
          // ignore
        }

        onResultRef.current(text);
      }
    };

    recognition.onerror = (event: any) => {
      console.warn('[Speech] Error:', event.error);

      clearRecognitionTimeout();

      // "aborted" commonly happens when we intentionally stop
      // recognition, so don't show it as a user-facing error.
      if (
        event.error === 'aborted' &&
        manuallyStoppedRef.current
      ) {
        return;
      }

      let msg =
        'Speech recognition failed. Try speaking again or typing.';

      if (
        event.error === 'not-allowed' ||
        event.error === 'permission-denied'
      ) {
        msg =
          'Microphone permission was denied. Please allow microphone access.';
        setPermissionError(msg);
      } else if (event.error === 'no-speech') {
        msg =
          'No speech was detected. Please try speaking again.';
      } else if (event.error === 'audio-capture') {
        msg =
          'Microphone could not be accessed. Check your microphone device.';
      } else if (event.error === 'network') {
        msg =
          'Speech recognition network error. Check your internet connection.';
      }

      setVoiceState('ERROR');

      if (onErrorRef.current) {
        onErrorRef.current(msg);
      }
    };

    recognition.onend = () => {
      console.log('[Speech] Ended');

      clearRecognitionTimeout();

      setVoiceState((prev) => {
        if (
          prev === 'PROCESSING' ||
          prev === 'SUCCESS'
        ) {
          return prev;
        }

        return 'IDLE';
      });
    };

    recognitionRef.current = recognition;

    return () => {
      clearRecognitionTimeout();

      try {
        manuallyStoppedRef.current = true;
        recognition.abort();
      } catch {
        // ignore
      }

      if (recognitionRef.current === recognition) {
        recognitionRef.current = null;
      }
    };
  }, [language]);

  const startListening = useCallback(() => {
    if (!isSupported) {
      onErrorRef.current?.(
        'Speech recognition is not supported in this browser.'
      );
      return;
    }

    const recognition = recognitionRef.current;

    if (!recognition) {
      onErrorRef.current?.(
        'Speech recognition is not initialized yet.'
      );
      return;
    }

    try {
      clearRecognitionTimeout();

      manuallyStoppedRef.current = false;

      setPermissionError(null);
      setInterimTranscript('');
      setVoiceState('LISTENING');

      console.log('[Speech] Starting...');

      recognition.start();
    } catch (error) {
      console.warn('[Speech] Start error:', error);

      // If recognition is already running, stop it first.
      try {
        recognition.stop();
      } catch {
        // ignore
      }

      setTimeout(() => {
        try {
          manuallyStoppedRef.current = false;
          recognition.start();
        } catch (err) {
          console.error('[Speech] Restart failed:', err);

          setVoiceState('ERROR');

          onErrorRef.current?.(
            'Could not start speech recognition. Please try again.'
          );
        }
      }, 300);
    }
  }, [isSupported]);

  const stopListening = useCallback(() => {
    console.log('[Speech] Manual stop');

    clearRecognitionTimeout();

    manuallyStoppedRef.current = true;

    try {
      recognitionRef.current?.stop();
    } catch {
      // ignore
    }

    setVoiceState('IDLE');
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