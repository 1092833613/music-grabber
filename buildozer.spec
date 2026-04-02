[app]
title = 音乐抓取
package.name = musicgrabber
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# 稳定依赖（Android 13 兼容）
requirements = python3,kivy==2.1.0,pyjnius,requests,beautifulsoup4

orientation = portrait

# Android 13（稳定版本）
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# 权限（兼容 Android 13）
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.accept_sdk_license = True

# 日志
buildozer.spec.log_level = 2
