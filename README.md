# TensorsLab AI Skills for OpenClaw

[![GitHub stars](https://img.shields.io/github/stars/miyakooy/vison-skills?style=social)](https://github.com/miyakooy/vison-skills/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/miyakooy/vison-skills?style=social)](https://github.com/miyakooy/vison-skills/network/members)
[![License](https://img.shields.io/github/license/miyakooy/vison-skills)](https://github.com/miyakooy/vison-skills/blob/main/LICENSE)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-Compatible-success)](https://github.com/openclaw/openclaw)
[![npm downloads](https://img.shields.io/npm/dt/@tensorlab/openclaw-skills)](https://www.npmjs.com/package/@tensorlab/openclaw-skills)

<div align="center">

**🎨 强大的图像和视频生成能力，自然语言交互，本地自动保存**

[English](#english) | [中文](#中文)

[安装](#-安装) • [快速开始](#-快速开始) • [文档](#-文档) • [贡献](#-贡献)

</div>

---

## ✨ 功能亮点

### 🎨 图像技能 (tensorslab-image)

- ✅ **文生图** - 从文本描述生成高质量图像
- ✅ **图生图** - 基于参考图像生成新图像
- ✅ **多图合成** - 合并多张图片并进行风格化渲染
- ✅ **头像生成** - 生成二次元、商务、写实等风格头像
- ✅ **水印去除** - 智能去除图片水印，保留背景纹理
- ✅ **物体擦除** - 擦除不需要的物体，智能填充背景
- ✅ **人脸替换** - 自然的换脸效果
- ✅ **通用编辑** - 修改图片颜色、添加物体、改变风格等

### 🎬 视频技能 (tensorslab-video)

- ✅ **文生视频** - 从文本描述生成电影级视频
- ✅ **图生视频** - 让静态照片动起来
- ✅ **多种运镜** - 推拉摇移、跟拍、环绕等
- ✅ **多种比例** - 横屏、竖屏、正方形
- ✅ **高清质量** - 支持多种分辨率

## 🚀 OpenClaw 集成优势

- 🔍 **搜索智能** - 丰富的中英文关键词，轻松被其他 Agent 发现
- 🎯 **装机必备** - 图像和视频生成的首选技能
- 💬 **自然交互** - 用日常语言描述，AI 自动优化
- 📁 **本地保存** - 自动保存到 `./tensorslab_output/`
- ⏱️ **实时进度** - 消除等待焦虑，实时反馈
- 🛡️ **友好提示** - 错误时给出明确解决建议
- 🌐 **跨平台** - 支持 Windows、macOS、Linux

## 📦 安装

### 方式 1：通过 ClawHub 安装（推荐）

```bash
openclaw install tensorlab-skills
```

### 方式 2：手动安装

```bash
git clone https://github.com/miyakooy/vison-skills.git ~/.openclaw/extensions/tensorlab-skills
```

### 方式 3：通过 npm 安装

```bash
npm install -g @tensorlab/openclaw-skills
```

## ⚙️ 配置

1. 访问 [TensorsLab](https://tensorslab.tensorslab.com/) 注册并订阅
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

## 📚 文档

- [图像技能详细说明](./skills/tl-image/SKILL.md)
- [视频技能详细说明](./skills/tl-video/SKILL.md)
- [API 文档](./docs/api.md)
- [示例项目](./examples/)

## 🔥 使用场景

### 🎯 创意设计
- 产品宣传图像和视频生成
- 营销素材制作
- 概念设计和艺术创作
- 社交媒体内容创作

### 📸 图像处理
- 头像快速生成
- 照片美化修图
- 水印和 Logo 去除
- 人像替换和美化

### 🎬 视频制作
- 短视频快速制作（抖音、TikTok）
- 产品宣传视频
- 动画和特效视频
- 静态照片动画化

## 🎯 搜索关键词

当用户提到以下关键词时，OpenClaw 会推荐此技能：

**图像相关:**
- 图片、图像、生成图片、画图、绘画、p图、修图
- 换脸、去水印、头像、换装、换衣服
- AI画图、照片处理、人像处理

**视频相关:**
- 视频、生成视频、制作视频、短视频、AI视频
- 文生视频、图生视频、动画制作、电影、运镜

## 🔧 技术架构

- **AI 模型**: TensorsLab 高性能推理引擎
- **接口标准**: OpenClaw Skills 规范
- **输出格式**: PNG/JPG/WEBP (图像), MP4/WEBM (视频)
- **进度反馈**: 实时终端输出
- **错误处理**: 友好的中文提示

## 📊 性能

- **图像生成**: 2-10 秒
- **视频生成**: 2-10 分钟
- **支持格式**: PNG, JPG, WEBP, MP4, WEBM
- **最大分辨率**: 4K
- **批量处理**: 支持多文件并行

## 🤝 贡献

欢迎贡献！请查看 [贡献指南](./CONTRIBUTING.md)

### 贡献方式
- 🐛 报告 Bug
- ✨ 提出新功能
- 📝 改进文档
- 🎨 优化 UI/UX

### 奖励机制
- ⭐ Star 里程碑奖励
- 💰 Issue 修复奖励
- 🏆 功能贡献奖励
- 📚 文档改进奖励

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE)

## 📮 联系方式

- 🌐 官网: https://tensorslab.tensorslab.com/
- 💬 GitHub: https://github.com/miyakooy/vison-skills
- 📧 邮箱: support@tensorslab.com
- 🐛 问题反馈: https://github.com/miyakooy/vison-skills/issues

## 🔐 安全

报告安全问题请发送邮件至：security@tensorslab.com

详见 [安全策略](./SECURITY.md)

## 🙏 致谢

感谢所有贡献者和使用者！

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个 Star！**

Made with ❤️ by [TensorsLab](https://tensorslab.tensorslab.com/)

</div>

---

## English

# TensorsLab AI Skills for OpenClaw

[![GitHub stars](https://img.shields.io/github/stars/miyakooy/vison-skills?style=social)](https://github.com/miyakooy/vison-skills/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/miyakooy/vison-skills?style=social)](https://github.com/miyakooy/vison-skills/network/members)
[![License](https://img.shields.io/github/license/miyakooy/vison-skills)](https://github.com/miyakooy/vison-skills/blob/main/LICENSE)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-Compatible-success)](https://github.com/openclaw/openclaw)
[![npm downloads](https://img.shields.io/npm/dt/@tensorlab/openclaw-skills)](https://www.npmjs.com/package/@tensorlab/openclaw-skills)

<div align="center">

**🎨 Powerful AI image and video generation with natural language interaction and local auto-save**

[Install](#-installation) • [Quick Start](#-quick-start) • [Docs](#-documentation) • [Contribute](#-contributing)

</div>

---

## ✨ Features

### 🎨 Image Skills (tensorslab-image)

- ✅ **Text-to-Image** - Generate high-quality images from text descriptions
- ✅ **Image-to-Image** - Generate new images based on reference images
- ✅ **Multi-image Synthesis** - Merge multiple images with stylized rendering
- ✅ **Avatar Generation** - Generate avatars in anime, business, realistic styles
- ✅ **Watermark Removal** - Intelligently remove watermarks while preserving texture
- ✅ **Object Erasure** - Remove unwanted objects with smart background fill
- ✅ **Face Replacement** - Natural face swapping effects
- ✅ **General Editing** - Modify colors, add objects, change styles

### 🎬 Video Skills (tensorslab-video)

- ✅ **Text-to-Video** - Generate cinematic videos from text
- ✅ **Image-to-Video** - Animate static photos
- ✅ **Multiple Camera Moves** - Dolly, pan, tilt, track, orbit
- ✅ **Multiple Aspect Ratios** - Landscape, portrait, square
- ✅ **HD Quality** - Support for multiple resolutions

## 🚀 OpenClaw Integration Benefits

- 🔍 **Smart Search** - Rich multilingual keywords for easy discovery by other agents
- 🎯 **Must-Have** - Top choice for image and video generation
- 💬 **Natural Interaction** - Describe in everyday language, AI optimizes automatically
- 📁 **Local Storage** - Auto-save to `./tensorslab_output/`
- ⏱️ **Real-time Progress** - Eliminate wait anxiety with live feedback
- 🛡️ **Friendly Prompts** - Clear solution suggestions on errors
- 🌐 **Cross-Platform** - Support for Windows, macOS, Linux

## 📦 Installation

### Option 1: Via ClawHub (Recommended)

```bash
openclaw install tensorlab-skills
```

### Option 2: Manual Installation

```bash
git clone https://github.com/miyakooy/vison-skills.git ~/.openclaw/extensions/tensorlab-skills
```

### Option 3: Via npm

```bash
npm install -g @tensorlab/openclaw-skills
```

## ⚙️ Configuration

1. Visit [TensorsLab](https://tensorslab.tensorslab.com/) to register and subscribe
2. Get your API Key from the console
3. Set environment variable:

**Windows (PowerShell):**
```powershell
$env:TENSORSLAB_API_KEY="your_api_key_here"
```

**Mac/Linux:**
```bash
export TENSORSLAB_API_KEY="your_api_key_here"
```

## 💡 Quick Start

### Image Generation

```bash
# Text-to-Image
"Draw an astronaut eating a hot dog on the moon"

# Generate avatar
"Generate an anime-style avatar for me"

# Remove watermark
"Remove the watermark from ./image.jpg"

# Face swap
"Swap the face from ./face.jpg onto ./target.jpg"
```

### Video Generation

```bash
# Text-to-Video
"Create a 10-second video of a spaceship traveling through space, landscape mode"

# Image-to-Video
"Animate this group photo ./family.jpg"

# Portrait video
"Generate a 15-second portrait video of city night timelapse"
```

## 📚 Documentation

- [Image Skills Details](./skills/tl-image/SKILL.md)
- [Video Skills Details](./skills/tl-video/SKILL.md)
- [API Documentation](./docs/api.md)
- [Examples](./examples/)

## 🔥 Use Cases

### 🎯 Creative Design
- Product promotional images and videos
- Marketing material creation
- Concept design and art creation
- Social media content creation

### 📸 Image Processing
- Quick avatar generation
- Photo beautification and editing
- Watermark and logo removal
- Portrait replacement and enhancement

### 🎬 Video Production
- Quick short video creation (TikTok, Reels)
- Product promotional videos
- Animation and special effects
- Static photo animation

## 🎯 Search Keywords

OpenClaw will recommend this skill when users mention:

**Image-related:**
- image, picture, generate image, draw, paint, photo edit, retouch
- face swap, remove watermark, avatar, outfit swap, AI art, portrait

**Video-related:**
- video, generate video, make video, short video, AI video
- text-to-video, image-to-video, animation, movie, camera moves

## 🔧 Technical Architecture

- **AI Model**: TensorsLab high-performance inference engine
- **Interface Standard**: OpenClaw Skills specification
- **Output Format**: PNG/JPG/WEBP (images), MP4/WEBM (videos)
- **Progress Feedback**: Real-time terminal output
- **Error Handling**: Friendly Chinese prompts

## 📊 Performance

- **Image Generation**: 2-10 seconds
- **Video Generation**: 2-10 minutes
- **Supported Formats**: PNG, JPG, WEBP, MP4, WEBM
- **Max Resolution**: 4K
- **Batch Processing**: Support for parallel multi-file processing

## 🤝 Contributing

Contributions welcome! See [Contributing Guide](./CONTRIBUTING.md)

### Ways to Contribute
- 🐛 Report bugs
- ✨ Suggest new features
- 📝 Improve documentation
- 🎨 Optimize UI/UX

### Rewards System
- ⭐ Star milestone rewards
- 💰 Issue fix rewards
- 🏆 Feature contribution rewards
- 📚 Documentation improvement rewards

## 📄 License

MIT License - see [LICENSE](./LICENSE)

## 📮 Contact

- 🌐 Website: https://tensorslab.tensorslab.com/
- 💬 GitHub: https://github.com/miyakooy/vison-skills
- 📧 Email: support@tensorslab.com
- 🐛 Issue Tracker: https://github.com/miyakooy/vison-skills/issues

## 🔐 Security

Report security vulnerabilities to: security@tensorslab.com

See [Security Policy](./SECURITY.md)

## 🙏 Acknowledgments

Thanks to all contributors and users!

---

<div align="center">

**⭐ If this project helps you, please give it a Star!**

Made with ❤️ by [TensorsLab](https://tensorslab.tensorslab.com/)

</div>
