"""
=====================================
  Home Screen - Main Translation UI
  The heart of the app
=====================================
"""

from kivy.uix.screen import Screen
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import (
    NumericProperty, StringProperty, BooleanProperty,
    ColorProperty, ListProperty
)
from kivy.utils import platform
import threading

from utils.translator import translation_engine, detect_language, check_internet
from utils.database import db
import utils.theme as theme_module


class HomeScreen(Screen):
    """
    Main translation screen
    All primary features live here
    """

    # UI State Properties
    is_dark_mode = BooleanProperty(True)
    is_translating = BooleanProperty(False)
    source_lang = StringProperty('en')
    target_lang = StringProperty('hi')
    source_lang_name = StringProperty('English')
    target_lang_name = StringProperty('Hindi')
    output_text = StringProperty('')
    status_message = StringProperty('')
    status_visible = BooleanProperty(False)
    translate_btn_scale = NumericProperty(1.0)
    swap_rotation = NumericProperty(0)
    has_output = BooleanProperty(False)
    is_favorite = BooleanProperty(False)
    current_record_id = NumericProperty(0)
    card_opacity = NumericProperty(0)

    # Theme colors
    bg_color = ListProperty([0.04, 0.04, 0.10, 1])
    card_color = ListProperty([0.10, 0.10, 0.22, 1])
    text_color = ListProperty([0.95, 0.95, 1.0, 1])
    accent_color = ListProperty([0.29, 0.56, 1.0, 1])
    hint_color = ListProperty([0.40, 0.40, 0.55, 1])
    border_color = ListProperty([0.20, 0.20, 0.40, 0.5])

    # Supported languages
    LANGUAGES = {
        'en': 'English',
        'hi': 'Hindi',
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._voice_thread = None
        self._tts_engine = None
        self._last_source_text = ''

    def on_enter(self):
        """Called every time screen becomes active"""
        self._apply_theme()

    def _apply_theme(self):
        """Apply current theme colors to UI"""
        t = theme_module.get_theme()
        self.bg_color = list(t['bg_primary'])
        self.card_color = list(t['bg_card'])
        self.text_color = list(t['text_primary'])
        self.accent_color = list(t['accent_primary'])
        self.hint_color = list(t['text_hint'])
        self.border_color = list(t['border'])
        self.is_dark_mode = (theme_module.current_theme == 'dark')

    def toggle_theme(self):
        """Switch between dark and light mode"""
        new_theme = 'light' if theme_module.current_theme == 'dark' else 'dark'
        theme_module.set_theme(new_theme)
        self._apply_theme()
        self._show_status(f"{'Dark' if new_theme == 'dark' else 'Light'} mode activated ✨", 'success')

    def swap_languages(self):
        """Swap source and target languages with animation"""
        # Animate the swap button
        anim = (
            Animation(swap_rotation=180, duration=0.3, t='out_back') +
            Animation(swap_rotation=0, duration=0.01)
        )
        anim.start(self)

        # Swap language codes and names
        self.source_lang, self.target_lang = self.target_lang, self.source_lang
        self.source_lang_name = self.LANGUAGES.get(self.source_lang, self.source_lang)
        self.target_lang_name = self.LANGUAGES.get(self.target_lang, self.target_lang)

        # Also swap the text if there's output
        try:
            src_input = self.ids.get('source_input')
            if src_input and self.output_text:
                current_source = src_input.text
                src_input.text = self.output_text
                self.output_text = current_source
        except Exception as e:
            print(f"Swap text error: {e}")

    def translate_text(self):
        """Main translation function - called when Translate button pressed"""
        try:
            source_input = self.ids.get('source_input')
            if not source_input:
                return

            text = source_input.text.strip()
        except Exception:
            return

        if not text:
            self._show_status("Please enter text to translate ✍️", 'error')
            self._shake_input()
            return

        # Check internet
        if not check_internet():
            self._show_status("No internet connection 📡\nCheck your network and try again", 'error')
            return

        # Start translation
        self.is_translating = True
        self.has_output = False
        self.output_text = ''
        self._animate_translate_button()

        # Determine languages
        src = self.source_lang
        tgt = self.target_lang

        # Auto-detect if needed
        if src == 'auto':
            detected = detect_language(text)
            src = detected
            tgt = 'hi' if detected == 'en' else 'en'

        # Translate asynchronously
        translation_engine.translate(
            text=text,
            source_lang=src,
            target_lang=tgt,
            callback=self._on_translation_complete
        )

    def _on_translation_complete(self, result, error):
        """Called from background thread when translation is done"""
        # Must update UI on main thread
        Clock.schedule_once(
            lambda dt: self._update_ui_with_result(result, error), 0
        )

    def _update_ui_with_result(self, result, error):
        """Update UI with translation result (runs on main thread)"""
        self.is_translating = False

        if error:
            if error == 'no_internet':
                self._show_status("No internet! Connect and try again 📡", 'error')
            elif error == 'library_missing':
                self._show_status("Translation library not installed", 'error')
            else:
                self._show_status(f"Translation failed. Try again! 🔄", 'error')
            return

        if result:
            self.output_text = result
            self.has_output = True
            self.is_favorite = False

            # Animate result card appearing
            self.card_opacity = 0
            Animation(card_opacity=1, duration=0.4, t='out_quad').start(self)

            # Save to history
            try:
                source_input = self.ids.get('source_input')
                if source_input:
                    record_id = db.add_translation(
                        source_text=source_input.text.strip(),
                        translated_text=result,
                        source_lang=self.source_lang,
                        target_lang=self.target_lang
                    )
                    if record_id:
                        self.current_record_id = record_id
            except Exception as e:
                print(f"Save history error: {e}")

            self._show_status("Translation complete! ✅", 'success')
        else:
            self._show_status("Empty result received. Try again!", 'error')

    def _animate_translate_button(self):
        """Pulse animation on translate button"""
        anim = (
            Animation(translate_btn_scale=0.92, duration=0.1, t='out_quad') +
            Animation(translate_btn_scale=1.0, duration=0.15, t='out_elastic')
        )
        anim.start(self)

    def _shake_input(self):
        """Shake animation for empty input feedback"""
        try:
            source_input = self.ids.get('source_input')
            if source_input:
                original_x = source_input.x
                shake = (
                    Animation(x=original_x + 8, duration=0.05) +
                    Animation(x=original_x - 8, duration=0.05) +
                    Animation(x=original_x + 5, duration=0.05) +
                    Animation(x=original_x - 5, duration=0.05) +
                    Animation(x=original_x, duration=0.05)
                )
                shake.start(source_input)
        except:
            pass

    def copy_translation(self):
        """Copy translated text to clipboard"""
        if not self.output_text:
            self._show_status("Nothing to copy!", 'error')
            return

        try:
            from kivy.core.clipboard import Clipboard
            Clipboard.copy(self.output_text)
            self._show_status("Copied to clipboard! 📋", 'success')
        except Exception as e:
            self._show_status("Copy failed - try again", 'error')

    def clear_all(self):
        """Clear both input and output"""
        try:
            source_input = self.ids.get('source_input')
            if source_input:
                source_input.text = ''
        except:
            pass

        # Animate card out
        if self.has_output:
            anim = Animation(card_opacity=0, duration=0.2, t='in_quad')
            anim.bind(on_complete=lambda *args: self._reset_output())
            anim.start(self)
        else:
            self._reset_output()

    def _reset_output(self, *args):
        """Reset output state"""
        self.output_text = ''
        self.has_output = False
        self.status_visible = False
        self.is_favorite = False
        self.current_record_id = 0

    def toggle_favorite(self):
        """Toggle favorite status of current translation"""
        if not self.has_output or not self.current_record_id:
            self._show_status("Translate something first! 💡", 'error')
            return

        new_status = db.toggle_favorite(self.current_record_id)
        self.is_favorite = new_status

        if new_status:
            self._show_status("Added to favorites! ⭐", 'success')
        else:
            self._show_status("Removed from favorites", 'success')

    def start_voice_input(self):
        """Start voice recognition"""
        if platform == 'android':
            self._android_voice_input()
        else:
            self._show_status("Voice input works on Android only 🎙️", 'error')

    def _android_voice_input(self):
        """Android-specific voice input using SpeechRecognition"""
        try:
            from android import activity
            from jnius import autoclass

            Intent = autoclass('android.content.Intent')
            RecognizerIntent = autoclass('android.speech.RecognizerIntent')

            intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
            intent.putExtra(
                RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                RecognizerIntent.LANGUAGE_MODEL_FREE_FORM
            )
            intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, 'en-US')
            intent.putExtra(RecognizerIntent.EXTRA_PROMPT, 'Speak now...')

            activity.startActivityForResult(intent, 1)
            self._show_status("Listening... 🎙️", 'success')

        except Exception as e:
            self._show_status("Voice input not available on this device", 'error')

    def speak_translation(self):
        """Text-to-speech for the translated text"""
        if not self.output_text:
            self._show_status("Nothing to speak! 🔇", 'error')
            return

        thread = threading.Thread(
            target=self._speak_worker,
            args=(self.output_text, self.target_lang),
            daemon=True
        )
        thread.start()
        self._show_status("Speaking... 🔊", 'success')

    def _speak_worker(self, text, lang):
        """Background TTS worker"""
        try:
            if platform == 'android':
                from jnius import autoclass
                TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
                Locale = autoclass('java.util.Locale')

                # Android TTS (simplified - full impl needs activity context)
                print(f"TTS: {text} in {lang}")
            else:
                # Desktop TTS using pyttsx3
                try:
                    import pyttsx3
                    engine = pyttsx3.init()
                    engine.say(text)
                    engine.runAndWait()
                except ImportError:
                    # Try gtts as fallback
                    try:
                        from gtts import gTTS
                        import tempfile
                        import os

                        tts = gTTS(text=text, lang=lang, slow=False)
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
                            tts.save(f.name)
                            # Play the audio
                            from kivy.core.audio import SoundLoader
                            sound = SoundLoader.load(f.name)
                            if sound:
                                sound.play()
                    except Exception as e:
                        print(f"TTS error: {e}")
        except Exception as e:
            print(f"Speak error: {e}")

    def _show_status(self, message, status_type='info'):
        """Show status message with auto-hide"""
        self.status_message = message
        self.status_visible = True

        # Auto-hide after 3 seconds
        Clock.unschedule(self._hide_status)
        Clock.schedule_once(self._hide_status, 3.0)

    def _hide_status(self, dt=None):
        """Hide status message"""
        self.status_visible = False

    def go_to_history(self):
        """Navigate to history screen"""
        self.manager.current = 'history'

    def go_to_favorites(self):
        """Navigate to favorites screen"""
        self.manager.current = 'favorites'
