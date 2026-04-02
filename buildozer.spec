[app]
title = 音乐抓取
package.name = musicgrabber
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 2.0.1

# 逐步恢复功能测试
requirements = python3,kivy==2.3.0,pyjnius

orientation = portrait

android.api = 32
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.accept_sdk_license = True

buildozer.spec.log_level = 2
