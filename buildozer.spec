[app]

title = Flow Translator
package.name = flowtranslator
package.domain = com.aaditya

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json

version = 1.0

requirements = python3,kivy,requests

orientation = portrait

fullscreen = 0

android.permissions = INTERNET,RECORD_AUDIO,VIBRATE

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

android.accept_sdk_license = True

presplash.filename = assets/1778821152699.png
icon.filename = assets/1778821152699.png

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
