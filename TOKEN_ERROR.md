# ⚠️ Token 权限不足

**错误信息**:
```
refusing to allow a Personal Access Token to create or update workflow 
`.github/workflows/build.yml` without `workflow` scope
```

---

## 🔑 需要重新创建 Token

### 步骤：

1. **访问**: https://github.com/settings/tokens

2. **删除旧 Token**（可选，为了安全）:
   - 找到刚才创建的 Token
   - 点击 "Delete"

3. **创建新 Token**:
   - 点击 "Generate new token (classic)"
   - **Note**: `Music Grabber App`
   - **Expiration**: `No expiration`
   - **Scopes**（权限）: 
     - ✅ `repo` (Full control of private repositories)
     - ✅ **`workflow`** (Update GitHub Action workflows) ← **这个必需！**

4. **复制新 Token**

5. **发给我新 Token**，我重新推送

---

## 📸 权限勾选示意

```
┌─────────────────────────────────────┐
│ Scopes:                             │
│                                     │
│ ☑ repo                              │
│   Full control of private repos     │
│                                     │
│ ☑ workflow  ← 必需勾选这个！        │
│   Update GitHub Action workflows    │
│                                     │
│        [Generate token]             │
└─────────────────────────────────────┘
```

---

## 🎯 快速总结

**需要的权限**:
- ✅ `repo` - 代码仓库权限
- ✅ `workflow` - GitHub Actions 权限（推送 workflow 文件必需）

**创建后**:
- 复制新 Token
- 发给我
- 我帮你重新推送

---

**请重新创建 Token 并发送给我！**
