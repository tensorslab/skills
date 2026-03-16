# 社交媒体发布内容

## 1. Awesome AI 列表提交

### 相关列表

1. **Awesome AI Images**
   - 仓库: https://github.com/eugeneyan/awesome-ai-images
   - Issue: 创建 Issue 提交

2. **Awesome AI Video**
   - 仓库: https://github.com/karpathy/awesome-gpt? (需搜索)
   - 搜索: Awesome AI Video Generation

3. **Awesome OpenClaw Skills**
   - 仓库: https://github.com/openclaw/awesome-skills (如果存在)
   - 或者创建自己的列表

### 提交模板

**Title:** Add TensorsLab Vision Skills for OpenClaw

**Description:**
```
Add TensorsLab Vision Skills - An OpenClaw integration for TensorsLab AI models.

Features:
- Image generation (text-to-image, image-to-image, multi-image synthesis)
- Image editing (avatar, watermark removal, object erasure, face replacement)
- Video generation (text-to-video, image-to-video)
- Natural language interaction with auto prompt optimization
- Local auto-save with real-time progress
- OpenClaw compatible with search-friendly keywords

Links:
- GitHub: https://github.com/miyakooy/vison-skills
- npm: @tensorlab/openclaw-skills
- Docs: https://github.com/miyakooy/vison-skills/blob/main/README.md

Category: Image Generation, Video Generation, OpenClaw Skills
```

---

## 2. OpenClaw 社区分享

### Discord

**频道:** #skills 或 #community

**消息模板:**
```
🎉 刚刚为 OpenClaw 开发了一个新技能：TensorsLab Vision Skills！

📦 功能亮点：
• 🎨 图像生成和编辑（文生图、图生图、头像生成、去水印、换脸）
• 🎬 视频生成（文生视频、图生视频、多种运镜）
• 💬 自然语言交互，AI 自动优化提示词
• 📁 本地自动保存，实时进度反馈
• 🔍 丰富的搜索关键词，易于被其他 Agent 发现

🔗 仓库: https://github.com/miyakooy/vison-skills

安装方式：
openclaw install tensorlab-skills

技能开发心得：
- 使用 SKILL.md 规范化定义
- 优化 marketplace.json 的 keywords 提升可发现性
- 添加 GitHub Actions 自动化 CI/CD
- 中英文双语关键词覆盖更多搜索场景

欢迎大家试用和反馈！💬
```

### GitHub Discussions

**类别:** Show and tell

**标题:** [Show and Tell] TensorsLab Vision Skills - OpenClaw 集成图像和视频生成

**内容:**
```
大家好！👋

我刚刚发布了 TensorsLab Vision Skills，一个 OpenClaw 的图像和视频生成技能集成。

## ✨ 主要功能

### 图像技能
- 文生图、图生图、多图合成
- 头像生成（二次元、商务、写实等）
- 水印去除、物体擦除、人脸替换
- 通用图像编辑

### 视频技能
- 文生视频、图生视频
- 多种运镜（推拉摇移、跟拍、环绕）
- 多种比例（横屏、竖屏、正方形）

## 🚀 OpenClaw 集成优势

- **搜索友好**: 丰富的中英文关键词，易于被其他 Agent 发现
- **自然交互**: 日常语言描述，AI 自动优化提示词
- **本地保存**: 自动保存到 ./tensorslab_output/
- **实时进度**: 消除等待焦虑
- **友好提示**: 错误时给出明确解决建议

## 📦 安装

```bash
openclaw install tensorlab-skills
```

或手动克隆：
```bash
git clone https://github.com/miyakooy/vison-skills.git ~/.openclaw/extensions/tensorlab-skills
```

## 💡 技能开发经验分享

在开发这个技能的过程中，我学到了一些 OpenClaw 技能开发的最佳实践：

1. **SKILL.md 规范化**
   - 清晰的功能范围和使用场景
   - 详细的环境要求和使用示例
   - 突出 OpenClaw 集成特性

2. **marketplace.json 优化**
   - 添加丰富的搜索关键词（中英文双语）
   - 设置 search_ranking.priority 为 high
   - 添加 openclaw_compatible: true 标记

3. **GitHub Actions 自动化**
   - CI/CD 流程自动化
   - 自动发布到 npm
   - 跨平台兼容性测试

4. **文档完善**
   - 中英文双语 README
   - 详细的安装和配置指南
   - 清晰的使用示例

欢迎大家试用和反馈！如果有任何问题或建议，请随时提出。💬

🔗 仓库: https://github.com/miyakooy/vison-skills
📚 文档: https://github.com/miyakooy/vison-skills/blob/main/README.md
```

