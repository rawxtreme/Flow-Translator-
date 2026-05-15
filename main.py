"""
=====================================
  Translation App - Stable Minimal Build
=====================================
"""

import os
import sys

# Fix encoding for Hindi text
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer,
        encoding='utf-8'
    )

os.environ['KIVY_AUDIO'] = (
    'android'
    if os.path.exists('/system')
    else 'sdl2'
)

from kivy.config import Config

# Configure before importing kivy widgets
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
from kivy.uix.screenmanager import (
    ScreenManager,
    FadeTransition
)
from kivy.core.window import Window
from kivy.utils import platform

# Desktop testing window
if platform != 'android':
    Window.size = (400, 720)
    Window.clearcolor = (0.05, 0.05, 0.1, 1)

# Import only stable screens
from screens.splash_screen import SplashScreen
from screens.loading_screen import LoadingScreen
from screens.home_screen import HomeScreen

# Load only required KV files
KV_FILES = [
    'kv/splash.kv',
    'kv/loading.kv',
    'kv/home.kv',
    'kv/widgets.kv',
]

for kv_file in KV_FILES:

    if os.path.exists(kv_file):
        Builder.load_file(kv_file)

    else:
        print(f"Missing KV file: {kv_file}")


class TranslationApp(App):

    def build(self):

        self.title = "Flow Translator"
        self.icon = "assets/images/logo.png"

        self.sm = ScreenManager(
            transition=FadeTransition(duration=0.4)
        )

        # Add only stable screens
        self.sm.add_widget(
            SplashScreen(name='splash')
        )

        self.sm.add_widget(
            LoadingScreen(name='loading')
        )

        self.sm.add_widget(
            HomeScreen(name='home')
        )

        # Start app
        self.sm.current = 'splash'

        return self.sm

    def on_start(self):

        if platform == 'android':
            self._request_android_permissions()

    def _request_android_permissions(self):

        try:
            from android.permissions import (
                request_permissions,
                Permission
            )

            request_permissions([
                Permission.INTERNET,
                Permission.VIBRATE,
            ])

        except ImportError:
            pass

    def on_pause(self):
        return True

    def on_resume(self):
        pass


if __name__ == '__main__':
    TranslationApp().run()
