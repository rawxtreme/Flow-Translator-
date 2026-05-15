"""
=====================================
  History Screen
  Shows past translations
=====================================
"""

from kivy.uix.screen import Screen
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import ListProperty, StringProperty, NumericProperty

from utils.database import db


class HistoryScreen(Screen):
    """
    Translation history screen
    Shows all past translations with delete option
    """

    history_data = ListProperty([])
    empty_opacity = NumericProperty(0)
    list_opacity = NumericProperty(0)

    def on_enter(self):
        """Load history when screen opens"""
        self._load_history()

    def _load_history(self):
        """Load translation history from database"""
        self.history_data = db.get_history(limit=50)

        if self.history_data:
            self.empty_opacity = 0
            Animation(list_opacity=1, duration=0.4, t='out_quad').start(self)
        else:
            self.list_opacity = 0
            Animation(empty_opacity=1, duration=0.4, t='out_quad').start(self)

    def delete_item(self, record_id):
        """Delete a history item"""
        db.delete_history_item(record_id)
        self._load_history()

    def toggle_favorite(self, record_id):
        """Toggle favorite for a history item"""
        db.toggle_favorite(record_id)
        self._load_history()

    def clear_all_history(self):
        """Clear all non-favorite history"""
        db.clear_history()
        self._load_history()

    def go_back(self):
        """Go back to home"""
        self.manager.current = 'home'

    def use_translation(self, source_text, translated_text, source_lang, target_lang):
        """Load a history item into the home screen"""
        home = self.manager.get_screen('home')
        try:
            source_input = home.ids.get('source_input')
            if source_input:
                source_input.text = source_text
        except:
            pass
        home.output_text = translated_text
        home.has_output = True
        home.source_lang = source_lang
        home.target_lang = target_lang
        home.source_lang_name = home.LANGUAGES.get(source_lang, source_lang)
        home.target_lang_name = home.LANGUAGES.get(target_lang, target_lang)
        self.manager.current = 'home'
