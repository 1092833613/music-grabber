[app]
title = Music
package.name = musicgrabber
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg

# 不包含 kv 文件
version = 2.0.2

requirements = python3,kivy==2.3.0

orientation = portrait
android.api = 32
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

android.permissions = INTERNET
android.accept_sdk_license = True
buildozer.spec.log_level = 2
