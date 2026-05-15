---
name: ali-video
description: Generate videos using Aliyun Bailian's HappyHorse AI video generation models via DashScope API. Supports text-to-video (T2V), image-to-video (I2V with first frame), and reference-to-video (R2V with multiple reference images). Requires DASHSCOPE_API_KEY. Video generation typically takes 1-5 minutes.
---

# Aliyun Bailian Video Generation (HappyHorse)

## Overview

This skill enables AI-powered video generation through Aliyun Bailian's DashScope API using HappyHorse models. Three generation modes are supported: text-to-video, image-to-video (first-frame based), and reference-to-video (multiple reference images). Video generation typically takes 1-5 minutes.

## Script Path

The Python scripts for this skill are located in the `scripts/` subdirectory relative to this SKILL.md file. **Always use the absolute path when executing scripts.** Determine the absolute path based on where this skill is installed.

For example, if this SKILL.md is at `/path/to/skills/ali-video/SKILL.md`, then:
- Auth script: `python "/path/to/skills/ali-video/scripts/ali_auth.py"`
- Video script: `python "/path/to/skills/ali-video/scripts/ali_video.py"`
- Query script: `python "/path/to/skills/ali-video/scripts/ali_query_task.py"`

When executing, construct the command using the resolved absolute path:
```bash
python "<absolute_path_to_skill_dir>/scripts/ali_video.py" <args>
```

## Authorization

The script reads the API key from the `.env` file at the skills directory. **Do NOT ask the user for an API key upfront.** Just run the script directly.

If the script fails with an authentication error (invalid/expired key), THEN tell the user:
1. Their API key is invalid or expired
2. Get a new key from: https://bailian.console.aliyun.com/
3. Pass directly: `--api-key YOUR_KEY`

The key passed via `--api-key` is **automatically saved** to the `.env` file at the skills directory. Future sessions will pick it up without needing to pass the key again.

## Models

| Mode | Model | Description | Best For |
|------|-------|-------------|----------|
| **T2V** | `happyhorse-1.0-t2v` | Text-to-Video | Default, generating video from text descriptions |
| **I2V** | `happyhorse-1.0-i2v` | Image-to-Video (first frame) | Animating a single image |
| **R2V** | `happyhorse-1.0-r2v` | Reference-to-Video | Combining multiple reference images into video |

Default mode: `t2v` (text-to-video)

## Workflow

### 1. Text-to-Video (T2V)

User request: "做一段 10 秒钟横屏的宇宙飞船穿梭星际的视频"

**Constraints:**
- Do NOT pass `--image-url` or `--reference-image` for T2V mode.

**Agent processing:**
1. Extract parameters: `duration=10`, `ratio="16:9"`
2. Enhance prompt with cinematic details, camera movements, scene descriptions
3. Call API with enriched prompt
4. Monitor progress with heartbeat updates (every 60 seconds)
5. Download to `./ali_output/`

**Example enhanced prompt:**
```
Cinematic wide shot of a spaceship rapidly flying through space, passing glowing
nebulae and distant stars, lens flares, dramatic camera movement, epic scale,
movie-quality visual effects, smooth 24fps motion
```

### 2. Image-to-Video (I2V)

User request: "让这张人物合影 family.jpg 动起来" or "让风景照动起来"

**Agent processing:**
1. Verify image URL (must be a publicly accessible HTTP/HTTPS URL or base64 data URL)
2. Enhance prompt with motion instructions
3. Monitor progress with heartbeat updates
4. Download results

**Parameters for I2V:**
- `--image-url`: First-frame image (required for I2V). Supports three formats:
  - Public URL: `https://example.com/image.png`
  - Base64 data URL: `data:image/png;base64,iVBORw0KGgo...`
  - Local file path: `./my_image.jpg` (auto-converted to base64)
- Prompt: Optional text describing desired motion/animation

**Note:** I2V does not support `--ratio`. Output aspect ratio matches the input image.

