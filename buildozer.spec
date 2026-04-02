[app]
title = 音乐抓取
package.name = musicgrabber
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

requirements = python3,kivy,yt-dlp,pydub,mutagen,requests,beautifulsoup4

orientation = portrait

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# 添加应用图标（如果有 icon.png 文件）
# icon.filename = icon.png

buildozer.spec.log_level = 2
