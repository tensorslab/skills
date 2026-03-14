---
name: tensorslab-image
description: "Generate and edit images using TensorsLab's AI models. Supports text-to-image, image-to-image generation, plus advanced editing: avatar generation, watermark removal, object erasure, face replacement, and general image editing. Features automatic prompt enhancement, progress tracking, and local file saving. Requires TENSORSLAB_API_KEY environment variable."
---

# TensorsLab Image Generation

## Overview

This skill enables AI-powered image generation through TensorsLab's API, supporting both text-to-image and image-to-image workflows. The agent enhances user prompts with detailed visual descriptions before calling the API, ensuring high-quality outputs.

## Authentication Check

Before any image generation, verify the API key is configured:

```bash
# 仅检查变量是否存在，不输出完整值
[ -n "$TENSORSLAB_API_KEY" ] && echo "✅ API key is set" || echo "❌ TENSORSLAB_API_KEY is not set"
```

If not set, display this friendly message:

```
您好！要生成高质量的内容，您需要先进行简单的配置：
1. 访问 https://tensorai.tensorslab.com/ 登录并订阅。
2. 在控制台中获取您的专属 API Key。
3. 将其保存为环境变量：
   - Windows (PowerShell): $env:TENSORSLAB_API_KEY="您的Key"
   - Mac/Linux: export TENSORSLAB_API_KEY="您的Key"
```

## Models

| Model | Description | Best For |
|-------|-------------|----------|
| **seedreamv45** | Latest enhanced model | General purpose, highest quality |
| **seedreamv4** | Standard model | Fast generation, good quality |
| **zimage** | Alternative model | Specific artistic styles |

Default: `seedreamv4`

## Workflow

For additional scenarios beyond basic generation (avatar generation, watermark removal, object erasure, face replacement), see [references/scenarios.md](references/scenarios.md).

### 1. Text-to-Image Generation

User request: "画一个在月球上吃热狗的宇航员"

**Agent processing:**
1. Extract the core subject and action
2. Enhance prompt with details (lighting, composition, style, atmosphere)
3. Call API with enriched prompt
4. Monitor progress with heartbeat updates
5. Download to `./tensorslab_output/`

**Example enhanced prompt:**
```
An astronaut sitting on the lunar surface, eating a hot dog with mustard,
cinematic lighting, Earth visible in the background, highly detailed,
photorealistic, 8k quality, dramatic shadows from the low sun angle
```

### 2. Image-to-Image Generation

User request: "把 cat.png 的背景换成太空" or "参考 sketch.png 渲染成 3D 模型"

**Agent processing:**
1. Extract image file paths (absolute or relative to current directory)
2. Enhance prompt with transformation instructions
3. Upload source images with prompt
4. Monitor and download results

**Parameters for image-to-image:**
- `sourceImage`: Array of image files (for local upload)
- `imageUrl`: URL of source image
- `prompt`: Description of desired transformation

### 3. Image Editing (General Purpose)

General-purpose editing for any local image modifications.

**User request examples:**
- "把这张图的天空改成日落色"
- "给人物加上墨镜"
- "把头发颜色染成粉色"

**Agent processing:**
1. Extract image file path
2. Parse the specific editing instruction (what to change, where)
3. Build enhanced prompt with precise editing guidance
4. Call API with source image and editing prompt
5. Save result to `./tensorslab_output/`

**Example enhanced prompt:**
```
Change the sky to sunset colors with warm orange and pink gradients,
matching the existing lighting conditions and atmospheric perspective,
seamless blend at the horizon line
```

For avatar generation, watermark removal, object erasure, and face replacement scenarios, see [references/scenarios.md](references/scenarios.md).

### 4. Resolution Options

Supported formats:
- **Aspect ratios**: `9:16`, `16:9`, `3:4`, `4:3`, `1:1`, `2:3`, `3:2`
- **Resolution levels**: `2K`, `4K`
- **Specific dimensions**: `WxH` format (e.g., `2048x2048`, `1920x1080`)
  - Constraint: Total pixels must be between 3,686,400 and 16,777,216


## Using the Script

> **依赖**：脚本需要 `requests` 库，首次使用前执行：
> ```bash
> pip install requests
> ```

Execute the Python script directly:

```bash
# Text-to-image
python scripts/tensorslab_image.py "a cat on the moon"

# With specific resolution
python scripts/tensorslab_image.py "sunset over mountains" --resolution 16:9

# Image-to-image
python scripts/tensorslab_image.py "watercolor style" --source cat.png

# Specify model
python scripts/tensorslab_image.py "cyberpunk city" --model seedreamv45

# Custom output directory
python scripts/tensorslab_image.py "a beautiful landscape" --output-dir ./my_images
```

## Task Status Flow

| Status | Code | Meaning |
|--------|------|---------|
| Queued | 1 | Task waiting in queue |
| Processing | 2 | Currently generating |
| Completed | 3 | Done, images ready |
| Failed | 4 | Error occurred |

## Error Handling

Translate API errors to user-friendly messages:

| Error Code | Meaning | User Message |
|------------|---------|--------------|
| 9000 | Insufficient credits | "亲，积分用完啦，请前往 https://tensorai.tensorslab.com"/ 充值" |
| 9999 | General error | Show the specific error message |

## Output

All images are saved to output directory with naming pattern:
- Default: `./tensorslab_output/` (current working directory)
- Custom: Use `--output-dir` or `-o` to specify a different path
- Naming: `{task_id}_{index}.{ext}` - e.g., `abcd_1234567890_0.png`

After completion, inform user:
```
🎉 您的图片处理完毕！已存放于 ./tensorslab_output/{filename}
```

## Resources

- **scripts/tensorslab_image.py**: Main API client with full CLI support
- **references/api_reference.md**: Detailed API documentation
- **references/scenarios.md**: Advanced usage scenarios (avatar generation, watermark removal, object erasure, face replacement)

