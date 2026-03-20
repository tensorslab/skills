# GitHub API 研究和替代方案

## 🔍 GitHub API 调查结果

### GitHub API (REST)
**状态**: ❌ 受限 - 特殊 IP 地址
- 无法访问 docs.github.com
- 无法访问 api.github.com（除 api.github.com/zen）

### GitHub Web API (API v3)
**状态**: ❌ 受限 - 特殊 IP 地址
- curl 到 api.github.com 失败
- 需要有效的 GitHub Token

### GitHub Zen 端点
**结果**: "Favor focus over features"
- 不是可用的 API 端点

---

## 💡 替代方案

### 方案 1: 使用 GitHub CLI（推荐）

**说明**: GitHub 官方命令行工具，功能强大且文档完整

**检查是否已安装**:
```bash
which gh
```

**如果未安装**:
```bash
# macOS
brew install gh

# Ubuntu/Debian
sudo apt-get install gh

# Windows
winget install --id GitHub.cli
```

**使用 gh CLI 创建 Issue**:
```bash
cd /root/.openclaw/workspace/miyakooy-skills
gh issue create \
  --repo jbhuang0604/awesome-computer-vision \
  --title "[New Tool] TensorsLab Vision Skills - OpenClaw Integration" \
  --body-file docs/AWESOME_COMPUTER_VISION.md
```

**优势**:
- ✅ 自动处理认证（已登录即用）
- ✅ 更好的错误处理
- ✅ 丰富的功能（搜索、查看、编辑）
- ✅ 官方维护和支持
- ✅ 可以配置默认仓库

**认证**:
```bash
# 登录
gh auth login

# 检查状态
gh auth status

# 查看当前用户
gh api user | jq -r '.login'
```

---

### 方案 2: 使用 Sessions API（备选）

**说明**: 通过 OpenClaw 的 sessions_spawn 创建子会话
**优势**: 可以访问用户配置的 GitHub Token
**适用**: 需要与 GitHub 交互的任务

**使用示例**:
```python
# 创建子会话
import subprocess
result = subprocess.run([
  'openclaw', 'sessions_spawn',
  '--runtime', 'subagent',
  '--task', '创建 GitHub Issue'
], capture_output=True)
```

---

### 方案 3: 配置 GitHub Token（备选）

**说明**: 直接配置 GitHub PAT（Personal Access Token）

**创建 PAT**:
1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 生成并复制 Token

**配置方式**:

**方式 A: 环境变量**
```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
```

**方式 B: 配置文件**
```bash
echo "ghp_xxxxxxxxxxxx" > ~/.github-token
```

**方式 C: Git 配置**
```bash
git config --global github.token ghp_xxxxxxxxxxxx
```

**使用 Token 创建 Issue**:
```bash
curl -X POST \
  -H "Authorization: token ghp_xxxxxxxxxxxx" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/jbhuang0604/awesome-computer-vision/issues \
  -d '{
    "title": "[New Tool] TensorsLab Vision Skills - OpenClaw Integration",
    "body": "...问题内容..."
  }'
```

---

### 方案 4: 手动创建 Issue（最简单）

**说明**: 通过 GitHub 网站创建 Issue，无需任何认证复杂性

**步骤**:
1. 访问: https://github.com/jbhuang0604/awesome-computer-vision/issues/new
2. 填写标题: `[New Tool] TensorsLab Vision Skills - OpenClaw Integration`
3. 复制内容: 打开 `docs/AWESOME_COMPUTER_VISION.md` 并复制
4. 粘贴到正文
5. 点击 "Submit new issue"

**优势**:
- ✅ 最简单直接
- ✅ 无需安装工具
- ✅ 无需配置 Token
- ✅ 通过 GitHub 网页验证
- ✅ 可以预览和编辑

---

## 🎯 推荐执行顺序

### 今晚（值守）
1. **尝试方案 1** - 检查 gh CLI 是否可用
2. **如果可用，使用 gh CLI** - 自动创建 Issue
3. **如果不可用，尝试方案 3** - 配置 Token 使用 curl
4. **如果都失败，提供方案 4** - 详细的手动指南
5. **记录所有尝试结果** - 保存到文件

### 明天（用户醒来）
1. **报告今晚的结果** - 显示所有尝试的输出
2. **提供下一步建议** - 基于结果给出最合适的方案
3. **等待用户响应** - 提供 PAT 或确认手动完成

---

## 📊 预期结果

| 方案 | 成功概率 | 所需 | 时间 |
|------|----------|------|------|
| gh CLI | 70% | brew install gh | 2-5 分钟 |
| Token + curl | 60% | 创建 PAT | 5-10 分钟 |
| 手动创建 | 100% | 访问网站 | 3-5 分钟 |
| Sessions API | 80% | 用户 Token | N/A |

---

## 🔧 故障排除

### gh CLI 问题

**问题**: `gh: command not found`
**解决**: `brew install gh` (macOS)

**问题**: `gh auth status: not logged in`
**解决**: `gh auth login` 并按提示操作

**问题**: 权限错误
**解决**: 确保 PAT 有 `repo` 权限

---

### Token 问题

**问题**: 401 Unauthorized
**解决**: 检查 Token 格式，确保以 `ghp_` 开头

**问题**: 403 Forbidden
**解决**: 确保 Token 有正确的权限（`repo` 或 `public_repo`）

**问题**: Token 过期
**解决**: 创建新的 PAT

---

## 💾 总结

### 当前限制
- ❌ GitHub API 受限（特殊 IP）
- ❌ Web fetch 受限
- ⏸️ 需要替代方案

### 可用方案
1. ✅ **gh CLI** - 官方推荐，功能强大
2. ✅ **PAT + curl** - 灵活，不依赖工具
3. ✅ **手动创建** - 最简单，立即可行
4. ✅ **Sessions API** - 可用用户配置

### 执行策略
- 🎯 优先级：gh CLI > Token > 手动
- 🔄 自动化：尽量自动化
- 💬 保守：失败后提供手动方案
- 📊 记录：所有尝试都记录

---

## 📝 下一步行动

1. 检查 gh CLI 可用性
2. 尝试使用 gh CLI 创建 Issue
3. 如果成功，更新状态并返回 Issue URL
4. 如果失败，尝试其他方案
5. 记录所有结果到文件
6. 准备给用户的完整报告

---

## 📚 参考资料

- GitHub CLI 文档: https://cli.github.com/manual/
- GitHub REST API: https://docs.github.com/en/rest
- 创建 Issue API: https://docs.github.com/en/rest/issues/create-an-issue
- PAT 权限: https://docs.github.com/en/authentication/keeping-your-access-tokens/creating-a-personal-access-token
