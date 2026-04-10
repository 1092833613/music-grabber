[app]
title = 音乐抓取
package.name = musicgrabber
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,ttf
version = 3.0.1

# 中文稳定版 v3.0.1 - 内置字体修复乱码
requirements = python3,kivy==2.3.0,pyjnius,requests,beautifulsoup4

orientation = portrait
android.api = 32
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# 添加中文字体文件到 APK
android.add_assets = fonts/:./fonts/

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.accept_sdk_license = True
buildozer.spec.log_level = 2