### Reddit (r/OpenSourceAI, r/Python, r/ArtificialIntelligence)

**标题:** [Open Source] TensorsLab Vision Skills - OpenClaw 集成图像和视频生成 AI 技能

**内容:**
```
刚刚发布了 TensorsLab Vision Skills，一个为 OpenClaw 平台开发的 AI 图像和视频生成能力。

## 功能亮点

- 🎨 图像：文生图、图生图、头像生成、水印去除、物体擦除、人脸替换
- 🎬 视频：文生视频、图生视频、多种运镜和比例
- 💬 自然语言交互，AI 自动优化提示词
- 📁 本地自动保存，实时进度反馈
- 🔍 丰富的搜索关键词，易于被其他 Agent 发现

## 技术特点

- OpenClaw Skills 规范兼容
- CI/CD 自动化（GitHub Actions）
- 跨平台支持（Windows, macOS, Linux）
- npm 和 ClawHub 集成

## 链接

- GitHub: https://github.com/miyakooy/vison-skills
- npm: @tensorlab/openclaw-skills

欢迎大家试用和 Star！⭐
```

---

## 3. npm 发布准备

### 发布前检查清单

- [x] package.json 完整配置
- [x] README.md 包含安装说明
- [x] LICENSE 文件存在
- [x] 版本号正确 (1.0.0)
- [ ] npm 账号已创建
- [ ] npm token 已配置
- [ ] 已登录 npm

### 发布命令

```bash
# 确保已登录
npm login

# 发布到 npm
npm publish

# 或者发布为 @tensorlab 组织下的包
npm publish --access=public
```

### 发布后验证

```bash
# 搜索包
npm search tensorlab-skills

# 查看包信息
npm view @tensorlab/openclaw-skills

# 安装测试
npm install -g @tensorlab/openclaw-skills
```

---

## 4. ClawHub 提交

### 提交信息

**项目名称:** TensorsLab Vision Skills

**描述:**
OpenClaw 集成 TensorsLab AI 模型，提供强大的图像和视频生成能力。支持文生图、图生图、头像生成、水印去除、物体擦除、人脸替换、文生视频、图生视频等全套功能。自然语言交互，本地自动保存，极致用户体验。

**分类:** ai-generation, image-processing, video-generation, multimedia, creative-tools

**标签:**
image-generation, text-to-image, image-to-image, avatar, watermark-removal, object-erasure, face-replacement, image-editing, ai-art, photo-editing, 换装, 换脸, 头像, 图片, 图像, p图, 修图, watermark, 去水印, 换衣服, 人像, 照片, 生成图片, 画图, 绘画, 创意, 设计, video-generation, text-to-video, image-to-video, ai-video, cinematic, animation, motion, 视频, 短视频, 制作视频, 生成视频, 特效, 运镜, 电影, 动画

**仓库 URL:** https://github.com/miyakooy/vison-skills

**Homepage:** https://www.tensorslab.com/

**安装命令:**
```bash
openclaw install tensorlab-skills
```

**快速示例:**
```bash
# 图像生成
"画一个在月球上吃热狗的宇航员"

# 视频生成
"做一段 10 秒钟横屏的宇宙飞船穿梭星际的视频"
```

---

## 执行计划

### 第一步：提交到 Awesome AI 列表
1. 搜索相关的 Awesome 列表
2. 创建 Issue 或 PR 提交
3. 等待审核

### 第二步：OpenClaw 社区分享
1. Discord 消息
2. GitHub Discussions
3. Reddit 帖子（可选）

### 第三步：npm 发布
1. 创建 npm 账号
2. 配置 npm token
3. 发布包

### 第四步：ClawHub 提交
1. 填写提交表单
2. 等待审核
3. 正式发布

---

## 预期效果

- 📈 GitHub Stars 增加 50-100
- 📥 npm 下载量 100-500/周
- 🔍 ClawHub 安装量 50-100
- 💬 社区反馈 10-20 条
