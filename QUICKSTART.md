# 音乐抓取 App - 快速开始指南

## 📦 项目已创建完成！

项目位置：`/home/admin/openclaw/workspace/music_grabber/`

## 🚀 立即运行（桌面测试）

### 步骤 1: 安装依赖

```bash
cd /home/admin/openclaw/workspace/music_grabber
pip install -r requirements.txt
```

### 步骤 2: 安装 ffmpeg

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
从 https://ffmpeg.org/download.html 下载并添加到 PATH

### 步骤 3: 运行 App

```bash
python main.py
```

## 📱 打包 Android APK

### 方法 A: 本地打包（需要 Linux/macOS）

```bash
# 1. 安装 buildozer
pip install buildozer

# 2. 下载 Android SDK/NDK（buildozer 会自动处理）
buildozer init

# 3. 打包
buildozer -v android debug

# APK 输出位置：bin/musicgrabber-1.0.0-debug.apk
```

### 方法 B: 云端打包（推荐，无需配置环境）

使用以下服务：
- **Buildozer Cloud**: https://buildozer.io/
- **GitHub Actions**: 配置 CI/CD 自动打包

## 📖 功能说明

### 核心功能

| 功能 | 说明 |
|------|------|
| 单视频下载 | 粘贴链接 → 选择格式 → 下载 |
| 格式转换 | MP3/WAV/FLAC/M4A/OGG |
| 批量下载 | 歌单/专辑批量下载 |
| 进度显示 | 实时下载进度和速度 |

### 支持平台

yt-dlp 支持 1000+ 网站，包括：
- YouTube、B 站、抖音、快手
- 网易云音乐、QQ 音乐（部分）
- SoundCloud、Bandcamp
- 完整列表：https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md

## ⚠️ 重要提醒

### 版权合规

- ✅ 可以下载：无版权音乐、CC 协议内容、自己上传的内容
- ❌ 禁止用于：商业分发、绕过付费墙、侵犯版权

### 使用建议

1. **个人学习**: 仅供研究和技术学习
2. **版权声明**: 分发时请保留版权声明
3. **合法使用**: 遵守当地法律法规

## 🛠️ 下一步开发建议

### 功能增强

- [ ] 添加搜索功能（直接搜索音乐）
- [ ] 添加下载历史记录
- [ ] 支持歌词下载
- [ ] 支持封面图下载
- [ ] 添加播放列表管理

### UI 优化

- [ ] 深色模式
- [ ] 下载队列管理
- [ ] 文件浏览器集成
- [ ] 通知栏进度显示（Android）

### 性能优化

- [ ] 多线程并发下载
- [ ] 断点续传
- [ ] 缓存机制

## 📞 问题反馈

遇到问题时：

1. 检查依赖是否安装完整
2. 查看 yt-dlp 是否支持目标网站
3. 确保 ffmpeg 已正确安装
4. 查看日志文件（如有）

---

**开发完成时间**: 2026-04-02  
**版本**: 1.0.0
