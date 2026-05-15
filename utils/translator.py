"""
=====================================
  Simple Translation Engine
  Stable testing version for APK build
=====================================
"""

import threading
import socket


def check_internet(host="8.8.8.8", port=53, timeout=3):
    """Check internet connection"""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False


def detect_language(text):
    """Simple Hindi/English detection"""
    if not text or not text.strip():
        return 'en'

    devanagari_count = sum(1 for c in text if '\u0900' <= c <= '\u097F')
    total_letters = sum(1 for c in text if c.isalpha())

    if total_letters == 0:
        return 'en'

    if devanagari_count / total_letters > 0.3:
        return 'hi'

    return 'en'


class TranslationEngine:
    """
    Stable test translation engine
    """

    def __init__(self):
        self.is_available = True

    def translate(self, text, source_lang='auto', target_lang='hi', callback=None):
        """Run translation in background thread"""

        thread = threading.Thread(
            target=self._translate_worker,
            args=(text, callback),
            daemon=True
        )
        thread.start()

    def _translate_worker(self, text, callback):
        """Fake translation worker for stable APK testing"""

        try:
            if not text.strip():
                if callback:
                    callback('', None)
                return

            # Simple stable test translation
            result = f"Translated: {text}"

            if callback:
                callback(result, None)

        except Exception as e:
            if callback:
                callback(None, str(e))

    def translate_sync(self, text, source_lang='auto', target_lang='hi'):
        """Simple sync translation"""

        try:
            result = f"Translated: {text}"
            return result, None
        except Exception as e:
            return None, str(e)


# Singleton instance
translation_engine = TranslationEngine()
