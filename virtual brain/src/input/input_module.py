"""Input Module - Voice and text input handling using sounddevice (no pyaudio needed)"""

import io
import wave
import numpy as np
import sounddevice as sd
import speech_recognition as sr
from typing import Optional


DEFAULT_MIC_INDEX = 1
SAMPLE_RATE = 16000
CHANNELS = 1

# Silence detection tuning
SILENCE_THRESHOLD = 500      # RMS below this = silence
SILENCE_DURATION  = 1.0      # seconds of silence before stopping
MAX_RECORD_SECS   = 10       # hard cap


class InputModule:
    """
    Handles voice and text input.
    Uses sounddevice for audio capture (works on Python 3.14 without pyaudio).
    Stops recording automatically after silence — no fixed wait time.
    """

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.6
        self.microphone_available = self._check_microphone_availability()

    def _check_microphone_availability(self) -> bool:
        try:
            devices = sd.query_devices()
            for d in devices:
                if d['max_input_channels'] > 0:
                    return True
            return False
        except Exception:
            return False

    def capture_text_input(self, text: str) -> str:
        if text is None:
            raise ValueError("Text input cannot be None")
        if not isinstance(text, str):
            raise ValueError("Text input must be a string")
        if not text.strip():
            raise ValueError("Text input cannot be empty")
        return text

    def capture_voice_input(self, timeout: int = 10, phrase_time_limit: int = 15) -> str:
        """
        Record audio, stopping automatically when silence is detected.
        Much faster than waiting a fixed duration.
        """
        if not self.microphone_available:
            raise RuntimeError("No microphone detected. Please connect a microphone.")

        try:
            chunk_size   = int(SAMPLE_RATE * 0.1)   # 100 ms chunks
            silence_chunks = int(SILENCE_DURATION / 0.1)
            max_chunks   = int(MAX_RECORD_SECS / 0.1)

            recorded_chunks = []
            silent_count    = 0
            speech_started  = False

            with sd.InputStream(
                samplerate=SAMPLE_RATE,
                channels=CHANNELS,
                dtype='int16',
                device=DEFAULT_MIC_INDEX,
                blocksize=chunk_size
            ) as stream:
                for _ in range(max_chunks):
                    chunk, _ = stream.read(chunk_size)
                    rms = int(np.sqrt(np.mean(chunk.astype(np.float32) ** 2)))

                    if rms > SILENCE_THRESHOLD:
                        speech_started = True
                        silent_count   = 0
                        recorded_chunks.append(chunk.copy())
                    else:
                        if speech_started:
                            recorded_chunks.append(chunk.copy())
                            silent_count += 1
                            if silent_count >= silence_chunks:
                                break   # enough silence after speech → stop

            if not recorded_chunks:
                raise ValueError("No speech detected. Please try again.")

            # Stitch chunks → WAV in memory
            audio_data = np.concatenate(recorded_chunks, axis=0)
            wav_buffer = io.BytesIO()
            with wave.open(wav_buffer, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(2)
                wf.setframerate(SAMPLE_RATE)
                wf.writeframes(audio_data.tobytes())
            wav_buffer.seek(0)

            # Transcribe
            with sr.AudioFile(wav_buffer) as source:
                audio = self.recognizer.record(source)

            text = self.recognizer.recognize_google(audio)
            if not text or not text.strip():
                raise ValueError("Speech recognition returned empty text.")
            return text

        except sr.UnknownValueError:
            raise ValueError("Could not understand audio. Please speak clearly.")
        except sr.RequestError as e:
            raise ValueError(f"Speech recognition error: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Voice capture error: {str(e)}")

    def get_input(self, text: Optional[str] = None, use_voice: bool = False) -> str:
        if text is not None:
            return self.capture_text_input(text)
        if use_voice and self.microphone_available:
            try:
                return self.capture_voice_input()
            except (RuntimeError, ValueError) as e:
                raise ValueError(f"Voice input failed: {str(e)}")
        if use_voice and not self.microphone_available:
            raise RuntimeError("Microphone unavailable. Please use text input.")
        raise ValueError("No input provided.")
