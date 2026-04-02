[app]
title = Music Test
package.name = musictest
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# 使用最新 Kivy 版本（Android 14 兼容）
requirements = python3,kivy==2.3.0,pyjnius

orientation = portrait

# Android 12（更稳定）
android.api = 32
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

# 权限
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.accept_sdk_license = True

buildozer.spec.log_level = 2
