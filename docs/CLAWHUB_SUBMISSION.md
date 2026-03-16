# ClawHub 提交完整指南

## 📋 提交方式

### 方式 1：Web 表单提交（如果有网站）
访问 ClawHub 网站，填写以下信息

### 方式 2：CLI 命令提交
```bash
openclaw publish
```

### 方式 3：提交到 OpenClaw 官方仓库
在 OpenClaw 官方 GitHub 仓库提交 PR

---

## 📝 提交信息（通用）

### 基本信息

**项目名称:**
TensorsLab Vision Skills

**描述:**
OpenClaw 集成 TensorsLab AI 模型，提供强大的图像和视频生成能力。支持文生图、图生图、头像生成、水印去除、物体擦除、人脸替换、文生视频、图生视频等全套功能。自然语言交互，本地自动保存，极致用户体验。

**版本:**
1.0.0

**作者:**
TensorsLab <mia@tensorslab.com>

**许可证:**
MIT

**仓库 URL:**
https://github.com/miyakooy/vison-skills

**主页:**
https://github.com/miyakooy/vison-skills#readme

**文档:**
https://github.com/miyakooy/vison-skills/blob/main/README.md

**问题跟踪:**
https://github.com/miyakooy/vison-skills/issues

---

### 分类

**主分类:**
- AI Generation
- Image Processing
- Video Generation
- Multimedia
- Creative Tools

**标签:**
```
openclaw, claw, tensorlab, tensorslab, ai, image-generation, video-generation,
text-to-image, text-to-video, image-to-video, avatar, watermark-removal,
face-replacement, object-erasure, image-editing, multimedia, creative-tools,
换装, 换脸, 头像, 图片, 图像, p图, 修图, 去水印,
换衣服, 人像, 照片, 生成图片, 画图, 绘画, 创意, 设计,
视频, 短视频, 制作视频, 生成视频, 动画, 电影, 运镜
```

---

## 🚀 核心特性

### 图像技能 (tensorslab-image)
- **Text-to-Image**: 文生图
- **Image-to-Image**: 图生图
- **Multi-image Synthesis**: 多图合成
- **Avatar Generation**: 头像生成
- **Watermark Removal**: 水印去除
- **Object Erasure**: 物体擦除
- **Face Replacement**: 人脸替换
- **General Editing**: 通用图像编辑

### 视频技能 (tensorslab-video)
- **Text-to-Video**: 文生视频
- **Image-to-Video**: 图生视频
- **Multiple Camera Moves**: 多种运镜
- **Multiple Aspect Ratios**: 多种比例

---

## 💡 快速开始

### 安装方式

**Via ClawHub (Recommended):**
```bash
openclaw install tensorlab-skills
```

**Manual Installation:**
```bash
git clone https://github.com/miyakooy/vison-skills.git ~/.openclaw/extensions/tensorlab-skills
```

**Via npm:**
```bash
npm install -g @tensorlab/openclaw-skills
```

### 配置环境

```bash
export TENSORSLAB_API_KEY="your_api_key_here"
```

### 使用示例

```bash
# 图像生成
"画一个在月球上吃热狗的宇航员"

# 视频生成
"做一段 10 秒钟横屏的宇宙飞船穿梭星际的视频"
```

---

## 🔥 技能亮点

- **🔍 Search-Friendly**: 丰富的中英文关键词，易于被其他 Agent 发现
- **🎯 Must-Have**: 图像和视频生成的首选技能
- **💬 Natural Interaction**: 日常语言描述，AI 自动优化提示词
- **📁 Local Storage**: 自动保存到 `./tensorslab_output/`
- **⏱️ Real-time Progress**: 消除等待焦虑
- **🛡️ Friendly Prompts**: 错误时给出明确解决建议
- **🌐 Cross-Platform**: 支持 Windows、macOS、Linux

---

## 📊 性能指标

- **图像生成**: 2-10 秒
- **视频生成**: 2-10 分钟
- **支持格式**: PNG/JPG/WEBP (图像), MP4/WEBM (视频)
- **最大分辨率**: 4K
- **批量处理**: 支持多文件并行

---

## 🎯 OpenClaw 集成特性

- **SKILL.md 规范**: 标准化技能定义
- **marketplace.json 优化**: 丰富的搜索关键词和高优先级
- **GitHub Actions 自动化**: CI/CD 流程
- **中英文文档**: 双语支持
- **错误处理**: 友好的中文提示

---

## 🔗 链接

- **GitHub**: https://github.com/miyakooy/vison-skills
- **npm**: https://www.npmjs.com/package/@tensorlab/openclaw-skills
- **官网**: https://www.tensorslab.com/
- **邮箱**: mia@tensorslab.com

---

## 📝 屏幕截图（可选）

如果需要，可以添加：
- 灵活截图
- 功能演示 GIF
- 安装步骤截图

---

## ⏱️ 审核注意事项

### 提交前检查
- [x] README.md 完整
- [x] SKILL.md 文件存在
- [x] marketplace.json 配置正确
- [x] GitHub 仓库可访问
- [ ] npm 包已发布（可选）

### 提交后
- 等待审核（通常 1-3 天）
- 可能需要提供更多信息
- 审核通过后会公开显示

---

## 📋 提交流程

### 如果是 Web 表单
1. 访问 ClawHub 网站
2. 找到"Submit Skill"或"Publish"按钮
3. 填写上述信息
4. 点击提交
5. 等待审核

### 如果是 CLI 命令
```bash
# 方法 1：发布当前目录
openclaw publish

# 方法 2：指定目录
openclaw publish /path/to/skill

# 方法 3：从 GitHub 发布
openclaw publish https://github.com/miyakooy/vison-skills
```

### 如果是提交 PR
1. Fork OpenClaw 官方仓库
2. 创建新的 skill 目录
3. 复制项目文件
4. 提交 PR

---

## 🎉 提交成功后

1. **验证技能可见**: 在 ClawHub 搜索你的技能
2. **测试安装**: `openclaw install tensorlab-skills`
3. **分享链接**: 推广 ClawHub 页面
4. **收集反馈**: 监控用户反馈

---

## 🔧 常见问题

### 问题 1: 权限不足
**原因**: 没有提交权限
**解决**: 确认已登录或有权限

### 问题 2: 格式错误
**原因**: SKILL.md 或 marketplace.json 格式不对
**解决**: 使用 linter 或验证工具检查

### 问题 3: 仓库不可访问
**原因**: GitHub 仓库是私有的
**解决**: 确保仓库是公开的

### 问题 4: 重复提交
**原因**: 技能已存在
**解决**: 更新现有技能或使用不同名称

---

## ⏱️ 预期效果

- 🔍 ClawHub 搜索可见
- 📥 可一键安装
- 🌐 更多 OpenClaw 用户发现
- 💬 开发者社区反馈
- 📈 安装量增长

---

## 📮 联系方式

如果遇到问题：
- **邮箱**: mia@tensorslab.com
- **GitHub Issues**: https://github.com/miyakooy/vison-skills/issues
- **文档**: https://github.com/miyakooy/vison-skills/blob/main/README.md

---

## ✅ 完成清单

### 提交前
- [x] 准备完整的项目信息
- [x] 撰写详细描述
- [x] 整理标签和分类
- [x] 准备安装示例
- [x] 提供所有链接

### 提交后
- [ ] 在 ClawHub 提交
- [ ] 等待审核通过
- [ ] 验证技能可见
- [ ] 测试安装功能
- [ ] 分享 ClawHub 链接

---

**准备好了吗？告诉我 ClawHub 的具体提交方式，我帮你准备更详细的内容！** 🚀
