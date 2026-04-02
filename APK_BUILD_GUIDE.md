# 📱 Android APK 打包指南

**项目**: 音乐抓取 App  
**版本**: 2.0.0  
**更新时间**: 2026-04-02

---

## ⚠️ 当前环境状态

**服务器环境限制**：
- ❌ 系统依赖冲突（systemd 版本问题）
- ❌ 无法安装 Java JDK
- ❌ 无法安装完整 Android SDK

**结论**: 当前服务器环境**不适合**直接打包 APK

---

## ✅ 推荐的打包方案

### 方案 1: 本地打包（推荐）⭐

**要求**：
- Ubuntu/Linux 或 macOS
- 至少 10GB 可用空间
- 稳定的网络连接

**步骤**：

```bash
# 1. 克隆或下载项目
cd music_grabber

# 2. 安装依赖
pip install -r requirements.txt

# 3. 安装构建工具
sudo apt install -y python3-pip python3-setuptools git openjdk-11-jdk zlib1g zlib1g-dev libncurses5-dev

# 4. 初始化 buildozer
buildozer init

# 5. 打包 APK
buildozer -v android debug

# 输出位置：bin/musicgrabber-1.0.0-debug.apk
```

**预计时间**: 30-60 分钟（首次需要下载 Android SDK）

---

### 方案 2: 云端打包（最简单）🌟

使用在线 CI/CD 服务，无需本地环境：

#### A. GitHub Actions

1. 将项目上传到 GitHub
2. 创建 `.github/workflows/build.yml`
3. 使用现成的 buildozer action

**示例工作流**：
```yaml
name: Build APK
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: ArtemSBulgakov/buildozer-action@v1
      - uses: actions/upload-artifact@v2
        with:
          name: apk
          path: bin/
```

#### B. Buildozer Cloud

访问：https://buildozer.io/

直接上传项目，云端自动打包。

---

### 方案 3: Docker 打包

使用预配置的 Docker 镜像：

```bash
# 拉取镜像
docker pull pullum/buildozer

# 打包
docker run -v $(pwd):/home/user/hostcwd pullum/buildozer android debug
```

---

## 📦 打包前的准备

### 1. 检查项目文件

确保以下文件存在：
- ✅ `main.py` - App 入口
- ✅ `buildozer.spec` - 打包配置
- ✅ `requirements.txt` - 依赖列表
- ✅ `core/` - 核心模块
- ✅ `ui/` - UI 模块

### 2. 修改 buildozer.spec

根据需求调整配置：

```ini
[app]
title = 音乐抓取
package.name = musicgrabber
package.domain = org.example

version = 2.0.0

requirements = python3,kivy,yt-dlp,pydub,mutagen,requests,beautifulsoup4

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
```

### 3. 图标和启动图（可选）

```
music_grabber/
├── icon.png          # 应用图标 (512x512)
└── splash.png        # 启动图 (1280x720)
```

---

## 🐛 常见问题

### Q1: Java 版本问题
```
Error: Java 11 is required
```
**解决**: 安装 OpenJDK 11
```bash
sudo apt install openjdk-11-jdk
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

### Q2: Android SDK 下载失败
```
ERROR: Downloading https://dl.google.com/android/repository/...
```
**解决**: 使用镜像或代理
```bash
export HTTPS_PROXY=http://your-proxy:port
```

### Q3: 空间不足
```
No space left on device
```
**解决**: 清理空间或使用外部存储
```bash
df -h  # 检查空间
buildozer android clean  # 清理构建缓存
```

### Q4: 依赖冲突
```
Unmet dependencies
```
**解决**: 在干净的环境中打包（推荐 Docker 或云端）

---

## 📊 打包输出

成功打包后，你会得到：

```
bin/
├── musicgrabber-1.0.0-debug.apk      # 调试版（可安装测试）
└── musicgrabber-1.0.0-release.apk    # 发布版（签名后上架）
```

---

## 🚀 快速验证

打包完成后，在 Android 设备或模拟器上测试：

```bash
# 通过 ADB 安装
adb install bin/musicgrabber-1.0.0-debug.apk

# 或直接传输到设备手动安装
```

---

## 📝 当前项目状态

| 检查项 | 状态 |
|--------|------|
| 项目代码 | ✅ 完整 |
| 依赖配置 | ✅ 完整 |
| buildozer.spec | ✅ 已配置 |
| 本地环境 | ⚠️ 有限制 |
| 打包能力 | ❌ 当前环境无法完成 |

---

## 💡 最佳实践

1. **首次打包**: 使用云端服务（最简单）
2. **频繁打包**: 本地配置 Docker 环境
3. **生产发布**: 使用 GitHub Actions 自动化

---

## 📞 需要帮助？

如果遇到打包问题，可以：

1. 查看 buildozer 日志：`.buildozer/android/platform/build-*/dists/*/build.log`
2. 检查 buildozer 文档：https://buildozer.readthedocs.io/
3. 参考 Kivy 社区：https://kivy.org/doc/stable/

---

**总结**: 项目代码已就绪，但需要在合适的环境中打包。推荐使用**本地 Linux/macOS**或**云端 CI/CD**服务。

**更新时间**: 2026-04-02 15:18
