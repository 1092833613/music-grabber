[app]
title = 音乐抓取
package.name = musicgrabber
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

requirements = python3,kivy==2.3.0,yt-dlp,pydub,requests,beautifulsoup4,multicolorbitmap

orientation = portrait

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,CAMERA

android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

# 添加启动配置
android.add_activities = org.kivy.android.PythonActivity
android.manifest.activity.launch_mode = standard

[buildozer]
log_level = 2
warn_on_root = 1