**Image constraints:**
- Formats: JPEG, JPG, PNG, WEBP
- Min resolution: 300x300 (width and height each >= 300px)
- Aspect ratio: 1:2.5 to 2.5:1
- Max size: 20MB

### 3. Reference-to-Video (R2V)

User request: "用这几张参考图生成一段视频" or "根据参考人物和场景生成视频"

**Agent processing:**
1. Collect 1-9 reference image URLs
2. Craft prompt using `[Image 1]`, `[Image 2]` tags to reference images by position
3. Monitor progress with heartbeat updates
4. Download results

**Parameters for R2V:**
- `--reference-image`: Reference images (1-9). Each supports:
  - Public URL: `https://example.com/image.jpg`
  - Base64 data URL: `data:image/jpeg;base64,...`
  - Local file path: `./ref.jpg` (auto-converted to base64)
- Prompt: Must use `[Image N]` tags to reference images

**Example prompt:**
```
[Image 1]中身着红色旗袍的女性缓缓展开[Image 2]中的折扇，镜头推进特写
```

**Image constraints:**
- 1-9 reference images
- Formats: JPEG, PNG, WEBP
- Min short side: 400px
- Max size: 10MB per image

### 4. Resolution and Aspect Ratio

**Aspect ratios (T2V and R2V only):**
- `16:9` - Horizontal (YouTube, standard video) - **default**
- `9:16` - Vertical (TikTok, Reels, Shorts)
- `1:1` - Square
- `4:3` - Standard
- `3:4` - Portrait

**Resolutions:**
- `720P` - HD quality - **default**
- `1080P` - Full HD

### 5. Duration Options

- Range: 3-15 seconds
- Default: 5 seconds
- Longer videos take proportionally more time to generate

## Progress Tracking

Video generation times vary by duration:
- **5s video:** ~1-2 minutes
- **10s video:** ~2-4 minutes
- **15s video:** ~5+ minutes

Keep users informed:

```
Waiting for video generation to complete...
   (This may take 1-5 minutes, longer for 15s videos - please be patient)
Status: RUNNING (elapsed: 45s)
Video rendering in progress, elapsed 60s, please wait...
Video rendering in progress, elapsed 120s, please wait...
Task completed!
```

**Heartbeat interval:** Print encouraging message every 60 seconds.

## Using the Script

> **Dependencies:** The script requires `requests` and `pyyaml` libraries. Install before first use:
> ```bash
> pip install requests pyyaml
> ```

Execute the Python script directly:

```bash
# Text-to-video (T2V, default 5s, 16:9)
python "<absolute_path_to_skill_dir>/scripts/ali_video.py" "a spaceship flying through space"

# 10 second vertical video
python "<absolute_path_to_skill_dir>/scripts/ali_video.py" "sunset over ocean waves" --duration 10 --ratio 9:16

# Image-to-video (I2V) with first-frame URL
python "<absolute_path_to_skill_dir>/scripts/ali_video.py" "a cat running on grass" --model i2v --image-url https://example.com/cat.jpg

# I2V with local image file (auto-converted to base64)
python "<absolute_path_to_skill_dir>/scripts/ali_video.py" "gentle waves" --model i2v --image-url ./my_photo.png

# Reference-to-video (R2V) with multiple images
python "<absolute_path_to_skill_dir>/scripts/ali_video.py" "[Image 1] girl in dress holding [Image 2] fan" --model r2v --reference-image https://example.com/girl.jpg --reference-image https://example.com/fan.jpg

# High quality 1080P
python "<absolute_path_to_skill_dir>/scripts/ali_video.py" "epic mountain timelapse" --resolution 1080P --duration 10

# With watermark
python "<absolute_path_to_skill_dir>/scripts/ali_video.py" "abstract flowing colors" --watermark true

# Custom output directory
python "<absolute_path_to_skill_dir>/scripts/ali_video.py" "a sunset timelapse" --output-dir ./my_videos
```

