# Awesome Computer Vision 列表提交内容

## 列表信息
**仓库**: https://github.com/jbhuang0604/awesome-computer-vision
**Issue 页面**: https://github.com/jbhuang0604/awesome-computer-vision/issues/new

---

## 📝 Issue 内容

### Title
```
[New Tool] TensorsLab Vision Skills - OpenClaw Integration
```

### Description
```
## Tool Name
TensorsLab Vision Skills

## Tool URL
https://github.com/miyakooy/vison-skills

## License
MIT

## Category
- [x] Image Generation
- [x] Image Editing
- [x] Video Generation
- [ ] Object Detection
- [ ] Image Classification
- [ ] Face Recognition
- [ ] Style Transfer
- [ ] Other

## Description
OpenClaw 集成 TensorsLab AI 模型，提供强大的图像和视频生成能力。

## Key Features

### Image Skills (tensorslab-image)
- **Text-to-Image**: Generate high-quality images from text descriptions
- **Image-to-Image**: Generate new images based on reference images
- **Multi-image Synthesis**: Merge multiple images with stylized rendering
- **Avatar Generation**: Generate avatars in anime, business, realistic styles
- **Watermark Removal**: Intelligently remove watermarks while preserving texture
- **Object Erasure**: Remove unwanted objects with smart background fill
- **Face Replacement**: Natural face swapping effects
- **General Editing**: Modify colors, add objects, change styles

### Video Skills (tensorslab-video)
- **Text-to-Video**: Generate cinematic videos from text descriptions
- **Image-to-Video**: Animate static photos
- **Multiple Camera Moves**: Dolly, pan, tilt, track, orbit
- **Multiple Aspect Ratios**: Landscape (16:9), Portrait (9:16), Square (1:1)

## OpenClaw Integration

- **🔍 Search-friendly**: Rich multilingual keywords for easy discovery by other agents
- **💬 Natural Interaction**: Describe in everyday language, AI optimizes automatically
- **📁 Local Storage**: Auto-save to `./tensorslab_output/`
- **⏱️ Real-time Progress**: Eliminate wait anxiety with live feedback
- **🛡️ Friendly Prompts**: Clear solution suggestions on errors
- **🌐 Cross-Platform**: Support for Windows, macOS, Linux

## Installation

### Via ClawHub (Recommended)
```bash
openclaw install tensorlab-skills
```

### Manual Installation
```bash
git clone https://github.com/miyakooy/vison-skills.git ~/.openclaw/extensions/tensorlab-skills
```

### Via npm
```bash
npm install -g @tensorlab/openclaw-skills
```

## Quick Start

### Image Generation
```bash
# Text-to-Image
"画一个在月球上吃热狗的宇航员"

# Generate avatar
"帮我生成一个二次元风格的头像"

# Remove watermark
"帮我去掉 ./image.jpg 的水印"

# Face swap
"把 ./face.jpg 的人脸换到 ./target.jpg 上"
```

### Video Generation
```bash
# Text-to-Video
"做一段 10 秒钟横屏的宇宙飞船穿梭星际的视频"

# Image-to-Video
"让这张人物合影 ./family.jpg 动起来"
```

## Links

- **Documentation**: https://github.com/miyakooy/vison-skills/blob/main/README.md
- **npm Package**: @tensorlab/openclaw-skills
- **Official Website**: https://www.tensorslab.com/

## Search Keywords

**Image-related:**
image, picture, generate image, draw, paint, photo edit, retouch,
face swap, remove watermark, avatar, outfit swap, AI art, portrait,
图片, 图像, 生成图片, 画图, 绘画, p图, 修图,
换脸, 去水印, 头像, 换装, 换衣服

**Video-related:**
video, generate video, make video, short video, AI video,
text-to-video, image-to-video, animation, movie, camera moves,
视频, 生成视频, 制作视频, 短视频, AI视频,
文生视频, 图生视频, 动画制作, 电影, 运镜

## Tags

openclaw, tensorlab, ai, computer-vision, image-generation,
video-generation, text-to-image, text-to-video, image-to-video,
avatar, watermark-removal, face-replacement, object-erasure
```

---

## 📋 操作步骤

### 1. 打开 Issue 页面
访问：https://github.com/jbhuang0604/awesome-computer-vision/issues/new

### 2. 填写 Title
复制并粘贴：
```
[New Tool] TensorsLab Vision Skills - OpenClaw Integration
```

### 3. 填写 Description
打开这个文件：`docs/AWESOME_COMPUTER_VISION.md`
复制从 `## Tool Name` 开始的所有内容

### 4. 提交
点击 **"Submit new issue"** 按钮

---

## ⏱️ 预计时间

**提交时间**: 3-5 分钟
**审核时间**: 通常 1-7 天

---

## ✅ 完成后

告诉我提交成功，我们继续第三步：**发布到 npm**！🚀
