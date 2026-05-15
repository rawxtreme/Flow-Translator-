"""
=====================================
  Setup Script
  Run this ONCE to create directories
  and generate placeholder assets
=====================================
"""

import os
import sys


def create_directories():
    """Create all required directories"""
    dirs = [
        'assets/images',
        'assets/fonts',
        'assets/sounds',
        'screens',
        'utils',
        'kv',
        'bin',
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"✅ Created: {d}/")


def generate_placeholder_logo():
    """Generate a placeholder logo if logo.png doesn't exist"""
    logo_path = 'assets/images/logo.png'

    if os.path.exists(logo_path):
        print(f"✅ Logo already exists: {logo_path}")
        return

    try:
        from PIL import Image, ImageDraw, ImageFont
        import math

        # Create 512x512 image
        size = 512
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Background circle (dark blue)
        draw.ellipse([10, 10, size - 10, size - 10], fill=(20, 30, 80, 255))

        # Gradient-like ring
        for i in range(8):
            alpha = int(200 * (1 - i / 8))
            draw.arc(
                [20 + i * 2, 20 + i * 2, size - 20 - i * 2, size - 20 - i * 2],
                start=0, end=360,
                fill=(74, 144, 255, alpha),
                width=3
            )

        # Translation arrows (stylized)
        center = size // 2
        # Left arrow (English)
        draw.rectangle([140, center - 20, center - 20, center + 20], fill=(74, 144, 255, 255))
        draw.polygon([
            (center - 20, center - 40),
            (center + 20, center),
            (center - 20, center + 40)
        ], fill=(74, 144, 255, 255))

        # Right arrow (Hindi)
        draw.rectangle([center + 20, center - 20, size - 140, center + 20], fill=(134, 61, 255, 255))
        draw.polygon([
            (size - 140, center - 40),
            (size - 100, center),
            (size - 140, center + 40)
        ], fill=(134, 61, 255, 255))

        # Text "T" in center
        try:
            font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 80)
        except:
            font = ImageFont.load_default()

        draw.text((center - 25, center - 50), 'T', font=font, fill=(255, 255, 255, 255))

        img.save(logo_path, 'PNG')
        print(f"✅ Generated placeholder logo: {logo_path}")
        print("   ⚠️  Replace with your actual logo (1778821152699.png)!")

    except ImportError:
        print("⚠️  Pillow not installed. Install it: pip install Pillow")
        print(f"   Manually place your logo at: {logo_path}")


def check_requirements():
    """Check if required packages are installed"""
    packages = {
        'kivy': 'kivy',
        'deep_translator': 'deep-translator',
        'PIL': 'Pillow',
    }

    print("\n📦 Checking dependencies...")
    missing = []

    for module, package in packages.items():
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - MISSING")
            missing.append(package)

    if missing:
        print(f"\n⚠️  Install missing packages:")
        print(f"  pip install {' '.join(missing)}")
    else:
        print("\n✅ All dependencies installed!")


if __name__ == '__main__':
    print("🚀 Translation App - Setup Script")
    print("=" * 40)

    create_directories()
    generate_placeholder_logo()
    check_requirements()

    print("\n" + "=" * 40)
    print("✅ Setup complete!")
    print("\nNext steps:")
    print("1. Add your logo to: assets/images/logo.png")
    print("2. Run: python main.py")
    print("3. For APK: buildozer android debug")
    print("\nMade by Aaditya Shukla 🎉")
