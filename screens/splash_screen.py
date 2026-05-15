"""
=====================================
  Splash Screen
  First screen user sees
  Premium animated intro
=====================================
"""

from kivy.uix.screen import Screen
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, ColorProperty
from kivy.graphics import Color, RoundedRectangle, Line
import math


class SplashScreen(Screen):
    """
    Premium splash screen with animations
    Shows logo, app name, and creator credit
    Transitions to loading screen after ~3.5 seconds
    """

    logo_scale = NumericProperty(0.1)
    title_opacity = NumericProperty(0)
    subtitle_opacity = NumericProperty(0)
    glow_alpha = NumericProperty(0)
    ring_angle = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Start animation after widget is fully loaded
        Clock.schedule_once(self._start_animations, 0.3)

    def _start_animations(self, dt):
        """Kick off all entrance animations"""

        # 1. Logo scales in with bounce effect
        logo_anim = (
            Animation(logo_scale=1.15, duration=0.5, t='out_back') +
            Animation(logo_scale=1.0, duration=0.2, t='out_elastic')
        )

        # 2. Glow pulse animation (infinite)
        glow_anim = (
            Animation(glow_alpha=0.8, duration=0.8, t='in_out_sine') +
            Animation(glow_alpha=0.2, duration=0.8, t='in_out_sine')
        )
        glow_anim.repeat = True

        # 3. Title fades in
        title_anim = Animation(title_opacity=0, duration=0.3) + \
                     Animation(title_opacity=1, duration=0.6, t='out_quad')

        # 4. Subtitle fades in with delay
        subtitle_anim = Animation(subtitle_opacity=0, duration=0.8) + \
                        Animation(subtitle_opacity=1, duration=0.5, t='out_quad')

        # 5. Spinning ring animation
        ring_anim = Animation(ring_angle=360, duration=2.0, t='linear')
        ring_anim.repeat = True

        # Start all animations
        logo_anim.start(self)
        glow_anim.start(self)
        ring_anim.start(self)

        # Staggered text animations
        Clock.schedule_once(lambda dt: title_anim.start(self), 0.4)
        Clock.schedule_once(lambda dt: subtitle_anim.start(self), 0.8)

        # Transition to loading screen after 3.5 seconds
        Clock.schedule_once(self._go_to_loading, 3.5)

    def _go_to_loading(self, dt):
        """Smooth transition to loading screen"""
        # Fade out animation before switching
        fade_out = Animation(opacity=0, duration=0.4, t='in_quad')
        fade_out.bind(on_complete=self._switch_screen)
        fade_out.start(self)

    def _switch_screen(self, anim, widget):
        """Switch to loading screen"""
        self.manager.current = 'loading'
        # Reset opacity for potential re-entry
        self.opacity = 1
