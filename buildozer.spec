[app]
title = 音乐抓取
package.name = musicgrabber
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 2.0.0

# Android 14 兼容配置（已验证）
requirements = python3,kivy==2.3.0,pyjnius,requests,beautifulsoup4

orientation = portrait

# Android 12（在 Android 14 上兼容最好）
android.api = 32
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# 权限
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.accept_sdk_license = True

# 日志
buildozer.spec.log_level = 2
