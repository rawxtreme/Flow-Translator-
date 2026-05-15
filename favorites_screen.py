"""
=====================================
  Favorites Screen
  Shows starred/favorite translations
=====================================
"""

from kivy.uix.screen import Screen
from kivy.animation import Animation
from kivy.properties import ListProperty, NumericProperty

from utils.database import db


class FavoritesScreen(Screen):
    """
    Favorites screen
    Shows all starred translations
    """

    favorites_data = ListProperty([])
    empty_opacity = NumericProperty(0)
    list_opacity = NumericProperty(0)

    def on_enter(self):
        """Load favorites when screen opens"""
        self._load_favorites()

    def _load_favorites(self):
        """Load favorites from database"""
        self.favorites_data = db.get_favorites()

        if self.favorites_data:
            self.empty_opacity = 0
            Animation(list_opacity=1, duration=0.4, t='out_quad').start(self)
        else:
            self.list_opacity = 0
            Animation(empty_opacity=1, duration=0.4, t='out_quad').start(self)

    def remove_favorite(self, record_id):
        """Remove a translation from favorites"""
        db.toggle_favorite(record_id)
        self._load_favorites()

    def go_back(self):
        """Go back to home"""
        self.manager.current = 'home'

    def use_translation(self, source_text, translated_text, source_lang, target_lang):
        """Load into home screen"""
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
