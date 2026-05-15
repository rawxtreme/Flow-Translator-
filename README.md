# 🌐 Translation App
### By Aaditya Shukla

Premium Android Translation App built with Python + Kivy
English ↔ Hindi | Voice Input | TTS | History | Favorites

---

## 📁 FOLDER STRUCTURE

```
TranslationApp/
├── main.py                    ← App entry point
├── requirements.txt           ← Python dependencies
├── buildozer.spec             ← Android build config
│
├── screens/
│   ├── __init__.py
│   ├── splash_screen.py       ← Animated splash screen
│   ├── loading_screen.py      ← Loading progress screen
│   ├── home_screen.py         ← Main translation screen
│   ├── history_screen.py      ← Translation history
│   └── favorites_screen.py    ← Starred translations
│
├── utils/
│   ├── __init__.py
│   ├── theme.py               ← Dark/Light theme colors
│   ├── translator.py          ← Translation engine
│   └── database.py            ← SQLite history/favorites
│
├── kv/
│   ├── splash.kv              ← Splash UI
│   ├── loading.kv             ← Loading UI
│   ├── home.kv                ← Main UI
│   ├── history.kv             ← History UI
│   ├── favorites.kv           ← Favorites UI
│   └── widgets.kv             ← Reusable components
│
└── assets/
    └── images/
        ├── logo.png           ← YOUR APP LOGO (add here!)
        └── splash.png         ← Splash background
```

---

## ⚡ STEP 1: ADD YOUR LOGO

Place your logo file at:
```
assets/images/logo.png
```
The app uses this file on:
- Splash screen
- Loading screen
- Top app bar
- Android launcher icon

**To generate all Android icon sizes**, run:
```bash
pip install Pillow
python -c "
from PIL import Image
import os

logo = Image.open('assets/images/logo.png').convert('RGBA')

sizes = {
    'mipmap-mdpi': 48,
    'mipmap-hdpi': 72,
    'mipmap-xhdpi': 96,
    'mipmap-xxhdpi': 144,
    'mipmap-xxxhdpi': 192,
}

for folder, size in sizes.items():
    os.makedirs(f'android_icons/{folder}', exist_ok=True)
    resized = logo.resize((size, size), Image.LANCZOS)
    resized.save(f'android_icons/{folder}/ic_launcher.png')
    print(f'Created {size}x{size} icon')

print('Done! Icons in android_icons/ folder')
"
```

---

## 🖥️ STEP 2: SETUP ON YOUR PC (Ubuntu/WSL recommended)

### Install Python dependencies:
```bash
pip install kivy==2.3.0 kivymd==1.1.1 deep-translator requests Pillow pyttsx3 gTTS
```

### Run on desktop to test:
```bash
python main.py
```

---

## 📱 STEP 3: BUILD APK FOR ANDROID

### A. Install Buildozer (Linux/WSL required):
```bash
# Install system dependencies
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool \
  pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake \
  libffi-dev libssl-dev

# Install buildozer
pip install buildozer cython

# Install Android SDK tools
buildozer android debug  # First run downloads everything (takes 20-30 min)
```

### B. Build Debug APK:
```bash
cd TranslationApp
buildozer android debug
```

APK will be at: `bin/translationapp-1.0.0-debug.apk`

### C. Build Release APK:
```bash
buildozer android release
```

---

## 📲 STEP 4: INSTALL ON ANDROID PHONE

### Method 1 - ADB (USB):
```bash
# Enable Developer Options on phone
# Enable USB Debugging
adb devices
adb install bin/translationapp-1.0.0-debug.apk
```

### Method 2 - Transfer file:
1. Copy APK to phone via USB/Bluetooth/Google Drive
2. Open file manager on phone
3. Tap the APK file
4. Allow "Install from unknown sources"
5. Tap Install

---

## 🔐 STEP 5: GENERATE SIGNED APK (For Play Store)

### A. Create a keystore:
```bash
keytool -genkey -v -keystore my-release-key.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias translation-app
```
(Remember the password you set!)

### B. Sign the APK:
```bash
# Build release first
buildozer android release

# Sign it
jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 \
  -keystore my-release-key.jks \
  bin/translationapp-1.0.0-release-unsigned.apk translation-app

# Align it (required for Play Store)
zipalign -v 4 \
  bin/translationapp-1.0.0-release-unsigned.apk \
  bin/translationapp-1.0.0-release.apk
```

### C. Verify signature:
```bash
jarsigner -verify -verbose -certs bin/translationapp-1.0.0-release.apk
```

---

## 🐙 STEP 6: PUBLISH ON GITHUB

```bash
# Initialize git repo
cd TranslationApp
git init
git add .
git commit -m "Initial commit - Translation App by Aaditya Shukla"

# Create repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/TranslationApp.git
git branch -M main
git push -u origin main
```

### Add .gitignore:
```
__pycache__/
*.pyc
.buildozer/
bin/
*.db
*.jks
*.keystore
.env
```

---

## 🎨 STEP 7: HOW TO CHANGE APP NAME / LOGO LATER

### Change App Name:
1. Open `buildozer.spec`
2. Change: `title = Translation App` → `title = YourNewName`
3. Rebuild APK

### Change Logo:
1. Replace `assets/images/logo.png` with your new image
2. Rebuild APK
3. Regenerate Android icons (see Step 1)

### Change Package Name (for Play Store uniqueness):
1. Open `buildozer.spec`
2. Change: `package.name = translationapp` → `package.name = yourappname`
3. Change: `package.domain = com.aadityashukla` → `com.yourdomain`
4. Rebuild — WARNING: changing this unlinks from Play Store listing

---

## 🏪 STEP 8: PUBLISH ON PLAY STORE

1. Go to https://play.google.com/console
2. Create developer account ($25 one-time fee)
3. Create new app
4. Upload signed APK or AAB
5. Fill in:
   - App title
   - Description
   - Screenshots (take from phone)
   - Category: Tools
6. Set pricing (Free recommended)
7. Submit for review (usually 2-7 days)

---

## 🐛 COMMON ERRORS & FIXES

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError: deep_translator` | `pip install deep-translator` |
| `kivy not found` | `pip install kivy==2.3.0` |
| APK crashes on start | Check logcat: `adb logcat` |
| Hindi text not showing | Install Noto fonts or use system font |
| Translation fails | Check internet connection |
| Buildozer error on Windows | Use WSL2 or Ubuntu VM |

---

## 📊 APP FEATURES SUMMARY

| Feature | Status |
|---------|--------|
| English → Hindi | ✅ |
| Hindi → English | ✅ |
| Auto language detect | ✅ |
| Copy translation | ✅ |
| Clear text | ✅ |
| Voice input (Android) | ✅ |
| Text-to-speech | ✅ |
| Dark/Light mode | ✅ |
| Internet check | ✅ |
| Offline error handling | ✅ |
| Loading animation | ✅ |
| Translation history | ✅ |
| Favorites | ✅ |
| Glassmorphism UI | ✅ |
| Gradient backgrounds | ✅ |
| Animated splash screen | ✅ |

---

## 💡 TIPS

- **Best build environment**: Ubuntu 22.04 or WSL2 on Windows
- **Test before building**: Always run `python main.py` on desktop first
- **Hindi fonts**: If Hindi looks broken, add Noto Sans Devanagari font to assets
- **Performance**: Works well on devices with Android 5.0+ (API 21+)

---

Made with ❤️ by **Aaditya Shukla**
