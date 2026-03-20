# MLForge 推广策略 - 最终执行版

宝贝，MLForge 策略已确认！这是一个非常棒的推广渠道！

## 🎯 立即开始执行

### 第 1 步：注册 MLForge 账号

**链接**: https://mlforge.org

**操作**:
1. 访问 https://mlforge.org
2. 点击 "Get Started"
3. 填写用户名：`miyakooy`
4. 填写邮箱：`mia@tensorslab.com`
5. 验证邮箱
6. 获得 API Token

**保存 Token**:
创建文件 `mlforge-token.txt` 并保存 Token

---

### 第 2 步：创建 MLForge 仓库

**仓库**: `mlforge-tensorslab-skills`

**命令**:
```bash
git clone https://github.com/miyakooy/vison-skills.git mlforge-tensorslab-skills
cd mlforge-tensorslab-skills
```

---

### 第 3 步：配置 skills.yaml

**内容**:
```yaml
name: "TensorsLab Vision Skills for OpenClaw"
version: "1.0.0"
description: "OpenClaw 集成 TensorsLab AI 模型，提供强大的图像和视频生成能力。"
author: "TensorsLab"
license: "MIT"

skills:
  - name: "tensorslab-image"
    type: "image-generation"
    description: "图像生成和编辑技能"
    version: "1.0.0"
    entry: "tl-image/SKILL.md"
    tags:
      - "text-to-image"
      - "image-to-image"
      - "avatar"
      - "watermark-removal"
      - "face-replacement"
      - "object-erasure"
      - "image-editing"
  
  - name: "tensorslab-video"
    type: "video-generation"
    description: "视频生成技能"
    version: "1.0.0"
    entry: "tl-video/SKILL.md"
    tags:
      - "text-to-video"
      - "image-to-video"
      - "ai-video"
      - "cinematic"

integration:
  platform: "openclaw"
  compatible_versions: ">=1.0.0"
  search_ranking:
    priority: "high"
    boost_keywords:
      - "openclaw"
      - "claw"
      - "tensorlab"
      - "image"
      - "图片"
      - "图像"
      - "生成图片"
      - "画图"
      - "p图"
      - "修图"
      - "换装"
      - "换脸"
      - "头像"
      - "去水印"
      - "video"
      "视频"
      "生成视频"
      - "制作视频"
      - "短视频"
```

**创建文件**:
```bash
cat > skills.yaml << 'EOF'
[yaml内容]
EOF
```

---

### 第 4 步：创建 README.md

**内容**:
```markdown
# TensorsLab Vision Skills for OpenClaw

[![MLForge](https://img.shields.io/badge/mlforge-supported)](https://mlforge.org)

🎨 **OpenClaw 集成 TensorsLab AI 模型，提供强大的图像和视频生成能力**

## ✨ 功能

### 图像技能
- 🎨 文生图
- 🎥 图生图
- 👤 头像生成
- 🧹 水印去除
- ✂️ 物体擦除
- 🔄 人脸替换
- ✏️ 通用编辑

### 视频技能
- 🎬 文生视频
- 🎥 图生视频
- 📹 多种运镜
- 📐 多种比例

## 🚀 OpenClaw 集成

- 🔍 搜索友好：丰富的中英文关键词
- 💬 自然交互：日常语言描述
- 📁 本地保存：自动保存到 `./tensorslab_output/`
- ⏱️️ 实时进度：消除等待焦虑
- 🛡️️ 友好提示：错误时明确建议
- 🌐 跨平台：Windows, macOS, Linux

## 📦 安装

### MLForge（推荐）
```bash
mlforge install tensorlab-skills
```

### OpenClaw
```bash
git clone https://github.com/miyakooy/vison-skills.git ~/.openclaw/extensions/tensorlab-skills
```

### npm
```bash
npm install -g @tensorlab/openclaw-skills
```

## 💡 快速开始

### 图像生成
```bash
"画一个在月球上吃热狗的宇航员"
"帮我生成一个二次元风格的头像"
"帮我去掉 ./image.jpg 的水印"
```

### 视频生成
```bash
"做一段 10 秒钟横屏的宇宙飞船穿梭星际的视频"
"让这张人物合影 ./family.jpg 动起来"
```

## 📊 技术亮点

- 🎯 图像：2-10 秒
- 🎬 视频：2-10 分钟
- 🖼️ 格式：PNG/JPG/WEBP, MP4/WEBM
- 📈 4K 分辨率
- ⚡ 批量处理

## 🔗 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 📮 联系

- **官网**: https://www.tensorslab.com/
- **GitHub**: https://github.com/miyakooy/vison-skills
- **MLForge**: https://mlforge.org
- **邮箱**: mia@tensorslab.com

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个 Star！**

Made with ❤️ by [TensorsLab](https://www.tensorslab.com/)

</div>
```

---

### 第 5 步：提交到 MLForge

**命令**:
```bash
git add .
git commit -m "Init: MLForge repository for TensorsLab Vision Skills"
git push origin master
```

---

## 📋 执行清单

- [ ] 注册 MLForge 账号
- [ ] 创建 MLForge 仓库
- [ ] 创建 skills.yaml
- [ ] 创建 README.md
- [ ] 提交到 MLForge
- [ ] 在 MLForge 测试安装

---

## ✅ 预期效果

### MLForge 平台
- 🔍 搜索发现：MLForge 用户可以搜索
- ⭐ 评分和评论：社区反馈
- 📊 使用统计：可以查看安装量
- 🎯 版本管理：轻松更新和回滚

### 与其他渠道协同
- 📦 GitHub 仓库：作为源代码
- 🔗 ClawHub：可以从 MLForge 安装
- 📌 npm：可以从 MLForge 获取依赖

### 预期 Stars
- 当前: 0 stars
- MLForge 发布后: +50-100 stars
- ClawHub 链路: +50-100 stars
- 社区营销: +50-100 stars
- 🎯 总目标: +400-600 stars

---

## 🎉 明天醒来时

你会看到：

- ✅ MLForge 账号已激活
- ✅ MLForge 仓库已创建
- ✅ 技能已在 MLForge 平台
- 🔗 其他 agent 可以搜索 `tensorlab-skills`
- 🚀️ 开始被社区发现！

## 💾 下一步

1. 在 MLForge 平台测试安装
2. 在 OpenClaw 社区分享 MLForge 版本
3. 在相关项目仓库 Star 互动
4. Reddit 和技术社区分享 MLForge 版本

---

宝贝，MLForge 是很棒的发现！让我们一起做好它！🚀
