"""
=====================================
  Home Screen - Stable APK Version
=====================================
"""

from kivy.uix.screen import Screen
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import (
    NumericProperty,
    StringProperty,
    BooleanProperty,
    ListProperty
)

from utils.translator import (
    translation_engine,
    detect_language,
    check_internet
)

from utils.database import db
import utils.theme as theme_module


class HomeScreen(Screen):

    # UI State
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

    # Theme Colors
    bg_color = ListProperty([0.04, 0.04, 0.10, 1])
    card_color = ListProperty([0.10, 0.10, 0.22, 1])
    text_color = ListProperty([0.95, 0.95, 1.0, 1])
    accent_color = ListProperty([0.29, 0.56, 1.0, 1])
    hint_color = ListProperty([0.40, 0.40, 0.55, 1])
    border_color = ListProperty([0.20, 0.20, 0.40, 0.5])

    LANGUAGES = {
        'en': 'English',
        'hi': 'Hindi',
    }

    def on_enter(self):
        self._apply_theme()

    def _apply_theme(self):
        t = theme_module.get_theme()

        self.bg_color = list(t['bg_primary'])
        self.card_color = list(t['bg_card'])
        self.text_color = list(t['text_primary'])
        self.accent_color = list(t['accent_primary'])
        self.hint_color = list(t['text_hint'])
        self.border_color = list(t['border'])

        self.is_dark_mode = (
            theme_module.current_theme == 'dark'
        )

    def toggle_theme(self):

        new_theme = (
            'light'
            if theme_module.current_theme == 'dark'
            else 'dark'
        )

        theme_module.set_theme(new_theme)
        self._apply_theme()

        self._show_status(
            f"{new_theme.capitalize()} mode activated ✨",
            'success'
        )

    def swap_languages(self):

        anim = (
            Animation(
                swap_rotation=180,
                duration=0.3,
                t='out_back'
            ) +
            Animation(
                swap_rotation=0,
                duration=0.01
            )
        )

        anim.start(self)

        self.source_lang, self.target_lang = (
            self.target_lang,
            self.source_lang
        )

        self.source_lang_name = self.LANGUAGES.get(
            self.source_lang,
            self.source_lang
        )

        self.target_lang_name = self.LANGUAGES.get(
            self.target_lang,
            self.target_lang
        )

        try:
            src_input = self.ids.get('source_input')

            if src_input and self.output_text:
                current_source = src_input.text
                src_input.text = self.output_text
                self.output_text = current_source

        except Exception as e:
            print(f"Swap error: {e}")

    def translate_text(self):

        try:
            source_input = self.ids.get('source_input')

            if not source_input:
                return

            text = source_input.text.strip()

        except Exception:
            return

        if not text:
            self._show_status(
                "Please enter text ✍️",
                'error'
            )
            self._shake_input()
            return

        if not check_internet():
            self._show_status(
                "No internet connection 📡",
                'error'
            )
            return

        self.is_translating = True
        self.has_output = False
        self.output_text = ''

        self._animate_translate_button()

        src = self.source_lang
        tgt = self.target_lang

        if src == 'auto':
            detected = detect_language(text)
            src = detected
            tgt = 'hi' if detected == 'en' else 'en'

        translation_engine.translate(
            text=text,
            source_lang=src,
            target_lang=tgt,
            callback=self._on_translation_complete
        )

    def _on_translation_complete(self, result, error):

        Clock.schedule_once(
            lambda dt: self._update_ui(result, error),
            0
        )

    def _update_ui(self, result, error):

        self.is_translating = False

        if error:
            self._show_status(
                "Translation failed 🔄",
                'error'
            )
            return

        if result:

            self.output_text = result
            self.has_output = True
            self.is_favorite = False

            self.card_opacity = 0

            Animation(
                card_opacity=1,
                duration=0.4,
                t='out_quad'
            ).start(self)

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
                print(f"DB error: {e}")

            self._show_status(
                "Translation complete ✅",
                'success'
            )

    def _animate_translate_button(self):

        anim = (
            Animation(
                translate_btn_scale=0.92,
                duration=0.1,
                t='out_quad'
            ) +
            Animation(
                translate_btn_scale=1.0,
                duration=0.15,
                t='out_elastic'
            )
        )

        anim.start(self)

    def _shake_input(self):

        try:
            source_input = self.ids.get('source_input')

            if source_input:

                original_x = source_input.x

                shake = (
                    Animation(
                        x=original_x + 8,
                        duration=0.05
                    ) +
                    Animation(
                        x=original_x - 8,
                        duration=0.05
                    ) +
                    Animation(
                        x=original_x,
                        duration=0.05
                    )
                )

                shake.start(source_input)

        except:
            pass

    def copy_translation(self):

        if not self.output_text:
            self._show_status(
                "Nothing to copy",
                'error'
            )
            return

        try:
            from kivy.core.clipboard import Clipboard

            Clipboard.copy(self.output_text)

            self._show_status(
                "Copied 📋",
                'success'
            )

        except:
            self._show_status(
                "Copy failed",
                'error'
            )

    def clear_all(self):

        try:
            source_input = self.ids.get('source_input')

            if source_input:
                source_input.text = ''

        except:
            pass

        self.output_text = ''
        self.has_output = False
        self.status_visible = False
        self.is_favorite = False
        self.current_record_id = 0

    def toggle_favorite(self):

        if not self.has_output:
            self._show_status(
                "Translate something first",
                'error'
            )
            return

        try:

            new_status = db.toggle_favorite(
                self.current_record_id
            )

            self.is_favorite = new_status

            if new_status:
                self._show_status(
                    "Added to favorites ⭐",
                    'success'
                )
            else:
                self._show_status(
                    "Removed from favorites",
                    'success'
                )

        except Exception as e:
            print(f"Favorite error: {e}")

    def _show_status(self, message, status_type='info'):

        self.status_message = message
        self.status_visible = True

        Clock.unschedule(self._hide_status)

        Clock.schedule_once(
            self._hide_status,
            3
        )

    def _hide_status(self, dt=None):

        self.status_visible = False

    def go_to_history(self):

        self.manager.current = 'history'

    def go_to_favorites(self):

        self.manager.current = 'favorites'
