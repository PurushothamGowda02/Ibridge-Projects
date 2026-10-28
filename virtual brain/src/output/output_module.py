"""
Output Module - Text display and text-to-speech output.
Creates a fresh pyttsx3 engine per speak call to avoid 'run loop already started' on Windows.
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class OutputModule:
    """Manages text display and voice synthesis output."""

    def __init__(self, voice_enabled: bool = True):
        self.voice_enabled = voice_enabled
        self.last_displayed_text: Optional[str] = None
        self._tts_available = self._test_tts()

    def _test_tts(self) -> bool:
        try:
            import pyttsx3
            e = pyttsx3.init()
            e.stop()
            return True
        except Exception as e:
            logger.warning(f"TTS not available: {e}")
            return False

    def display_text(self, text: str) -> str:
        if not text:
            text = ""
        self.last_displayed_text = text
        return text

    def speak_text(self, text: str) -> bool:
        if not text or not self.voice_enabled or not self._tts_available:
            return False

        # Trim long responses for speech
        speak_text = text[:400] + ("..." if len(text) > 400 else "")

        try:
            import pyttsx3
            # Fresh engine every call — avoids 'run loop already started'
            engine = pyttsx3.init()
            engine.setProperty('rate', 165)
            engine.setProperty('volume', 1.0)
            engine.say(speak_text)
            engine.runAndWait()
            engine.stop()
            return True
        except Exception as e:
            logger.error(f"TTS error: {e}")
            return False

    def output_response(self, text: str, use_voice: Optional[bool] = None) -> str:
        if not text:
            text = ""
        displayed = self.display_text(text)
        should_speak = use_voice if use_voice is not None else self.voice_enabled
        if should_speak:
            self.speak_text(text)
        return displayed

    def set_voice_enabled(self, enabled: bool) -> None:
        self.voice_enabled = enabled
        if enabled and not self._tts_available:
            self._tts_available = self._test_tts()
        logger.info(f"Voice output {'enabled' if enabled else 'disabled'}")

    def get_last_displayed_text(self) -> Optional[str]:
        return self.last_displayed_text
