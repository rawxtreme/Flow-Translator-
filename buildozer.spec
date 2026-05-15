[app]

title = Flow Translator
package.name = flowtranslator
package.domain = com.aaditya

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json

version = 1.0

requirements = python3==3.9.16,kivy==2.1.0,requests

orientation = portrait

fullscreen = 0

android.permissions = INTERNET,RECORD_AUDIO,VIBRATE

android.api = 31
android.minapi = 21
android.ndk = 25b

android.accept_sdk_license = True

presplash.filename = assets/images/logo.png
icon.filename = assets/images/logo.png

splash_color = #101820

android.archs = arm64-v8a, armeabi-v7a

android.allow_backup = True

android.enable_androidx = True

log_level = 2

warn_on_root = 1

window.softinput_mode = resize

[buildozer]

log_level = 2

warn_on_root = 1
