# 需要的权限和 Token

## 🔑 GitHub Personal Access Token (PAT)

### 为什么需要 PAT？
当前用于 ClawHub 的 Token 无法用于 GitHub API，需要：
- `repo` 权限：创建 Issue 到仓库
- `public_repo` 权限：访问公开仓库

### 如何创建 PAT？

#### 步骤 1: 访问 GitHub Token 设置
1. 访问：https://github.com/settings/tokens
2. 点击 **"Generate new token (classic)"**
3. 或访问：https://github.com/settings/tokens/new

#### 步骤 2: 配置 Token
1. **Token 名称**: `awesome-list-submission` (或任意名称)
2. **Expiration**: 选择过期时间（建议 30 天或 90 天）
3. **Scopes**: 勾选以下权限：
   - ✅ `repo` (Full control of private repositories)
   - ✅ `public_repo` (Access to public repositories)
4. 点击 **"Generate token"**
5. **立即复制** Token（只显示一次！）

### Token 格式
```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

以 `ghp_` 开头

---

## 🔑 ClawHub Token

### 当前状态
✅ 已配置：`clh_mZ1ybyNg0Mb8qjMm5Y0JmLs9x1jrMiPGutWhLACl2lp04`

### 用途
- 发布技能到 ClawHub
- 提交技能元数据
- 管理技能版本

---

## 📋 需要的 Token 汇总

| 用途 | 状态 | 来源 |
|------|------|------|
| GitHub API (创建 Issue) | ❌ 缺失 | 需要创建 PAT |
| ClawHub (发布技能) | ✅ 已配置 | 从用户提供 |

---

## 💡 使用方式

### 方式 1: 明天提供给 Token
醒来后告诉我：
```
我的 GitHub PAT 是: ghp_xxxxxxxxxxxx
```

我会立即继续任务。

### 方式 2: 保存到配置文件
如果你希望保存 Token 到服务器，告诉我：
```
保存 GitHub PAT: ghp_xxxxxxxxxxxx
```

我会安全地保存并使用。

---

## 🛡️ 安全提醒

- ⚠️ **PAT 只显示一次**：创建后立即复制
- 🔒 不要在代码、消息、公开分享 PAT
- 🗑️ 定期轮换 PAT：建议 30-90 天
- 🚫 使用最小权限：只勾选需要的 Scopes
- ❌ 不要使用 OAuth Token 替代 PAT

---

## 🔧 常见问题

### Q: 我不知道之前是否创建过 PAT
**A**: 访问 https://github.com/settings/tokens 查看所有活动的 Token

### Q: PAT 过期了怎么办
**A**: 
1. 访问 Token 设置页面
2. 找到过期的 Token
3. 删除或重新生成
4. 提供新的 PAT

### Q: 可以使用不同的 Token 吗
**A**: 可以，只要有 `repo` 和 `public_repo` 权限

---

## 📮 参考链接

- GitHub Token 设置: https://github.com/settings/tokens
- 创建新 Token: https://github.com/settings/tokens/new
- PAT 权限说明: https://docs.github.com/en/authentication/keeping-your-account-secure/managing-your-personal-access-tokens
- ClawHub 文档: https://clawhub.ai/docs
