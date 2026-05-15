"""
=====================================
  Theme & Color Constants
  Central place for all colors/styles
=====================================
"""

# Dark Mode Colors
DARK_THEME = {
    'bg_primary': (0.04, 0.04, 0.10, 1),         # Deep dark blue-black
    'bg_secondary': (0.08, 0.08, 0.18, 1),        # Slightly lighter
    'bg_card': (0.10, 0.10, 0.22, 1),             # Card background
    'glass_bg': (0.12, 0.12, 0.25, 0.7),          # Glassmorphism
    'accent_primary': (0.29, 0.56, 1.0, 1),       # Electric blue
    'accent_secondary': (0.52, 0.24, 1.0, 1),     # Purple
    'accent_pink': (1.0, 0.27, 0.60, 1),          # Neon pink
    'accent_cyan': (0.0, 0.85, 1.0, 1),           # Cyan
    'text_primary': (0.95, 0.95, 1.0, 1),         # Near white
    'text_secondary': (0.65, 0.65, 0.80, 1),      # Muted
    'text_hint': (0.40, 0.40, 0.55, 1),           # Placeholder
    'border': (0.20, 0.20, 0.40, 0.5),            # Border with transparency
    'success': (0.20, 0.90, 0.50, 1),             # Green
    'error': (1.0, 0.30, 0.30, 1),               # Red
    'gradient_start': (0.04, 0.04, 0.12, 1),
    'gradient_end': (0.10, 0.04, 0.20, 1),
}

# Light Mode Colors
LIGHT_THEME = {
    'bg_primary': (0.96, 0.96, 1.0, 1),           # Light lavender white
    'bg_secondary': (0.90, 0.90, 0.98, 1),
    'bg_card': (1.0, 1.0, 1.0, 1),
    'glass_bg': (1.0, 1.0, 1.0, 0.7),
    'accent_primary': (0.20, 0.45, 0.95, 1),
    'accent_secondary': (0.45, 0.15, 0.90, 1),
    'accent_pink': (0.90, 0.15, 0.50, 1),
    'accent_cyan': (0.0, 0.65, 0.90, 1),
    'text_primary': (0.05, 0.05, 0.15, 1),
    'text_secondary': (0.30, 0.30, 0.50, 1),
    'text_hint': (0.60, 0.60, 0.70, 1),
    'border': (0.80, 0.80, 0.90, 0.8),
    'success': (0.10, 0.70, 0.35, 1),
    'error': (0.85, 0.15, 0.15, 1),
    'gradient_start': (0.88, 0.88, 0.98, 1),
    'gradient_end': (0.94, 0.88, 1.0, 1),
}

# Currently active theme (can be switched)
current_theme = 'dark'

def get_theme():
    """Get current theme colors"""
    if current_theme == 'dark':
        return DARK_THEME
    return LIGHT_THEME

def set_theme(theme_name):
    """Set current theme"""
    global current_theme
    current_theme = theme_name

# Font sizes
FONTS = {
    'xs': '11sp',
    'sm': '13sp',
    'md': '15sp',
    'lg': '18sp',
    'xl': '22sp',
    'xxl': '28sp',
    'xxxl': '36sp',
    'huge': '48sp',
}

# Spacing
SPACING = {
    'xs': '4dp',
    'sm': '8dp',
    'md': '16dp',
    'lg': '24dp',
    'xl': '32dp',
    'xxl': '48dp',
}

# Animation durations (seconds)
ANIM = {
    'fast': 0.15,
    'normal': 0.3,
    'slow': 0.5,
    'splash': 3.5,
}
