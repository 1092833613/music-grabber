[app]
title = 音乐抓取
package.name = musicgrabber
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,ttf
version = 2.1.1

# 修复中文乱码（注册中文字体）
requirements = python3,kivy==2.3.0

orientation = portrait
android.api = 32
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.accept_sdk_license = True
buildozer.spec.log_level = 2
