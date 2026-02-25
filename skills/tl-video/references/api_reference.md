# TensorsLab Video API Reference

## Base URL

```
https://test.tensorai.tensorslab.com
```

## Authentication

All requests require Bearer token authentication:

```
Authorization: Bearer <TENSORSLAB_API_KEY>
```

## Response Format

All responses follow this structure:

```json
{
  "code": 1000,
  "msg": "Success message",
  "data": { ... }
}
```

### Response Codes

| Code | Meaning |
|------|---------|
| 1000 | Success |
| 9000 | Insufficient Credits |
| 9999 | Error |

## Endpoints

### 1. Generate Video (SeeDance V2 - Latest)

**Endpoint:** `POST /v1/video/seedancev2`

**Recommended for:** Highest quality, general purpose

**Parameters (multipart/form-data):**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | Text description of desired video |
| `ratio` | string | No | Aspect ratio, default: "9:16" |
| `duration` | integer | No | 5-15 seconds, default: 5 |
| `resolution` | string | No | 480p, 720p, 1080p, 1440p, default: "1080p" |
| `fps` | string | No | Frame rate, default: "24" |
| `sourceImage` | file[] | No | Source images (1-2 images) |
| `generate_audio` | string | No | "1" to generate audio |
| `return_last_frame` | string | No | "1" to return last frame as image |
| `seed` | integer | No | Random seed |

**Response:**

```json
{
  "code": 1000,
  "msg": "Task created successfully",
  "data": {
    "taskid": "abcd_1234567890abcdef"
  }
}
```

### 2. Generate Video (SeeDance V1.5 Pro)

**Endpoint:** `POST /v1/video/seedancev15pro`

**Recommended for:** High-quality productions

**Parameters:**

Same as seedancev2 except:
- Duration: 5-10 seconds only
- Resolution: 480p, 720p, 1080p
- No `generate_audio` or `return_last_frame` options

### 3. Generate Video (SeeDance V1 Pro Fast)

**Endpoint:** `POST /v1/video/seedancev1profast`

**Recommended for:** Quick previews, faster generation

**Parameters:**

Same as seedancev15pro

### 4. Generate Video (SeeDance V1 Lite)

**Endpoint:** `POST /v1/video/seedancev1`

**Recommended for:** Basic videos, cost-effective

**Parameters:**

Same as seedancev15pro

### 5. Query Task Status

**Endpoint:** `POST /v1/video/infobytaskid`

**Request Body (application/json):**

```json
{
  "taskid": "abcd_1234567890abcdef",
  "moreTaskInfo": false
}
```

**Response:**

```json
{
  "code": 1000,
  "msg": "OK",
  "data": {
    "taskid": "abcd_1234567890abcdef",
    "url": ["https://example.com/video.mp4"],
    "task_status": 3,
    "prompt": "...",
    "imageurl": "https://...",
    "resolution": "1080p",
    "fps": 24,
    "source": "seedancev2",
    "duration": 5,
    "seed": 12345,
    "ratio": "16:9"
  }
}
```

### Task Status Codes

| Code | Status |
|------|--------|
| 1 | Pending |
| 2 | Processing |
| 3 | Completed (url array contains results) |
| 4 | Failed (check message field) |
| 5 | Uploading |

### 6. Delete Task

**Endpoint:** `POST /v1/video/deletevideotask`

**Request Body:**

```json
{
  "taskids": ["taskid1", "taskid2"]
}
```

## Common Parameters

### Ratio (Aspect Ratio)

| Value | Description | Use Case |
|-------|-------------|----------|
| `9:16` | Vertical | TikTok, Reels, Shorts |
| `16:9` | Horizontal | YouTube, standard video |

### Resolution

| Value | Description | Available Models |
|-------|-------------|------------------|
| `480p` | SD quality | All models |
| `720p` | HD quality | All models |
| `1080p` | Full HD | All models |
| `1440p` | 2K quality | seedancev2 only |

### Duration

| Model | Range |
|-------|-------|
| seedancev2 | 5-15 seconds |
| Others | 5-10 seconds |

## Error Handling

### Insufficient Credits (9000)

```json
{
  "code": 9000,
  "msg": "Insufficient credits"
}
```

**User message:** "亲，积分用完啦，请前往 https://test.tensorai.tensorslab.com/ 充值"

### Task Failed (task_status: 4)

```json
{
  "data": {
    "taskid": "...",
    "task_status": 4,
    "message": "Generation failed: specific reason"
  }
}
```

## Timeout

Request timeout: 300000ms (5 minutes)

For video generation, tasks run asynchronously. Poll the status endpoint until completion.

## Typical Generation Times

| Resolution/Duration | Approximate Time |
|---------------------|------------------|
| 5s @ 720p | 2-3 minutes |
| 5s @ 1080p | 3-5 minutes |
| 10s @ 1080p | 5-10 minutes |
| 15s @ 1440p | 10-15 minutes |

Times vary based on queue and complexity.
