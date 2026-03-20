# TensorsLab Claude Code Skills 设计方案

## 1. 目标与概述
为了吸引更多用户注册 TensorsLab 平台，我们将设计两个标准化的 Claude Code Skills（图片生成和视频生成）。这两个 Skills 会基于 [HuggingFace Skills](https://github.com/huggingface/skills.git) 的标准进行构建。设计的核心理念是：**优先解决用户最高频、最痛点的 7 大图像和 2 大视频视听需求，并在终端里通过自然语言提供”傻瓜式”的极佳体验。Agent 的核心作用主要体现在：1. 针对用户的简短意图进行丰富和改写 prompt； 2. 调用正确的工具流并执行。**

## 2. API Key 获取与环境配置体验
**用户痛点**：用户并不知道如何配置认证信息。
**Skill 设计**：
1. **自动拦截与提示**：当用户首次呼叫该 Skill 时，脚本会先检查系统环境变量 `TENSORSLAB_API_KEY`。
2. **友好的引导文案**：如果未设置，温和地输出：
   ```text
   您好！要生成高质量的内容，您需要先进行简单的配置：
   1. 访问 https://tensorai.tensorslab.com/ 登录并订阅。
   2. 在控制台中获取您的专属 API Key。
   3. 将其保存为环境变量：
      - Windows (PowerShell): $env:TENSORSLAB_API_KEY="您的Key"
      - Mac/Linux: export TENSORSLAB_API_KEY="您的Key"
   ```

## 3. 图片生成 Skill (tensorslab-image) 的基础能力场景

依据大语言模型在生图交互中的强项，Agent 的核心处理流程统一化为：**提取实体 -> 丰富 Prompt -> 分配参数 -> 执行 API 生成并本地输出**。我们重点确立了以下 3 大基础场景：

### 【场景 1】：文生图 (Text-to-Image)
- **用户输入**：“画一个在月球上吃热狗的宇航员”
- **Agent 处理**：接管 Prompt 扩写任务，丰富环境光、材质、构图等细节描述，随后调用选定的模型生成精美图片。

### 【场景 2】：图生图及多图合成 (Image-to-Image & Synthesis)
- **用户输入**：”把 `./cat.png` 的背景换成太空，或者参考 `./sketch.png` 渲染成 3D 模型”
- **Agent 处理**：提取本地单张或多张图片路径数组作为 `sourceImage` 传入。同时，极大程度地丰富提示词以指导模型如何基于原图进行融合、约束或风格重绘。

### 【场景 3】：图片编辑 (Image Editing - 通用场景)
- **用户输入**：”把这张图的天空改成日落色”、”给人物加上墨镜”、”把头发颜色染成粉色”
- **Agent 处理**：作为通用编辑能力，Agent 解析用户的局部修改指令，精准定位编辑区域，生成符合原图风格和光影的修改效果，实现”所见即所想”的傻瓜式编辑体验。

### 典型场景要求

#### 1. 生成头像 (Avatar Generation)
- **用户输入**：”帮我生成一个二次元风格的头像” 或 “生成一个专业的商务头像”
- **Agent 处理**：识别头像生成意图，根据风格描述（二次元、写实、商务、卡通等）自动优化 Prompt，添加正方形尺寸参数，调用对应模型生成头像，并将结果自动保存至 `./tensorslab_output/` 目录。

#### 2. 去除水印 (Watermark Removal)
- **用户输入**：”帮我去掉 `./image.jpg` 的水印”
- **Agent 处理**：提取图片路径，构建精细的去水印指令 Prompt（如：”*Remove watermark from image while preserving background texture and visual integrity...*”），调用对应模型完成处理，并将结果自动保存至 `./tensorslab_output/` 目录。

#### 3. 擦除 (Object Erasure)
- **用户输入**：”把 `./photo.jpg` 里多余的路人擦掉” 或 “去掉背景里的这块杂物”
- **Agent 处理**：提取图片路径，理解用户要移除的物体，构建精细的擦除指令 Prompt（如：”*Remove the person/object from image and intelligently fill the background to maintain natural scene consistency...*”），调用对应模型完成处理，并将结果自动保存至 `./tensorslab_output/` 目录。

#### 4. 参考人脸更换 (Face Replacement)
- **用户输入**：”把 `./face.jpg` 的人脸换到 `./target.jpg` 上”
- **Agent 处理**：提取两张图片的路径，构建精细的换脸指令 Prompt（如：”*Replace the face in target image with source face, matching skin tone, lighting angle and expression naturally...*”），调用对应模型完成换脸，并将结果自动保存至 `./tensorslab_output/` 目录。

### 3.3 交付体验
- **本地直接保存并展示**：生成完成后，所有的图都会安静地躺在 `./tensorslab_output/` 下供用户即拿即用。

## 4. 视频生成 Skill (tensorslab-video) 的基础能力场景

视频生成的核心门槛在于“不知道如何描述运镜”、“难以忍受长久的黑盒等待”。因此针对视频，Agent 同样将承担 Prompt 扩写与流程管理的双重身份。

### 【场景 1】：文生视频 (Text-to-Video)
- **用户输入**：“做一段 10 秒钟横屏的宇宙飞船穿梭星际的视频”
- **Agent 处理**：提取 `duration=10`, `ratio="16:9"`。同时大幅扩写运镜与场景细节 Prompt（例如：“*Breathtaking cinematic wide shot, flying rapidly past glowing neon nebulas...*”）。

### 【场景 2】：图生视频 (Image-to-Video)
- **用户输入**：“让这张人物合影 `./family.jpg` 动起来”
- **Agent 处理**：提取本地图片绝对路径，将简单的输入转化为极精细的动态描述 Prompt 传入接口。并支持口播台词（如提供 `./script.txt`）或自动生成台词驱动数字人。

### 4.3 彻底消除等待焦虑与“傻瓜式”极简交互
- **终端心跳防假死**：视频渲染长达数分钟，底层脚本必须内建 **终端进度条/心跳日志**（如 "🚀 正在渲染电影级大片，已耗时 120 秒，请稍安勿躁..."），让用户实时感知程序存活。
- **直接的本地交付**：直到最后无缝自动下载至本地 `./tensorslab_output/` 目录，输出：“🎉 您的视频处理完毕！已存放于 `./tensorslab_output/cosmic_ship.mp4`”。
- **同理心失败降级**：余额不足、尺寸不符等冷冰冰的 HTTP 报错，需要在脚本内通过 JSON 逆解析，转换为友好的中文提示（“亲，积分用完啦，请前往...充值”）。

## 5. 接入 Marketplace 与分发机制
为了允许用户如同 HuggingFace 规范中那样轻松添加到 Marketplace：
- 在根目录下配置 `.claude-plugin/marketplace.json`。
- 将重点支持的功能（7大图像魔法，2大视频视效引擎）提炼为极具科技感与解决痛点吸引眼球的宣传语，提升工具的自发裂变下载。