## Querying Task Status After Timeout

If video generation times out, the script prints the task ID and suggests using the query script. To check status or download a completed task later:

```bash
# Poll and wait for completion (default 120s), auto-download on success
python "<absolute_path_to_skill_dir>/scripts/ali_query_task.py" TASK_ID

# Wait longer (e.g. 10 minutes)
python "<absolute_path_to_skill_dir>/scripts/ali_query_task.py" TASK_ID --wait 600

# Poll with custom interval and output directory
python "<absolute_path_to_skill_dir>/scripts/ali_query_task.py" TASK_ID --wait 600 --poll-interval 15 --output-dir ./my_videos

# Single query, just check status (no waiting)
python "<absolute_path_to_skill_dir>/scripts/ali_query_task.py" TASK_ID --wait 0

# Single query + download if already succeeded
python "<absolute_path_to_skill_dir>/scripts/ali_query_task.py" TASK_ID --wait 0 --download
```

The script polls until the task reaches a terminal state (SUCCEEDED/FAILED/UNKNOWN) or the timeout expires. `--wait` defaults to 120 seconds; pass `--wait 0` for a single query. On success it auto-downloads the video. On timeout it prints the task ID again so the agent can retry.

## Task Status Flow

| Status | Meaning |
|--------|---------|
| PENDING | Task waiting in queue |
| RUNNING | Currently generating |
| SUCCEEDED | Done, video ready for download |
| FAILED | Error occurred, check error code and message |
| UNKNOWN | Task expired (>24 hours) or not found |

## Error Handling

| Scenario | User Message |
|----------|--------------|
| No API key / key invalid | "API key not found or invalid. Get a new key from https://bailian.console.aliyun.com/ and set via --api-key" |
| Task failed | Show the specific error code and message from API |
| Timeout | "Generation timed out after N seconds. Task ID: xxx. Use query script to check later: python ali_query_task.py xxx" |
| Invalid parameters | Show validation error |

## Output

All videos are saved to output directory with naming pattern:
- Default: `./ali_output/` (current working directory)
- Custom: Use `--output-dir` or `-o` to specify a different path
- Naming: `{task_id}.mp4` - e.g., `0385dc79-5ff8-4d82-bcb6-xxxxxx.mp4`

**URL mapping**: The script also saves file-to-URL mappings in `./ali_output/urls.yaml`. This file tracks the original URLs for each downloaded file and accumulates entries across multiple runs. When you need the original URL of a generated video, read this file.

**Important:** Video URLs expire after 24 hours. Download promptly.

After completion, the script outputs both the local file path and the remote URL. Inform user with both:
```
Video generation complete!
   - File: ./ali_output/{filename}
   - URL: {remote_url}
```

## Tips for Better Results

### Text-to-Video (T2V)
- Include cinematic terms: "wide shot", "close-up", "pan", "dolly"
- Describe motion: "flying rapidly", "slowly drifting", "zooming in"
- Specify style: "cinematic", "documentary style", "dreamy"
- Prompt supports up to 5000 English chars or 2500 Chinese chars

### Image-to-Video (I2V)
- Describe the desired motion: "gentle sway", "subtle movement"
- For landscapes: "clouds moving", "water flowing", "leaves rustling"
- The output ratio matches the input image automatically

### Reference-to-Video (R2V)
- Use `[Image 1]`, `[Image 2]` tags in prompt to reference specific images
- Be specific about how elements from different images should interact
- 1-9 reference images supported

## Resources

- **scripts/ali_video.py**: Main API client with full CLI support
- **scripts/ali_query_task.py**: Standalone task query/download script (use after timeout)
- **scripts/ali_auth.py**: API key management module
- **references/api_reference.md**: Detailed DashScope HappyHorse API documentation
- **DashScope Console**: https://bailian.console.aliyun.com/
