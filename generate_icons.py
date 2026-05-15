"""
=====================================
  Icon Generator
  Generates all Android icon sizes
  from your logo.png
=====================================

Usage: python generate_icons.py
"""

import os
import sys

try:
    from PIL import Image
except ImportError:
    print("Install Pillow first: pip install Pillow")
    sys.exit(1)


def generate_android_icons(source_path='assets/images/logo.png'):
    """Generate all required Android icon sizes"""

    if not os.path.exists(source_path):
        print(f"Error: Logo not found at {source_path}")
        print("Please add your logo file first!")
        return

    logo = Image.open(source_path).convert('RGBA')

    # Android icon sizes
    sizes = {
        'mipmap-ldpi':    36,
        'mipmap-mdpi':    48,
        'mipmap-hdpi':    72,
        'mipmap-xhdpi':   96,
        'mipmap-xxhdpi':  144,
        'mipmap-xxxhdpi': 192,
        'playstore':      512,  # Play Store icon
    }

    output_dir = 'android_icons'

    for folder, size in sizes.items():
        dir_path = os.path.join(output_dir, folder)
        os.makedirs(dir_path, exist_ok=True)

        resized = logo.resize((size, size), Image.LANCZOS)

        if folder == 'playstore':
            out_path = os.path.join(dir_path, 'ic_launcher_playstore.png')
        else:
            out_path = os.path.join(dir_path, 'ic_launcher.png')

        resized.save(out_path, 'PNG')
        print(f"✅ {folder}: {size}x{size} → {out_path}")

    # Also create a 512x512 for general use
    splash = logo.resize((512, 512), Image.LANCZOS)

    # Create splash screen (1080x1920 with centered logo)
    splash_img = Image.new('RGBA', (1080, 1920), (8, 4, 15, 255))
    logo_size = 300
    logo_resized = logo.resize((logo_size, logo_size), Image.LANCZOS)
    x = (1080 - logo_size) // 2
    y = (1920 - logo_size) // 2 - 100
    splash_img.paste(logo_resized, (x, y), logo_resized)

    splash_path = 'assets/images/splash.png'
    splash_img.save(splash_path, 'PNG')
    print(f"\n✅ Splash screen: {splash_path}")

    print(f"\n🎉 All icons generated in: {output_dir}/")
    print("Copy the mipmap folders to your Android project's res/ directory")


if __name__ == '__main__':
    print("🎨 Android Icon Generator")
    print("=" * 35)
    generate_android_icons()
