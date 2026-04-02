# 🔑 GitHub 认证设置指南

**问题**: 推送需要 GitHub 认证

---

## ⚠️ 当前情况

推送命令需要登录 GitHub，但当前环境无法交互式登录。

**错误信息**:
```
fatal: could not read Username for 'https://github.com'
```

---

## ✅ 解决方案（3 选 1）

### 方案 1: 使用 Personal Access Token（推荐）⭐

#### 第 1 步：创建 Token

1. 访问：https://github.com/settings/tokens
2. 点击 **"Generate new token (classic)"**
3. 填写：
   - **Note**: `Music Grabber App`
   - **Expiration**: `No expiration`（或选择 90 天）
   - **Scopes**: 勾选 ✅ `repo`（完整控制私有仓库）
4. 点击 **"Generate token"**
5. **复制 Token**（只显示一次！）

#### 第 2 步：使用 Token 推送

拿到 Token 后，执行：

```bash
cd /home/admin/openclaw/workspace/music_grabber

# 方法 A: 在 URL 中包含 Token
git remote set-url origin https://1092833613:你的_TOKEN@github.com/1092833613/music-grabber.git
git push -u origin main

# 方法 B: 使用 credential helper
git config --global credential.helper store
git push -u origin main
# 然后输入用户名和 Token
```

---

### 方案 2: 在本地电脑推送（最简单）🌟

如果你有自己的电脑：

1. **下载项目代码**（从服务器）：
   ```bash
   # 在你的电脑上
   scp -r admin@服务器 IP:/home/admin/openclaw/workspace/music_grabber ~/Downloads/
   ```

2. **在本地推送**：
   ```bash
   cd ~/Downloads/music_grabber
   git init
   git add -A
   git commit -m "Initial commit"
   git remote add origin https://github.com/1092833613/music-grabber.git
   git push -u origin main
   ```

3. **GitHub Desktop**（图形界面，更简单）：
   - 下载：https://desktop.github.com/
   - 登录 GitHub
   - 添加项目文件夹
   - 点击 "Publish repository"

---

### 方案 3: 使用 SSH 密钥（高级）

#### 第 1 步：生成 SSH 密钥

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

#### 第 2 步：添加公钥到 GitHub

1. 查看公钥：
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

2. 复制输出内容

3. 访问：https://github.com/settings/keys
4. 点击 **"New SSH key"**
5. 粘贴公钥
6. 保存

#### 第 3 步：使用 SSH 推送

```bash
# 改用 SSH URL
git remote set-url origin git@github.com:1092833613/music-grabber.git
git push -u origin main
```

---

## 🎯 推荐方案

**最简单**: 方案 2 - 在本地电脑推送

**最快**: 方案 1 - 使用 Token（如果你能创建 Token）

**最安全**: 方案 3 - SSH 密钥

---

## 📝 详细步骤（方案 1）

### 1. 创建 Token

访问：https://github.com/settings/tokens

```
┌─────────────────────────────────────┐
│ Generate a personal access token    │
│                                     │
│ Note: Music Grabber App             │
│ Expiration: No expiration           │
│ Scopes: ✅ repo                     │
│                                     │
│        [Generate token]             │
└─────────────────────────────────────┘
```

### 2. 复制 Token

生成的 Token 类似：
```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**⚠️ 只显示一次！立即复制保存！**

### 3. 推送代码

```bash
cd /home/admin/openclaw/workspace/music_grabber

# 替换为你的 Token
git remote set-url origin https://1092833613:ghp_xxxxxxxx@github.com/1092833613/music-grabber.git
git push -u origin main
```

---

## 🔍 验证推送

推送成功后：

1. 访问：https://github.com/1092833613/music-grabber
2. 应该看到所有代码文件
3. 点击 **Actions** 标签
4. 看到 **"Build Android APK"** 工作流运行中

---

## ❓ 常见问题

### Q: Token 创建后看不到？
**A**: 刷新页面或重新创建（只能看到一次）

### Q: 推送还是失败？
**A**: 检查 Token 是否有 `repo` 权限

### Q: Token 安全吗？
**A**: 可以隨時删除：https://github.com/settings/tokens

---

## 📞 需要帮助？

**如果你已经创建了 Token**：

把 Token 发给我（私下发），我帮你执行推送命令。

**或者**：

按照上方步骤在自己电脑上操作。

---

**更新时间**: 2026-04-02 16:12
