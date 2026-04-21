---
name: tl-video
description: Generate videos using TensorsLab's AI video generation models. Supports text-to-video and image-to-video generation with automatic prompt enhancement, progress tracking, and local file saving. Use for generating videos from text descriptions, animating static images, creating cinematic content, and various aspect ratios. Requires browser-based authorization before first use. Video generation takes several minutes.
---

# TensorsLab Video Generation

## Overview

This skill enables AI-powered video generation through TensorsLab's API, supporting both text-to-video and image-to-video workflows. Video generation is a time-intensive process - tasks typically take several minutes to complete.

## Script Path

The Python scripts for this skill are located in the `scripts/` subdirectory relative to this SKILL.md file. **Always use the absolute path when executing scripts.** Determine the absolute path based on where this skill is installed.

For example, if this SKILL.md is at `/path/to/skills/tl-video/SKILL.md`, then:
- Auth script: `python "/path/to/skills/tl-video/scripts/tensorslab_auth.py"`
- Video script: `python "/path/to/skills/tl-video/scripts/tensorslab_video.py"`

When executing, construct the command using the resolved absolute path:
```bash
python "<absolute_path_to_skill_dir>/scripts/tensorslab_video.py" <args>
```

## Authorization

**BEFORE any video generation, you must ensure you are authorized with TensorsLab.**

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
1. Direct the user to get their API Key at [TensorsLab Console](https://tensorai.tensorslab.com/).
2. Set the `TENSORSLAB_API_KEY` environment variable in the cloud environment.

## Models

| Model | Description | Best For | Max Duration |
|-------|-------------|----------|--------------|
| **seedancev2** | Latest, highest quality | General purpose, cinematic content | 15s |
| **seedancev15pro** | Pro quality | High-end productions | 10s |
| **seedancev1profast** | Fast generation | Quick previews | 10s |
| **seedancev1** | Standard lite | Basic videos | 10s |

Default: `seedancev1profast`

## Workflow

### 1. Text-to-Video Generation

User request: "做一段 10 秒钟横屏的宇宙飞船穿梭星际的视频"

**Constraints:**
- Do NOT pass `sourceImage` or `imageUrl` for text-to-video generation.

**Agent processing:**
1. Extract parameters: `duration=10`, `ratio="16:9"`
2. Enhance prompt with cinematic details, camera movements, scene descriptions
3. Call API with enriched prompt
4. Monitor progress with heartbeat updates (every 60 seconds)
5. Download to `./tensorslab_output/`

**Example enhanced prompt:**
```
Cinematic wide shot of a spaceship rapidly flying through space, passing glowing
nebulae and distant stars, lens flares, dramatic camera movement, epic scale,
movie-quality visual effects, smooth 24fps motion
```

### 2. Image-to-Video Generation

User request: "让这张人物合影 family.jpg 动起来" or "让风景照动起来"

**Agent processing:**
1. Extract image file paths (1-2 images supported)
2. Enhance prompt with motion instructions
3. Monitor progress with heartbeat updates
4. Download results

**Parameters for image-to-video:**
- `sourceImage`: Array of image files (1-2 images max)
- `imageUrl`: Comma-separated URLs of source images (Must be standard HTTP/HTTPS URLs. Do NOT use local paths like /tmp/xxx.png here)
- `prompt`: Description of desired motion/animation

### 3. Resolution and Aspect Ratio

**Aspect ratios:**
- `9:16` - Vertical (TikTok, Reels, Shorts) - **default**
- `16:9` - Horizontal (YouTube, standard video)
- Other ratios available depending on model

**Resolutions:**
- `480p` - SD quality, faster generation
- `720p` - HD quality - **default**
- `1080p` - Full HD
- `1440p` - 2K quality (seedancev2 only)

### 4. Duration Options

- **seedancev2**: 5-15 seconds
- **Other models**: 5-10 seconds

Longer videos take proportionally more time to generate.

### 5. Special Features (seedancev2 only)

| Feature | Parameter | Description |
|---------|-----------|-------------|
| Audio Generation | `generate_audio=1` | Generate soundtrack with video |
| Last Frame | `return_last_frame=1` | Also return final frame as image |

## Progress Tracking

Video generation takes **several minutes**. Keep users informed:

```
⏳ Waiting for video generation to complete...
   (This may take several minutes - please be patient)
🔄 Status: Processing (elapsed: 45s)
🚀 正在渲染电影级大片，已耗时 60 秒，请稍安勿躁...
🚀 正在渲染电影级大片，已耗时 120 秒，请稍安勿躁...
✅ Task completed!
```

**Heartbeat interval:** Print encouraging message every 60 seconds.

## Using the Script

> **依赖**：脚本需要 `requests` 和 `pyyaml` 库，首次使用前执行：
> ```bash
> pip install requests pyyaml
> ```

Execute the Python script directly:

```bash
# Text-to-video (default 5s, vertical 9:16)
python "<absolute_path_to_skill_dir>/scripts/tensorslab_video.py" "a spaceship flying through space"

# 10 second horizontal video
python "<absolute_path_to_skill_dir>/scripts/tensorslab_video.py" "sunset over ocean waves" --duration 10 --ratio 16:9

# Image-to-video with local file
python "<absolute_path_to_skill_dir>/scripts/tensorslab_video.py" "make this photo come alive" --source portrait.jpg

# Image-to-video with URL
python "<absolute_path_to_skill_dir>/scripts/tensorslab_video.py" "make this photo come alive" --image-url https://example.com/portrait.jpg

# Fast preview
python "<absolute_path_to_skill_dir>/scripts/tensorslab_video.py" "abstract flowing colors" --model seedancev1profast

# High quality with audio
python "<absolute_path_to_skill_dir>/scripts/tensorslab_video.py" "epic mountain timelapse" --resolution 1440p --duration 10 --audio

# Custom output directory
python "<absolute_path_to_skill_dir>/scripts/tensorslab_video.py" "a sunset timelapse" --output-dir ./my_videos
```

## Task Status Flow

| Status | Code | Meaning |
|--------|------|---------|
| Pending | 1 | Task waiting in queue |
| Processing | 2 | Currently generating |
| Completed | 3 | Done, video ready |
| Failed | 4 | Error occurred |
| Uploading | 5 | Uploading generated video |

## Error Handling

Translate API errors to user-friendly messages:

| Error Code | Meaning | User Message |
|------------|---------|--------------|
| 9000 | Insufficient credits | "亲，积分用完啦，请前往 https://tensorai.tensorslab.com/ 充值" |
| 9999 | General error | Show the specific error message |

## Output

All videos are saved to output directory with naming pattern:
- Default: `./tensorslab_output/` (current working directory)
- Custom: Use `--output-dir` or `-o` to specify a different path
- Naming: `{task_id}_{index}.mp4` - e.g., `abcd_1234567890_0.mp4`

**URL mapping**: The script also saves file-to-URL mappings in `./tensorslab_output/urls.yaml`. This file tracks the original URLs for each downloaded file and accumulates entries across multiple runs. When you need the original URL of a generated video, read this file.

```yaml
# Example urls.yaml content
abcd_1234567890_0.mp4: https://tensorai.tensorslab.com/videos/abcd_1234567890_0.mp4
```

After completion, the script outputs both the local file path and the remote URL. Inform user with both:
```
🎉 您的视频处理完毕！
   - File: ./tensorslab_output/{filename}
   - URL: {remote_url}
```

## Tips for Better Results

### Text-to-Video
- Include cinematic terms: "wide shot", "close-up", "pan", "dolly"
- Describe motion: "flying rapidly", "slowly drifting", "zooming in"
- Specify style: "cinematic", "documentary style", "dreamy"

### Image-to-Video
- Describe the desired motion: "gentle sway", "subtle movement"
- For landscapes: "clouds moving", "water flowing", "leaves rustling"

## Resources

- **scripts/tensorslab_video.py**: Main API client with full CLI support
- **references/api_reference.md**: Detailed API documentation
