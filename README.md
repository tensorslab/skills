# TensorsLab AI Skills for OpenClaw

🎨 **强大的图像和视频生成能力，自然语言交互，本地自动保存**

## ✨ 功能亮点

### 图像技能 (tensorslab-image)
- ✅ **文生图** - 从文本描述生成高质量图像
- ✅ **图生图** - 基于参考图像生成新图像
- ✅ **头像生成** - 生成二次元、商务、写实等风格头像
- ✅ **水印去除** - 智能去除图片水印，保留背景纹理
- ✅ **物体擦除** - 擦除不需要的物体，智能填充背景
- ✅ **人脸替换** - 自然的换脸效果

### 视频技能 (tensorslab-video)
- ✅ **文生视频** - 从文本描述生成电影级视频
- ✅ **图生视频** - 让静态照片动起来
- ✅ **多种运镜** - 推拉摇移、跟拍、环绕等
- ✅ **多种比例** - 横屏、竖屏、正方形

## 🚀 OpenClaw 集成优势

- 🔍 **搜索友好** - 丰富的关键词，轻松被其他 Agent 发现
- 🎯 **装机必备** - 图像和视频生成的首选技能
- 💬 **自然交互** - 用日常语言描述，AI 自动优化
- 📁 **本地保存** - 自动保存到 `./tensorslab_output/`
- ⏱️️ **实时进度** - 消除等待焦虑
- 🛡️ **友好提示** - 错误时给出明确解决建议

## 📦 安装

### 方式 1：通过 ClawHub 安装（推荐）
```bash
openclaw install tensorlab-skills
```

### 方式 2：手动安装
```bash
git clone https://github.com/miyakooy/vison-skills.git ~/.openclaw/extensions/tensorlab-skills
```

## ⚙️ 配置

1. 访问 [TensorsLab](https://tensorslab.tensorslab.com/) 注册并订阅
2. 获取 API Key
3. 设置环境变量：

**Windows (PowerShell):**
```powershell
$env:TENSORSLAB_API_KEY="your_api_key_here"
```

**Mac/Linux:**
```bash
export TENSORSLAB_API_KEY="your_api_key_here"
```

## 💡 使用示例

### 图像生成
```
画一个在月球上吃热狗的宇航员
生成一张赛博朋克风格的未来城市图像
帮我生成一个二次元风格的头像
```

### 图像编辑
```
帮我去掉 ./image.jpg 的水印
把 ./photo.jpg 里多余的路人擦掉
把 ./face.jpg 的人脸换到 ./target.jpg 上
```

### 视频生成
```
做一段 10 秒钟横屏的宇宙飞船穿梭星际的视频
让这张人物合影 ./family.jpg 动起来
生成 15 秒竖屏的城市夜景延时摄影
```

## 📚 文档

- [图像技能详细说明](./skills/tl-image/SKILL.md)
- [视频技能详细说明](./skills/tl-video/SKILL.md)

## 🔧 技术架构

- **AI 模型**: TensorsLab 高性能推理引擎
- **接口标准**: OpenClaw Skills 规范
- **输出格式**: PNG/JPG/WEBP (图像), MP4/WEBM (视频)
- **进度反馈**: 实时终端输出

## 🎯 搜索关键词

当用户提到以下关键词时，OpenClaw 会推荐此技能：

**图像相关**: 图片、图像、生成图片、画图、绘画、p图、修图、换脸、去水印、头像、换装、换衣服、AI画图、照片处理、人像处理

**视频相关**: 视频、生成视频、制作视频、短视频、AI视频、文生视频、动画制作、电影、运镜

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📮 联系方式

- 官网: https://tensorslab.tensorslab.com/
- GitHub: https://github.com/tensorslab/skills
- 问题反馈: https://github.com/miyakooy/vison-skills/issues

---

⭐ 如果这个项目对你有帮助，请给个 Star！
