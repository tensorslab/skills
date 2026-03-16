# npm 发布完整指南

## 📋 发布前检查清单

### 必需文件
- [x] package.json ✅
- [x] README.md ✅
- [x] LICENSE (需要添加）
- [ ] .npmignore (可选但推荐）

### package.json 检查
- [x] name: @tensorlab/openclaw-skills ✅
- [x] version: 1.0.0 ✅
- [x] description: 已填写 ✅
- [x] keywords: 丰富关键词 ✅
- [x] repository: GitHub 链接 ✅
- [x] homepage: 文档链接 ✅
- [x] bugs: Issues 链接 ✅
- [x] license: MIT ✅
- [ ] main/exports/index (可选)

---

## 📝 步骤 1: 添加 LICENSE 文件

```bash
cd /root/.openclaw/workspace/miyakooy-skills
```

创建 LICENSE 文件，内容如下：

```
MIT License

Copyright (c) 2026 TensorsLab

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📝 步骤 2: 创建 .npmignore（可选）

创建 .npmignore 文件，排除不需要发布的文件：

```
.git
.gitignore
.github
.gitattributes
docs/
examples/
tests/
*.md
!README.md
!LICENSE
```

---

## 📝 步骤 3: 注册/登录 npm

### 如果没有 npm 账号
1. 访问：https://www.npmjs.com/signup
2. 填写用户名、邮箱、密码
3. 验证邮箱（重要！）

### 登录 npm
```bash
npm login
```

会提示：
```
Username: <你的 npm 用户名>
Password: <你的 npm 密码>
Email: (this is public) <你的邮箱>
```

### 或者使用 Token（推荐）
1. 访问：https://www.npmjs.com/settings/tokens
2. 点击 "Create New Token"
3. 选择 "Automation" 或 "Publish"
4. 复制生成的 Token
5. 登录：
```bash
npm login --auth-only
Username: <你的用户名>
Password: <粘贴 Token>
```

---

## 📝 步骤 4: 检查包名是否可用

```bash
npm view @tensorlab/openclaw-skills
```

如果返回包信息，说明包名已被占用
如果返回 404 错误，说明包名可用

---

## 📝 步骤 5: 发布到 npm

### 发布前验证
```bash
npm pack --dry-run
```

这会模拟打包过程，检查是否有错误

### 正式发布
```bash
cd /root/.openclaw/workspace/miyakooy-skills
npm publish
```

### 如果是组织包（@tensorlab）
```bash
npm publish --access=public
```

---

## 📝 步骤 6: 验证发布

### 搜索包
```bash
npm search tensorlab-skills
```

### 查看包信息
```bash
npm view @tensorlab/openclaw-skills
```

### 测试安装
```bash
npm install -g @tensorlab/openclaw-skills
```

---

## 🔧 常见问题

### 问题 1: 403 Forbidden
**原因**: 认证失败
**解决**: 
- 确认已登录：`npm whoami`
- 重新登录：`npm login`
- 检查是否有发布权限

### 问题 2: 包名已被占用
**原因**: @tensorlab/openclaw-skills 已被发布
**解决**:
- 修改 package.json 中的 name
- 例如：@tensorlab/openclaw-vision-skills
- 重新发布

### 问题 3: 语法错误
**原因**: package.json 格式错误
**解决**:
```bash
npm run validate
# 或
npm validate package.json
```

### 问题 4: 需要 2FA
**原因**: npm 需要 2FA 短信验证
**解决**:
- 输入 2FA 短信
- 或使用 Token（推荐）

---

## 📊 发布后维护

### 更新版本
修改 package.json 中的 version：
```json
"version": "1.0.1"
```

提交并推送：
```bash
git add package.json
git commit -m "chore: bump version to 1.0.1"
git push
```

重新发布：
```bash
npm publish
```

### 使用 git tag（推荐）
```bash
git tag v1.0.0
git push origin v1.0.0
npm publish
```

---

## 🎯 预期效果

发布成功后：
- 📦 可以通过 `npm install @tensorlab/openclaw-skills` 安装
- 📊 npm 页面显示包信息
- 🔍 在 npm 搜索中可以找到
- 📈 每周下载量开始统计

---

## 📮 npm 包页面

发布成功后访问：
https://www.npmjs.com/package/@tensorlab/openclaw-skills

---

## ⚠️ 重要提示

1. **第一次发布**: 需要验证邮箱
2. **组织包 (@tensorlab)**: 需要组织权限
3. **版本号**: 遵循语义化版本 (1.0.0)
4. **敏感信息**: 不要在 package.json 中包含 API Key
5. **文档**: README.md 会作为包描述显示

---

## ✅ 成功标志

看到以下信息表示发布成功：
```
npm notice 📦 @tensorlab/openclaw-skills@1.0.0
npm notice === Tarball Contents ===
...
npm notice 🎉 published successfully
```

---

## 🎉 下一步

发布成功后，我们进行第四步：**提交到 ClawHub**

完成后告诉我 npm 发布的结果！
