"""
=====================================
  Loading Screen
  Shows animated progress bar
  Prepares app while looking premium
=====================================
"""

from kivy.uix.screen import Screen
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, ColorProperty
import threading


class LoadingScreen(Screen):
    """
    Loading screen that simulates initialization
    Shows progress bar and loading messages
    """

    progress = NumericProperty(0)
    loading_text = StringProperty("Initializing...")
    content_opacity = NumericProperty(0)
    bar_width = NumericProperty(0)
    dots_text = StringProperty("")

    # Loading steps with messages and durations
    LOADING_STEPS = [
        (15, "Loading components...", 0.3),
        (35, "Setting up translation engine...", 0.5),
        (55, "Connecting services...", 0.4),
        (70, "Loading fonts & assets...", 0.3),
        (85, "Preparing UI...", 0.3),
        (95, "Almost ready...", 0.3),
        (100, "Welcome!", 0.2),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._dot_counter = 0
        self._dot_event = None

    def on_enter(self):
        """Called when screen becomes active"""
        # Reset state
        self.progress = 0
        self.content_opacity = 0
        self.bar_width = 0

        # Fade in content
        Clock.schedule_once(self._start_loading, 0.1)

    def _start_loading(self, dt):
        """Start the loading sequence"""
        # Fade in
        Animation(content_opacity=1, duration=0.5, t='out_quad').start(self)

        # Start dot animation
        self._dot_event = Clock.schedule_interval(self._animate_dots, 0.4)

        # Start loading steps
        self._run_loading_steps()

    def _animate_dots(self, dt):
        """Animate loading dots"""
        self._dot_counter = (self._dot_counter + 1) % 4
        self.dots_text = '.' * self._dot_counter

    def _run_loading_steps(self):
        """Execute loading steps sequentially"""
        delay = 0
        for i, (target_progress, message, duration) in enumerate(self.LOADING_STEPS):
            Clock.schedule_once(
                lambda dt, p=target_progress, m=message, d=duration:
                    self._update_progress(p, m, d),
                delay
            )
            delay += duration + 0.1

        # After all steps, go to home
        Clock.schedule_once(self._finish_loading, delay + 0.3)

    def _update_progress(self, target, message, duration):
        """Update progress bar and message"""
        self.loading_text = message

        # Animate progress bar
        anim = Animation(progress=target, duration=duration, t='out_quad')
        anim.start(self)

        # Also animate bar width property for visual bar
        # (handled in KV using progress property)

    def _finish_loading(self, dt):
        """Complete loading and go to home screen"""
        # Stop dot animation
        if self._dot_event:
            self._dot_event.cancel()
            self._dot_event = None

        self.dots_text = ""
        self.loading_text = "Let's Go! 🚀"

        # Fade out and switch
        Clock.schedule_once(self._go_to_home, 0.6)

    def _go_to_home(self, dt):
        """Transition to home screen"""
        fade_out = Animation(content_opacity=0, duration=0.4, t='in_quad')
        fade_out.bind(on_complete=self._switch_to_home)
        fade_out.start(self)

    def _switch_to_home(self, anim, widget):
        """Switch to main home screen"""
        self.manager.current = 'home'
        # Reset for potential re-use
        self.content_opacity = 1
        self.progress = 0
