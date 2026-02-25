---
name: tensorslab-video
description: Generate videos using TensorsLab's AI video generation models. Supports text-to-video and image-to-video generation with automatic prompt enhancement, progress tracking, and local file saving. Use for generating videos from text descriptions, animating static images, creating cinematic content, and various aspect ratios. Requires TENSORSLAB_API_KEY environment variable. Video generation takes several minutes.
---

# TensorsLab Video Generation

## Overview

This skill enables AI-powered video generation through TensorsLab's API, supporting both text-to-video and image-to-video workflows. Video generation is a time-intensive process - tasks typically take several minutes to complete.

## Authentication Check

Before any video generation, verify the API key is configured:

```bash
# Check if API key is set
echo $TENSORSLAB_API_KEY
```

If not set, display this friendly message:

```
您好！要生成高质量的内容，您需要先进行简单的配置：
1. 访问 https://tensorslab.tensorslab.com/ 登录并订阅。
2. 在控制台中获取您的专属 API Key。
3. 将其保存为环境变量：
   - Windows (PowerShell): $env:TENSORSLAB_API_KEY="您的Key"
   - Mac/Linux: export TENSORSLAB_API_KEY="您的Key"
```

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
2. For portraits/faces: set `camerafixed=1` to avoid distracting camera movement
3. Enhance prompt with motion instructions
4. Monitor progress with heartbeat updates
5. Download results

**Parameters for image-to-video:**
- `sourceImage`: Array of image files (1-2 images max)
- `imageUrl`: Comma-separated URLs of source images
- `camerafixed`: Set to "1" for stable scenes (portraits, products)
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

Execute the Python script directly:

```bash
# Text-to-video (default 5s, vertical 9:16)
python scripts/tensorslab_video.py "a spaceship flying through space"

# 10 second horizontal video
python scripts/tensorslab_video.py "sunset over ocean waves" --duration 10 --ratio 16:9

# Image-to-video with fixed camera
python scripts/tensorslab_video.py "make this photo come alive" --source portrait.jpg --camera-fixed

# Fast preview
python scripts/tensorslab_video.py "abstract flowing colors" --model seedancev1profast

# High quality with audio
python scripts/tensorslab_video.py "epic mountain timelapse" --resolution 1440p --duration 10 --audio
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
| 9000 | Insufficient credits | "亲，积分用完啦，请前往 https://tensorslab.tensorslab.com/ 充值" |
| 9999 | General error | Show the specific error message |

## Output

All videos are saved to `./tensorslab_output/` with naming pattern:
- `{task_id}_{index}.mp4` - e.g., `abcd_1234567890_0.mp4`

After completion, inform user:
```
🎉 您的视频处理完毕！已存放于 ./tensorslab_output/{filename}
```

## Tips for Better Results

### Text-to-Video
- Include cinematic terms: "wide shot", "close-up", "pan", "dolly"
- Describe motion: "flying rapidly", "slowly drifting", "zooming in"
- Specify style: "cinematic", "documentary style", "dreamy"

### Image-to-Video
- Use `camerafixed` for portraits and product shots
- Describe the desired motion: "gentle sway", "subtle movement"
- For landscapes: "clouds moving", "water flowing", "leaves rustling"

## Resources

- **scripts/tensorslab_video.py**: Main API client with full CLI support
- **references/api_reference.md**: Detailed API documentation
