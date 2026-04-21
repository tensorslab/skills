---
name: tl-image
description: "Generate and edit images using TensorsLab's AI models. Supports text-to-image, image-to-image generation, plus advanced editing: avatar generation, watermark removal, object erasure, face replacement, and general image editing. Features automatic prompt enhancement, progress tracking, and local file saving. Requires browser-based authorization before first use."
---

# TensorsLab Image Generation

## Overview

This skill enables AI-powered image generation through TensorsLab's API, supporting both text-to-image and image-to-image workflows. The agent enhances user prompts with detailed visual descriptions before calling the API, ensuring high-quality outputs.

## Script Path

The Python scripts for this skill are located in the `scripts/` subdirectory relative to this SKILL.md file. **Always use the absolute path when executing scripts.** Determine the absolute path based on where this skill is installed.

For example, if this SKILL.md is at `/path/to/skills/tl-image/SKILL.md`, then:
- Auth script: `python "/path/to/skills/tl-image/scripts/tensorslab_auth.py"`
- Image script: `python "/path/to/skills/tl-image/scripts/tensorslab_image.py"`

When executing, construct the command using the resolved absolute path:
```bash
python "<absolute_path_to_skill_dir>/scripts/tensorslab_image.py" <args>
```

## Authorization

**BEFORE any image generation, you must ensure you are authorized with TensorsLab.**

### 1. Automatic Authorization
The authorization script will automatically check if an API key already exists in the `TENSORSLAB_API_KEY` environment variable or in `~/.tensorslab/.env` before proceeding.
*(Note: When you need to verify the environment variable, ONLY check if it exists. NEVER display or print the actual API key value.)*

Run:
```bash
python "<absolute_path_to_skill_dir>/scripts/tensorslab_auth.py"
```
This will open a browser for authorization. Wait for "Authorization Successful!" before proceeding.


After authorization, the API key is stored in `~/.tensorslab/.env` and you don't need to re-authorize unless the key expires.

### 2. Manual Configuration (For Cloud/Headless Environments)
**When the agent or openclaw operates in a cloud environment without a browser, the URL authorization method will also fail.** In this scenario, you must instruct the user to manually acquire their API key and configure it in the cloud environment:
1. Direct the user to get their API Key at [TensorsLab Console](https://tensorai.tensorslab.com/apikey).
2. Set the `TENSORSLAB_API_KEY` environment variable in the cloud environment.

## Models

| Model | Description | Best For |
|-------|-------------|----------|
| **seedreamv5** | Latest enhanced model | General purpose, highest quality |
| **seedreamv4** | Standard model | Fast generation, good quality |
| **zimage** | Alternative model | Specific artistic styles |
| **quickedit** | Image instruction editing | Fast color/style/object editing |

Default: `seedreamv4`

## Workflow

For additional scenarios beyond basic generation (avatar generation, watermark removal, object erasure, face replacement), see [references/scenarios.md](references/scenarios.md).

### 1. Text-to-Image Generation

User request: "画一个在月球上吃热狗的宇航员"

**Constraints:**
- Do NOT pass `sourceImage` or `imageUrl` for text-to-image generation.

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
- `imageUrl`: URL of source image (Must be a standard HTTP/HTTPS URL. Do NOT use local paths like /tmp/xxx.png here)
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

> **依赖**：脚本需要 `requests` 和 `pyyaml` 库，首次使用前执行：
> ```bash
> pip install requests pyyaml
> ```

Execute the Python script directly:

```bash
# Text-to-image
python "<absolute_path_to_skill_dir>/scripts/tensorslab_image.py" "a cat on the moon"

# With specific resolution
python "<absolute_path_to_skill_dir>/scripts/tensorslab_image.py" "sunset over mountains" --resolution 16:9

# Image-to-image with local file
python "<absolute_path_to_skill_dir>/scripts/tensorslab_image.py" "watercolor style" --source cat.png

# Image-to-image with URL
python "<absolute_path_to_skill_dir>/scripts/tensorslab_image.py" "watercolor style" --image-url https://example.com/cat.jpg

# Specify model
python "<absolute_path_to_skill_dir>/scripts/tensorslab_image.py" "cyberpunk city" --model seedreamv5

# Custom output directory
python "<absolute_path_to_skill_dir>/scripts/tensorslab_image.py" "a beautiful landscape" --output-dir ./my_images

# Quick editing (Fast instructions)
python "<absolute_path_to_skill_dir>/scripts/tensorslab_image.py" "把主体改为蓝色" --source image.png --model quickedit
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

**URL mapping**: The script also saves file-to-URL mappings in `./tensorslab_output/urls.yaml`. This file tracks the original URLs for each downloaded file and accumulates entries across multiple runs. When you need the original URL of a generated image, read this file.

```yaml
# Example urls.yaml content
abcd_1234567890_0.png: https://tensorai.tensorslab.com/images/abcd_1234567890_0.png
abcd_1234567890_1.png: https://tensorai.tensorslab.com/images/abcd_1234567890_1.png
```

After completion, the script outputs both the local file path and the remote URL. Inform user with both:
```
🎉 您的图片处理完毕！
   - File: ./tensorslab_output/{filename}
   - URL: {remote_url}
```

## Resources

- **scripts/tensorslab_image.py**: Main API client with full CLI support
- **references/api_reference.md**: Detailed API documentation
- **references/scenarios.md**: Advanced usage scenarios (avatar generation, watermark removal, object erasure, face replacement)

