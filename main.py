"""
=====================================
  Translation App - by Aaditya Shukla
  Main Entry Point
=====================================
"""

import os
import sys

# Fix encoding for Hindi text on Windows/Android
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

os.environ['KIVY_AUDIO'] = 'android' if os.path.exists('/system') else 'sdl2'

from kivy.config import Config

# Must be set before any kivy imports
Config.set('graphics', 'resizable', '0')
Config.set('kivy', 'default_font', [
    'Roboto',
    'data/fonts/Roboto-Regular.ttf',
    'data/fonts/Roboto-Italic.ttf',
    'data/fonts/Roboto-Bold.ttf',
    'data/fonts/Roboto-BoldItalic.ttf',
])

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
from kivy.utils import platform

# Set window size for desktop testing (Android ignores this)
if platform != 'android':
    Window.size = (400, 720)
    Window.clearcolor = (0.05, 0.05, 0.1, 1)

# Import all screens
from screens.splash_screen import SplashScreen
from screens.loading_screen import LoadingScreen
from screens.home_screen import HomeScreen
from screens.history_screen import HistoryScreen
from screens.favorites_screen import FavoritesScreen

# Load KV files
from kivy.lang import Builder

KV_FILES = [
    'kv/splash.kv',
    'kv/loading.kv',
    'kv/home.kv',
    'kv/history.kv',
    'kv/favorites.kv',
    'kv/widgets.kv',
]

for kv_file in KV_FILES:
    if os.path.exists(kv_file):
        Builder.load_file(kv_file)


class TranslationApp(App):
    """
    Main Application Class
    Controls the entire app lifecycle
    """

    def build(self):
        """Build and return the root widget"""
        self.title = "Translation App"
        self.icon = "assets/images/logo.png"

        # Create screen manager with fade transition
        self.sm = ScreenManager(transition=FadeTransition(duration=0.4))

        # Add all screens
        self.sm.add_widget(SplashScreen(name='splash'))
        self.sm.add_widget(LoadingScreen(name='loading'))
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(HistoryScreen(name='history'))
        self.sm.add_widget(FavoritesScreen(name='favorites'))

        # Start with splash screen
        self.sm.current = 'splash'

        return self.sm

    def on_start(self):
        """Called when app starts"""
        # Request Android permissions if on Android
        if platform == 'android':
            self._request_android_permissions()

    def _request_android_permissions(self):
        """Request necessary Android permissions"""
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.INTERNET,
                Permission.RECORD_AUDIO,
                Permission.VIBRATE,
            ])
        except ImportError:
            pass  # Not on Android

    def on_pause(self):
        """Allow app to pause (important for Android)"""
        return True

    def on_resume(self):
        """Resume app from pause"""
        pass


if __name__ == '__main__':
    TranslationApp().run()
