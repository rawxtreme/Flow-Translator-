"""
=====================================
  Translation Engine
  Handles translation logic, language detection,
  internet checking, and offline fallback
=====================================
"""

import threading
import socket
from functools import lru_cache


def check_internet(host="8.8.8.8", port=53, timeout=3):
    """
    Check if internet is available
    Tries to connect to Google DNS
    Returns True if connected, False otherwise
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False


def detect_language(text):
    """
    Simple language detection
    Checks if text contains Devanagari script (Hindi) or Latin (English)
    Returns 'hi' for Hindi, 'en' for English
    """
    if not text or not text.strip():
        return 'en'

    # Count Devanagari characters (Hindi Unicode range: 0900-097F)
    devanagari_count = sum(1 for c in text if '\u0900' <= c <= '\u097F')
    total_letters = sum(1 for c in text if c.isalpha())

    if total_letters == 0:
        return 'en'

    # If more than 30% characters are Devanagari, it's Hindi
    if devanagari_count / total_letters > 0.3:
        return 'hi'
    return 'en'


class TranslationEngine:
    """
    Core translation engine
    Uses deep-translator library (works offline for basic, online for full)
    Falls back gracefully when no internet
    """

    def __init__(self):
        self.is_available = False
        self._check_dependencies()

    def _check_dependencies(self):
        """Check if translation library is available"""
        try:
            from deep_translator import GoogleTranslator
            self.is_available = True
        except ImportError:
            self.is_available = False

    def translate(self, text, source_lang='auto', target_lang='hi', callback=None):
        """
        Translate text asynchronously
        
        Args:
            text: Text to translate
            source_lang: Source language code ('auto', 'en', 'hi')
            target_lang: Target language code ('en', 'hi')
            callback: Function to call with (result, error) when done
        """
        if not text or not text.strip():
            if callback:
                callback('', None)
            return

        # Run translation in background thread to avoid UI freeze
        thread = threading.Thread(
            target=self._translate_worker,
            args=(text, source_lang, target_lang, callback),
            daemon=True
        )
        thread.start()

    def _translate_worker(self, text, source_lang, target_lang, callback):
        """Background worker for translation"""
        try:
            # Check internet first
            if not check_internet():
                if callback:
                    callback(None, 'no_internet')
                return

            if not self.is_available:
                if callback:
                    callback(None, 'library_missing')
                return

            from deep_translator import GoogleTranslator

            # Handle auto-detection
            if source_lang == 'auto':
                detected = detect_language(text)
                # If detected same as target, translate to the other language
                if detected == target_lang:
                    source_lang = 'hi' if target_lang == 'hi' else 'en'
                    target_lang = detected
                else:
                    source_lang = detected

            # Perform actual translation
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            
            # Handle long text by splitting into chunks (Google has 5000 char limit)
            if len(text) > 4500:
                chunks = self._split_text(text, 4500)
                translated_chunks = []
                for chunk in chunks:
                    translated_chunk = translator.translate(chunk)
                    translated_chunks.append(translated_chunk or chunk)
                result = ' '.join(translated_chunks)
            else:
                result = translator.translate(text)

            if callback:
                callback(result or text, None)

        except Exception as e:
            error_msg = str(e)
            if 'ConnectionError' in error_msg or 'timeout' in error_msg.lower():
                if callback:
                    callback(None, 'no_internet')
            else:
                if callback:
                    callback(None, f'error: {error_msg}')

    def _split_text(self, text, max_length):
        """Split long text into chunks at sentence boundaries"""
        chunks = []
        sentences = text.replace('।', '.').split('.')
        current_chunk = ''

        for sentence in sentences:
            if len(current_chunk) + len(sentence) < max_length:
                current_chunk += sentence + '. '
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + '. '

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks if chunks else [text]

    def translate_sync(self, text, source_lang='auto', target_lang='hi'):
        """
        Synchronous translation (use only when necessary)
        Returns (result, error) tuple
        """
        if not check_internet():
            return None, 'no_internet'

        if not self.is_available:
            return None, 'library_missing'

        try:
            from deep_translator import GoogleTranslator
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            result = translator.translate(text)
            return result, None
        except Exception as e:
            return None, str(e)


# Singleton instance
translation_engine = TranslationEngine()
