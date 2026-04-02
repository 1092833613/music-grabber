# ⚠️ ffmpeg 安装说明

**当前状态**: 系统级安装遇到依赖问题

---

## 🔧 解决方案

### 方案 1: 使用 Snap 安装（推荐）⭐

```bash
sudo snap install ffmpeg
```

**优点**: 独立打包，不依赖系统库
**缺点**: 需要 snap 支持

---

### 方案 2: 下载静态编译版本

```bash
# 下载静态编译的 ffmpeg
cd /tmp
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
tar -xf ffmpeg-release-amd64-static.tar.xz

# 移动到系统路径
sudo mv ffmpeg-*/ffmpeg /usr/local/bin/
sudo mv ffmpeg-*/ffprobe /usr/local/bin/
sudo chmod +x /usr/local/bin/ffmpeg
sudo chmod +x /usr/local/bin/ffprobe

# 验证
ffmpeg -version
```

**优点**: 无需依赖，开箱即用
**缺点**: 需要手动下载

---

### 方案 3: 使用 conda（如果有）

```bash
conda install -c conda-forge ffmpeg
```

---

### 方案 4: 继续修复系统依赖

```bash
# 尝试修复依赖
sudo apt --fix-broken install
sudo apt update
sudo apt upgrade -y

# 然后安装
sudo apt install -y ffmpeg
```

---

## ✅ 当前 App 状态

**即使没有 ffmpeg，App 仍可使用以下功能**：

| 功能 | 状态 | 说明 |
|------|------|------|
| 音频下载 | ✅ 可用 | yt-dlp 直接下载 |
| 音乐搜索 | ✅ 可用 | 完全正常 |
| 歌词下载 | ✅ 可用 | 完全正常 |
| 封面下载 | ✅ 可用 | 完全正常 |
| 历史记录 | ✅ 可用 | 完全正常 |
| 播放列表 | ✅ 可用 | 完全正常 |
| **格式转换** | ⚠️ 需要 ffmpeg | 转换功能受限 |
| **ID3 嵌入** | ⚠️ 需要 ffmpeg | 部分功能受限 |

---

## 📝 建议

### 如果你要：

**仅下载音频** → 不需要 ffmpeg，直接使用即可

**需要格式转换** → 安装 ffmpeg（推荐方案 1 或 2）

**完整功能** → 安装 ffmpeg

---

## 🚀 快速验证

安装后验证：

```bash
ffmpeg -version
```

如果显示版本信息，说明安装成功！

---

**更新时间**: 2026-04-02 15:14
