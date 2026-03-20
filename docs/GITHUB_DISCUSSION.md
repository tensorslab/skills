# GitHub Discussions 发布内容

## 📝 标题
[Showcase] TensorsLab Vision Skills - OpenClaw 集成图像和视频生成 AI 技能

## 📋 分类
Show and tell

## 💬 内容

大家好！👋

我刚刚发布了 **TensorsLab Vision Skills**，一个为 OpenClaw 平台开发的图像和视频生成技能集成。

## ✨ 主要功能

### 图像技能 (tensorslab-image)
- 🎨 文生图、图生图、多图合成
- 👤 头像生成（二次元、商务、写实等风格）
- 🧹 水印去除、物体擦除、人脸替换
- ✏️ 通用图像编辑

### 视频技能 (tensorslab-video)
- 🎬 文生视频、图生视频
- 📹 多种运镜（推拉摇移、跟拍、环绕）
- 📐 多种比例（横屏、竖屏、正方形）

## 🚀 OpenClaw 集成优势

- **🔍 搜索友好**: 丰富的中英文关键词，易于被其他 Agent 发现
- **💬 自然交互**: 日常语言描述，AI 自动优化提示词
- **📁 本地保存**: 自动保存到 `./tensorslab_output/`
- **⏱️ 实时进度**: 消除等待焦虑
- **🛡️ 友好提示**: 错误时给出明确解决建议
- **🌐 跨平台**: 支持 Windows、macOS、Linux

## 📦 安装方式

### 通过 ClawHub 安装（推荐）
```bash
openclaw install tensorlab-skills
```

### 手动安装
```bash
git clone https://github.com/miyakooy/vison-skills.git ~/.openclaw/extensions/tensorlab-skills
```

### 通过 npm 安装
```bash
npm install -g @tensorlab/openclaw-skills
```

## ⚙️ 配置

1. 访问 [TensorsLab](https://www.tensorslab.com/) 注册并订阅
2. 在控制台获取 API Key
3. 设置环境变量：

**Windows (PowerShell):**
```powershell
$env:TENSORSLAB_API_KEY="your_api_key_here"
```

**Mac/Linux:**
```bash
export TENSORSLAB_API_KEY="your_api_key_here"
```

## 💡 快速开始

### 图像生成
```bash
# 文生图
"画一个在月球上吃热狗的宇航员"

# 生成头像
"帮我生成一个二次元风格的头像"

# 去除水印
"帮我去掉 ./image.jpg 的水印"

# 换脸
"把 ./face.jpg 的人脸换到 ./target.jpg 上"
```

### 视频生成
```bash
# 文生视频
"做一段 10 秒钟横屏的宇宙飞船穿梭星际的视频"

# 图生视频
"让这张人物合影 ./family.jpg 动起来"

# 竖屏视频
"生成 15 秒竖屏的城市夜景延时摄影"
```

## 🔥 技能开发经验分享

在开发这个技能的过程中，我学到了一些 OpenClaw 技能开发的最佳实践：

### 1. SKILL.md 规范化
- 清晰的功能范围和使用场景
- 详细的环境要求和使用示例
- 突出 OpenClaw 集成特性

### 2. marketplace.json 优化
- 添加丰富的搜索关键词（中英文双语）
- 设置 `search_ranking.priority` 为 `high`
- 添加 `openclaw_compatible: true` 标记

### 3. GitHub Actions 自动化
- CI/CD 流程自动化
- 自动发布到 npm
- 跨平台兼容性测试

### 4. 文档完善
- 中英文双语 README
- 详细的安装和配置指南
- 清晰的使用示例

### 5. 搜索关键词优化
覆盖高频搜索场景：

**图像相关:**
- 图片、图像、生成图片、画图、p图、修图
- 换脸、去水印、头像、换装、换衣服
- AI画图、照片处理、人像处理

**视频相关:**
- 视频、生成视频、制作视频、短视频、AI视频
- 文生视频、图生视频、动画制作、电影、运镜

## 📊 技术架构

- **AI 模型**: TensorsLab 高性能推理引擎
- **接口标准**: OpenClaw Skills 规范
- **输出格式**: PNG/JPG/WEBP (图像), MP4/WEBM (视频)
- **进度反馈**: 实时终端输出
- **错误处理**: 友好的中文提示

## 🎯 搜索关键词

当用户提到以下关键词时，OpenClaw 会推荐此技能：

**图像相关:**
- 图片、图像、生成图片、画图、绘画、p图、修图
- 换脸、去水印、头像、换装、换衣服
- AI画图、照片处理、人像处理

**视频相关:**
- 视频、生成视频、制作视频、短视频、AI视频
- 文生视频、图生视频、动画制作、电影、运镜

## 📚 更多资源

- 🌐 官网: https://www.tensorslab.com/
- 📖 文档: https://github.com/miyakooy/vison-skills/blob/main/README.md
- 🔧 API 文档: https://github.com/miyakooy/vison-skills/tree/main/docs
- 🐛 问题反馈: https://github.com/miyakooy/vison-skills/issues

## 🤝 欢迎试用和反馈

欢迎大家试用和反馈！💬

如果你在使用过程中遇到任何问题或有功能建议，请随时：
- 📝 提交 Issue: https://github.com/miyakooy/vison-skills/issues
- 💬 参与讨论: https://github.com/miyakooy/vison-skills/discussions
- 📧 联系邮箱: mia@tensorslab.com

## ⭐ 如果这个项目对你有帮助

请给个 Star！🌟

---

**🔗 链接**
- GitHub: https://github.com/miyakooy/vison-skills
- npm: https://www.npmjs.com/package/@tensorlab/openclaw-skills
- License: MIT

**Made with ❤️ by TensorsLab**

---

## 📮 联系方式

- 🌐 官网: https://www.tensorslab.com/
- 💬 GitHub: https://github.com/miyakooy/vison-skills
- 📧 邮箱: mia@tensorslab.com
- 🐛 问题反馈: https://github.com/miyakooy/vison-skills/issues

---

## 📄 许可证

MIT License

---

## 🙏 致谢

感谢所有贡献者和使用者！

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个 Star！**

Made with ❤️ by [TensorsLab](https://www.tensorslab.com/)

</div>
