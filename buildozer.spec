[app]
title = Music Test
package.name = musictest
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# 最简化依赖
requirements = python3,kivy==2.1.0

orientation = portrait

# Android 13（稳定）
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# 权限
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.accept_sdk_license = True

buildozer.spec.log_level = 2
