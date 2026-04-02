# 🎵 音乐抓取 App - 完整版

基于 Python + Kivy 的跨平台音频下载工具，支持从任意网页抓取音频。

## ⚠️ 版权声明

**本工具仅供学习和研究使用**

- ✅ 可以下载：无版权音乐、CC 协议内容、自己上传的内容
- ❌ 禁止用于：商业分发、绕过付费墙、侵犯版权

---

## ✨ 功能特性（完整版）

### 核心功能
- 🌐 **通用抓取**：支持 1000+ 网站（YouTube、B 站、抖音等）
- 🎵 **格式转换**：MP3、WAV、FLAC、M4A、OGG
- 📁 **批量下载**：支持歌单/专辑批量下载

### 新增功能 🆕
- 🔍 **音乐搜索**：多音源搜索（YouTube/SoundCloud/Bandcamp）
- 📝 **歌词下载**：自动匹配 LRC 格式歌词
- 🖼️ **封面下载**：自动下载并嵌入 ID3 标签
- 📋 **历史记录**：完整下载历史管理
- 🎵 **播放列表**：创建和管理播放列表

---

## 🚀 快速开始

### 桌面端运行

```bash
# 1. 安装依赖
cd music_grabber
pip install -r requirements.txt

# 2. 安装 ffmpeg（格式转换必需）
# Ubuntu/Debian:
sudo apt install ffmpeg
# macOS:
brew install ffmpeg
# Windows: 从 https://ffmpeg.org/download.html 下载

# 3. 运行 App
python main.py
```

### Android 打包

```bash
# 1. 安装 Buildozer
pip install buildozer

# 2. 打包 APK
buildozer -v android debug

# 输出：bin/musicgrabber-1.0.0-debug.apk
```

---

## 📖 使用指南

### 1️⃣ 下载单个音频

1. 打开 App
2. 粘贴视频/音频链接
3. 选择输出格式（MP3/WAV/FLAC 等）
4. 点击「获取信息」预览
5. 点击「下载」

### 2️⃣ 搜索音乐 🆕

1. 切换到「搜索」标签
2. 输入歌曲名或歌手
3. 选择音源（YouTube/SoundCloud 等）
4. 点击搜索
5. 选择结果直接下载

### 3️⃣ 批量下载歌单

1. 点击「歌单下载」
2. 粘贴歌单/专辑链接
3. 设置最大下载数量（可选）
4. 开始下载

### 4️⃣ 查看下载历史 🆕

1. 切换到「历史」标签
2. 查看所有下载记录
3. 支持搜索历史记录
4. 支持清空历史

### 5️⃣ 管理播放列表 🆕

1. 切换到「播放列表」标签
2. 创建新播放列表
3. 添加歌曲到列表
4. 支持导入/导出

---

## 📁 项目结构

```
music_grabber/
├── main.py                    # App 入口
├── core/
│   ├── downloader.py          # 下载核心
│   ├── converter.py           # 格式转换
│   ├── batch.py              # 批量下载
│   ├── searcher.py           # 音乐搜索 🆕
│   ├── lyrics.py             # 歌词下载 🆕
│   ├── cover.py              # 封面下载 🆕
│   ├── history.py            # 历史记录 🆕
│   ├── playlist.py           # 播放列表 🆕
│   └── __init__.py
├── ui/
│   ├── main_screen.py         # 主界面
│   ├── search_screen.py       # 搜索界面 🆕
│   ├── history_screen.py      # 历史界面 🆕
│   ├── playlist_screen.py     # 播放列表界面 🆕
│   └── __init__.py
├── data/
│   ├── history.json           # 下载历史 🆕
│   └── playlists.json         # 播放列表 🆕
├── buildozer.spec             # Android 打包配置
├── requirements.txt           # 依赖
├── README.md                  # 完整文档
└── QUICKSTART.md              # 快速开始
```

---

## 🔧 技术栈

- **核心**: yt-dlp（视频/音频下载）
- **界面**: Kivy（跨平台 Python UI）
- **转换**: pydub + ffmpeg
- **ID3**: mutagen（音频标签编辑）
- **打包**: Buildozer（Android）、kivy-ios（iOS）

---

## ⚙️ API 使用示例

### Python 代码调用

```python
from core.downloader import MusicDownloader
from core.searcher import MusicSearcher
from core.lyrics import LyricsDownloader
from core.cover import CoverDownloader

# 1. 搜索音乐
searcher = MusicSearcher()
result = searcher.search("周杰伦 七里香", max_results=5)
for item in result["results"]:
    print(f"  - {item['title']}")

# 2. 下载音频
downloader = MusicDownloader()
result = downloader.download(
    url="https://www.youtube.com/watch?v=xxx",
    format="mp3",
)

# 3. 下载歌词
lyrics_dl = LyricsDownloader()
lyrics_result = lyrics_dl.download_lyrics(
    title="七里香",
    artist="周杰伦",
)

# 4. 下载并嵌入封面
cover_dl = CoverDownloader()
cover_result = cover_dl.download_and_embed(
    url="https://www.youtube.com/watch?v=xxx",
    audio_file="./downloads/song.mp3",
    title="七里香",
    artist="周杰伦",
)
```

### 历史记录管理

```python
from core.history import DownloadHistory

history = DownloadHistory()

# 添加记录
history.add(
    url="https://...",
    title="歌曲名",
    artist="歌手",
    filename="./downloads/song.mp3",
)

# 查询历史
all_items = history.get_all()
recent = history.get_recent(days=7)
searched = history.search("周杰伦")

# 删除
history.delete(record_id=1)
```

### 播放列表管理

```python
from core.playlist import PlaylistManager

manager = PlaylistManager()

# 创建播放列表
playlist = manager.create("我的最爱", "最喜欢的歌曲")

# 添加歌曲
manager.add_track(playlist["id"], {
    "title": "七里香",
    "artist": "周杰伦",
    "url": "https://...",
})

# 导出
manager.export(playlist["id"], "my_playlist.json")
```

---

## 🐛 常见问题

### Q: 下载失败怎么办？
A: 检查网络连接，确认链接有效，更新 yt-dlp：`pip install -U yt-dlp`

### Q: 歌词下载失败？
A: 部分歌曲可能没有歌词，尝试手动添加 LRC 文件

### Q: 封面嵌入失败？
A: 确保安装了 mutagen：`pip install mutagen`

### Q: Android 打包报错？
A: 确保 Python 版本 3.7-3.11，更新 buildozer：`pip install -U buildozer`

### Q: 支持哪些网站？
A: 完整列表见 https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - 强大的视频下载工具
- [Kivy](https://kivy.org/) - 跨平台 Python UI 框架
- [pydub](https://github.com/jiaaro/pydub) - 音频处理库
- [mutagen](https://github.com/quodlibet/mutagen) - ID3 标签编辑

---

**开发完成时间**: 2026-04-02  
**版本**: 2.0.0（完整版）  
**新增功能**: 搜索、歌词、封面、历史、播放列表
