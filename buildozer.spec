[app]
title = 音乐抓取
package.name = musicgrabber
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# Android 14 兼容配置
requirements = python3==3.8.10,kivy==2.2.0,pyjnius==1.5.0,pysdl2==0.9.14

# 简化依赖，移除可能导致问题的
# yt-dlp, pydub, mutagen 在运行时加载

orientation = portrait

# Android 14 权限配置
android.api = 34
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# 权限（最小化）
android.permissions = INTERNET,READ_MEDIA_IMAGES,READ_MEDIA_AUDIO

# 禁用自动权限请求
android.accept_sdk_license = True

# 日志
buildozer.spec.log_level = 2
