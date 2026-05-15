# Aliyun Bailian HappyHorse Video Generation API Reference

## Overview

The DashScope Video Generation API provides AI-powered video generation through three HappyHorse models:

| Mode | Model | Description |
|------|-------|-------------|
| Text-to-Video (T2V) | `happyhorse-1.0-t2v` | Generate video from text prompt |
| Image-to-Video (I2V) | `happyhorse-1.0-i2v` | Generate video from first-frame image + optional text |
| Reference-to-Video (R2V) | `happyhorse-1.0-r2v` | Generate video from 1-9 reference images + text |

## Authentication

All requests require a DashScope API key in the Authorization header:

```
Authorization: Bearer $DASHSCOPE_API_KEY
```

Get your API key from: https://bailian.console.aliyun.com/

The API key is stored in the `.env` file at the skills directory (not environment variables).

## Endpoints

### Submit Task

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
```

Required headers:
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `Content-Type: application/json`
- `X-DashScope-Async: enable` (required - API only supports async calls)

### Query Task Status

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

Required headers:
- `Authorization: Bearer $DASHSCOPE_API_KEY`

## Request Format

### T2V (Text-to-Video)

```json
{
    "model": "happyhorse-1.0-t2v",
    "input": {
        "prompt": "Your text prompt here (max 5000 chars / 2500 Chinese chars)"
    },
    "parameters": {
        "resolution": "720P",
        "ratio": "16:9",
        "duration": 5
    }
}
```

### I2V (Image-to-Video)

```json
{
    "model": "happyhorse-1.0-i2v",
    "input": {
        "prompt": "Optional text guidance",
        "media": [
            {"type": "first_frame", "url": "https://example.com/image.png"}
        ]
    },
    "parameters": {
        "resolution": "720P",
        "duration": 5
    }
}
```

Note: I2V does not support the `ratio` parameter. Output aspect ratio matches the input image.

### R2V (Reference-to-Video)

```json
{
    "model": "happyhorse-1.0-r2v",
    "input": {
        "prompt": "[Image 1] description... [Image 2] description...",
        "media": [
            {"type": "reference_image", "url": "https://example.com/img1.jpg"},
            {"type": "reference_image", "url": "https://example.com/img2.jpg"}
        ]
    },
    "parameters": {
        "resolution": "720P",
        "ratio": "16:9",
        "duration": 5
    }
}
```

Use `[Image N]` tags in prompt to reference images by their position in the media array.

## Parameters

| Parameter | Type | Values | Default | T2V | I2V | R2V |
|-----------|------|--------|---------|-----|-----|-----|
| `resolution` | string | "720P", "1080P" | "1080P" | Yes | Yes | Yes |
| `ratio` | string | "16:9", "9:16", "1:1", "4:3", "3:4" | "16:9" | Yes | No | Yes |
| `duration` | int | 3-15 | 5 | Yes | Yes | Yes |
| `watermark` | bool | true/false | false | Yes | Yes | Yes |
| `seed` | int | 0-2147483647 | random | Yes | Yes | Yes |

## Task Status Flow

```
PENDING -> RUNNING -> SUCCEEDED
                  -> FAILED
         -> UNKNOWN (expired task_id, >24h)
```

## Response Format

### Task Submission Response

```json
{
    "output": {
        "task_status": "PENDING",
        "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx"
    },
    "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx"
}
```

### Task Completion Response

```json
{
    "output": {
        "task_id": "4673458e-...",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-04-20 17:55:17.075",
        "scheduled_time": "2026-04-20 17:55:17.129",
        "end_time": "2026-04-20 17:56:36.658",
        "video_url": "https://dashscope-result.oss-cn-beijing.aliyuncs.com/xxx.mp4?Expires=xxx"
    },
    "usage": {
        "duration": 5,
        "video_count": 1,
        "SR": 720,
        "ratio": "16:9"
    }
}
```

### Failure Response

```json
{
    "output": {
        "task_id": "86ecf553-...",
        "task_status": "FAILED",
        "code": "InvalidParameter",
        "message": "The parameter is invalid."
    }
}
```

## Image Constraints

### I2V First Frame
- Formats: JPEG, JPG, PNG, WEBP
- Min resolution: 300x300 (width and height each >= 300px)
- Aspect ratio: 1:2.5 to 2.5:1
- Max file size: 20MB
- Input formats:
  - Public URL (HTTP/HTTPS): `https://example.com/image.png`
  - Base64 data URL: `data:{MIME_type};base64,{base64_data}`
    - Example: `data:image/png;base64,iVBORw0KGgo...`

### R2V Reference Images
- 1-9 images
- Formats: JPEG, JPG, PNG, WEBP
- Min short side: 400px
- Max file size: 10MB per image

## Rate Limits

- Polling endpoint: 20 RPS
- Task ID validity: 24 hours
- Video URL validity: 24 hours (download promptly)

## Typical Generation Times

- 5s video: ~1-2 minutes
- 10s video: ~2-4 minutes
- 15s video: ~5+ minutes

Recommended polling interval: 15 seconds.


## doc url
https://www.alibabacloud.com/help/zh/model-studio/happyhorse-text-to-video-api-reference