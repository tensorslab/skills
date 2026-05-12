# Aliyun Bailian Video (ali-video) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a new `ali-video` skill that mirrors the tl-video skill's front-end UX (prompt enhancement, progress tracking, heartbeat messages, local downloads) but replaces the backend with Aliyun Bailian DashScope API using HappyHorse models.

**Architecture:** Follow tl-video's directory layout exactly (`SKILL.md`, `scripts/`, `references/`). Replace `tensorslab_auth.py` with a simpler `ali_auth.py` that manages `DASHSCOPE_API_KEY` via environment variable or `~/.ali_video/.env`. Replace `tensorslab_video.py` with `ali_video.py` that calls DashScope's async video synthesis API and polls for results. Three models are supported: T2V (text-to-video), I2V (image-to-video with first frame), and R2V (reference images + text prompt).

**Tech Stack:** Python 3.10+, `requests`, `pyyaml`

---

## File Structure

```
skills/ali-video/
  SKILL.md                          # Skill definition with usage docs
  references/
    api_reference.md                # DashScope HappyHorse API reference
  scripts/
    __init__.py                     # Empty package marker
    ali_auth.py                     # DashScope API key management
    ali_video.py                    # Main video generation CLI script
    ali_output/                     # Default output directory (created at runtime)
```

**Key differences from tl-video:**
- Auth: DashScope API key (no browser OAuth) - simpler, just env var or manual entry
- API: JSON POST (not multipart form) to `dashscope.aliyuncs.com`
- Models: `happyhorse-1.0-t2v`, `happyhorse-1.0-i2v`, `happyhorse-1.0-r2v`
- Polling: GET request to `/api/v1/tasks/{task_id}` with 15s interval
- Output dir: `ali_output/` instead of `tensorslab_output/`
- Config dir: `~/.ali_video/.env` instead of `~/.tensorslab/.env`

---

### Task 1: Create skill directory structure and empty files

**Files:**
- Create: `skills/ali-video/scripts/__init__.py`
- Create: `skills/ali-video/references/` (directory)

- [ ] **Step 1: Create directory structure and empty __init__.py**

```bash
mkdir -p "D:\skills\TL_Skills\skills\ali-video\scripts"
mkdir -p "D:\skills\TL_Skills\skills\ali-video\references"
```

Create `skills/ali-video/scripts/__init__.py` as an empty file (same as tl-video).

- [ ] **Step 2: Commit**

```bash
git add skills/ali-video/scripts/__init__.py
git commit -m "chore: scaffold ali-video skill directory structure"
```

---

### Task 2: Create `ali_auth.py` - DashScope API key management

**Files:**
- Create: `skills/ali-video/scripts/ali_auth.py`

This is a simplified version of `tensorslab_auth.py`. No browser OAuth - just API key loading from environment variable or `~/.ali_video/.env` file, plus manual entry prompt.

- [ ] **Step 1: Write `ali_auth.py`**

```python
#!/usr/bin/env python3
"""
Aliyun DashScope API Key Management Module

Manages DASHSCOPE_API_KEY for Aliyun Bailian video generation.
No browser OAuth - simple env var or file-based key management.
"""

import os
import sys
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Shared user configurations
USER_CONFIG_DIR = os.path.expanduser("~/.ali_video")
ENV_FILE_PATH = os.path.join(USER_CONFIG_DIR, ".env")
DEFAULT_OUTPUT_DIR = Path(".") / "ali_output"

# DashScope API constants
DASHSCOPE_API_BASE = "https://dashscope.aliyuncs.com"
DASHSCOPE_VIDEO_ENDPOINT = f"{DASHSCOPE_API_BASE}/api/v1/services/aigc/video-generation/video-synthesis"
DASHSCOPE_TASK_ENDPOINT = f"{DASHSCOPE_API_BASE}/api/v1/tasks"


def load_api_key_from_env() -> str | None:
    """
    Load API key from ~/.ali_video/.env file.

    Returns:
        The API key if found and valid (non-empty), None otherwise.
    """
    if not os.path.exists(ENV_FILE_PATH):
        return None

    try:
        with open(ENV_FILE_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("DASHSCOPE_API_KEY="):
                    api_key = line.strip().split("=", 1)[1].strip()
                    if api_key:
                        return api_key
                    return None
    except Exception as e:
        logger.warning(f"Failed to read .env file: {e}")

    return None


def save_api_key_to_env(api_key: str):
    """Save API key to ~/.ali_video/.env for future sessions."""
    try:
        os.makedirs(os.path.dirname(ENV_FILE_PATH), exist_ok=True)

        lines = []
        if os.path.exists(ENV_FILE_PATH):
            with open(ENV_FILE_PATH, "r", encoding="utf-8") as f:
                lines = f.readlines()

        new_lines = []
        key_updated = False
        for line in lines:
            if line.startswith("DASHSCOPE_API_KEY="):
                new_lines.append(f"DASHSCOPE_API_KEY={api_key}\n")
                key_updated = True
            else:
                new_lines.append(line)

        if not key_updated:
            new_lines.append(f"DASHSCOPE_API_KEY={api_key}\n")

        with open(ENV_FILE_PATH, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        logger.info(f"[Success] API Key persisted to: {ENV_FILE_PATH}")
    except Exception as e:
        logger.warning(f"[Warning] Failed to save API key to .env: {e}")


def get_or_prompt_api_key() -> str:
    """
    Get API key from environment variable or ~/.ali_video/.env file.

    Returns:
        The API key.

    Exits with error if no key is found and not running interactively.
    """
    # First check environment variable
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if api_key:
        return api_key

    # Then check .env file
    api_key = load_api_key_from_env()
    if api_key:
        os.environ["DASHSCOPE_API_KEY"] = api_key
        return api_key

    logger.error("=" * 60)
    logger.error("[!] DASHSCOPE_API_KEY not found.")
    logger.error("[!] Please get your API key from:")
    logger.error("[!]   https://bailian.console.aliyun.com/")
    logger.error("[!] Then set it via:")
    logger.error("[!]   export DASHSCOPE_API_KEY=your_api_key_here")
    logger.error("[!] Or re-run this script with: --api-key YOUR_KEY")
    logger.error("=" * 60)
    sys.exit(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    api_key = get_or_prompt_api_key()
    if api_key:
        print(f"[Success] API Key: {api_key[:4]}****{api_key[-4:]}")
```

- [ ] **Step 2: Commit**

```bash
git add skills/ali-video/scripts/ali_auth.py
git commit -m "feat(ali-video): add DashScope API key management module"
```

---

### Task 3: Create `ali_video.py` - Main video generation script

**Files:**
- Create: `skills/ali-video/scripts/ali_video.py`

This is the core script. It mirrors `tensorslab_video.py` structure but uses DashScope JSON API. Three models supported: T2V, I2V, R2V. The API is async - submit task, get task_id, poll GET endpoint.

Key differences from tl-video:
- Uses JSON POST body (not multipart form) with `X-DashScope-Async: enable` header
- Different response parsing: `output.task_id`, `output.task_status` (PENDING/RUNNING/SUCCEEDED/FAILED)
- Result URL is at `output.video_url` (single URL, not array)
- Poll interval: 15 seconds (per DashScope recommendation)
- Image input for I2V uses `input.media[].type = "first_frame"` with URL
- R2V uses `input.media[].type = "reference_image"` with `[Image N]` tags in prompt

- [ ] **Step 1: Write `ali_video.py`**

```python
#!/usr/bin/env python3
"""
Aliyun Bailian Video Generation Client (HappyHorse Models)

Supports three modes:
  - T2V: Text-to-Video (happyhorse-1.0-t2v)
  - I2V: Image-to-Video, first-frame based (happyhorse-1.0-i2v)
  - R2V: Reference images + text to Video (happyhorse-1.0-r2v)

Uses DashScope async API: submit task -> poll for completion -> download result.
"""

import os
import sys
import time
import json
import argparse
import logging
from pathlib import Path
from typing import Optional, List

try:
    import requests
except ImportError:
    import logging as _logging
    _logging.getLogger(__name__).error("Error: requests module is required. Install with: pip install requests")
    import sys as _sys
    _sys.exit(1)

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

# Resolve script directory so imports work regardless of CWD
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from ali_auth import (
    get_or_prompt_api_key,
    save_api_key_to_env,
    DASHSCOPE_VIDEO_ENDPOINT,
    DASHSCOPE_TASK_ENDPOINT,
    DEFAULT_OUTPUT_DIR,
)

# Disable proxies for this session
_SESSION = requests.Session()
_SESSION.proxies = {"http": "", "https": ""}


class AliVideoAPIError(Exception):
    """Aliyun video API error with context."""
    pass


logger = logging.getLogger(__name__)

# DashScope task status values
TASK_STATUS_PENDING = "PENDING"
TASK_STATUS_RUNNING = "RUNNING"
TASK_STATUS_SUCCEEDED = "SUCCEEDED"
TASK_STATUS_FAILED = "FAILED"
TASK_STATUS_UNKNOWN = "UNKNOWN"

# Model names
MODEL_T2V = "happyhorse-1.0-t2v"
MODEL_I2V = "happyhorse-1.0-i2v"
MODEL_R2V = "happyhorse-1.0-r2v"

ALL_MODELS = [MODEL_T2V, MODEL_I2V, MODEL_R2V]


def ensure_output_dir(output_dir: Path):
    """Create output directory if it doesn't exist."""
    output_dir.mkdir(parents=True, exist_ok=True)


def download_video(url: str, output_path: Path) -> bool:
    """Download a video from URL to local path."""
    try:
        response = _SESSION.get(url, timeout=300, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        progress_markers = [10, 25, 50, 75, 100]
        next_marker_idx = 0

        with open(output_path, 'wb') as f:
            if total_size > 0:
                size_mb = total_size / (1024 * 1024)
                logger.info(f"Downloading video ({size_mb:.1f} MB): {output_path}")
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        percent = (downloaded / total_size) * 100
                        while next_marker_idx < len(progress_markers) and percent >= progress_markers[next_marker_idx]:
                            marker = progress_markers[next_marker_idx]
                            logger.info(f"Download progress: {marker}%")
                            next_marker_idx += 1
            else:
                logger.info(f"Downloading video: {output_path}")
                f.write(response.content)

        logger.info(f"Download complete: {output_path}")
        return True
    except Exception as e:
        logger.warning(f"Failed to download video from {url}: {e}")
        return False


def save_url_mapping(output_dir: Path, filename: str, url: str):
    """
    Save filename-to-URL mapping to urls.yaml.
    """
    if not YAML_AVAILABLE:
        return

    urls_file = output_dir / "urls.yaml"

    if urls_file.exists():
        try:
            with open(urls_file, 'r', encoding='utf-8') as f:
                mappings = yaml.safe_load(f) or {}
        except Exception:
            mappings = {}
    else:
        mappings = {}

    mappings[filename] = url

    with open(urls_file, 'w', encoding='utf-8') as f:
        yaml.dump(mappings, f, allow_unicode=True, sort_keys=False)


def generate_video(
    prompt: str,
    model: str = MODEL_T2V,
    ratio: str = "16:9",
    duration: int = 5,
    resolution: str = "720P",
    image_url: Optional[str] = None,
    reference_images: Optional[List[str]] = None,
    seed: Optional[int] = None,
    watermark: bool = True,
    api_key: Optional[str] = None,
) -> str:
    """
    Submit a video generation task to DashScope API.

    Args:
        prompt: Text prompt for video generation.
        model: Model to use (happyhorse-1.0-t2v, happyhorse-1.0-i2v, happyhorse-1.0-r2v).
        ratio: Video aspect ratio (16:9, 9:16, 1:1, 4:3, 3:4). Not supported by I2V.
        duration: Video duration in seconds (3-15, default 5).
        resolution: Video resolution (720P or 1080P, default 720P).
        image_url: URL of first-frame image for I2V.
        reference_images: List of reference image URLs for R2V (1-9 images).
        seed: Random seed for reproducibility.
        watermark: Whether to add watermark (default True).
        api_key: DashScope API key (uses env var if not provided).

    Returns:
        Task ID for tracking generation status.
    """
    if api_key is None:
        api_key = get_or_prompt_api_key()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable",
    }

    # Build request body
    body = {
        "model": model,
        "input": {},
        "parameters": {
            "resolution": resolution,
            "duration": duration,
        },
    }

    # Add ratio parameter (not supported by I2V)
    if model != MODEL_I2V:
        body["parameters"]["ratio"] = ratio

    # Add optional parameters
    if seed is not None:
        body["parameters"]["seed"] = seed
    if not watermark:
        body["parameters"]["watermark"] = False

    # Build input based on model
    if model == MODEL_T2V:
        body["input"]["prompt"] = prompt

    elif model == MODEL_I2V:
        if not image_url:
            raise AliVideoAPIError("I2V model requires --image-url parameter")
        body["input"]["prompt"] = prompt
        body["input"]["media"] = [
            {"type": "first_frame", "url": image_url}
        ]

    elif model == MODEL_R2V:
        if not reference_images or len(reference_images) == 0:
            raise AliVideoAPIError("R2V model requires at least one --reference-image URL")
        body["input"]["prompt"] = prompt
        body["input"]["media"] = [
            {"type": "reference_image", "url": url}
            for url in reference_images[:9]
        ]

    try:
        logger.info(f"Generating video using {model}...")
        logger.info(f"Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
        logger.info(f"Settings: {ratio} @ {resolution}, {duration}s")

        response = _SESSION.post(
            DASHSCOPE_VIDEO_ENDPOINT,
            headers=headers,
            json=body,
            timeout=60,
        )

        logger.debug(f"API Response ({response.status_code}): {response.text}")

        try:
            result = response.json()
        except ValueError:
            raise AliVideoAPIError(f"Invalid JSON response (HTTP {response.status_code}): {response.text}")

        # Check for API errors
        if response.status_code != 200:
            error_msg = result.get("message", "Unknown error")
            error_code = result.get("code", "Unknown")
            raise AliVideoAPIError(f"API error: {error_msg} (Code: {error_code})")

        task_id = result.get("output", {}).get("task_id")
        if not task_id:
            raise AliVideoAPIError(f"No task_id in response: {result}")

        task_status = result.get("output", {}).get("task_status", "UNKNOWN")
        logger.info(f"Task created successfully! Task ID: {task_id}, Status: {task_status}")
        return task_id

    except AliVideoAPIError:
        raise
    except requests.exceptions.RequestException as e:
        raise AliVideoAPIError(f"Network error: {e}") from e


def query_task_status(task_id: str, api_key: Optional[str] = None) -> Optional[dict]:
    """
    Query the status of a video generation task via DashScope API.

    Args:
        task_id: Task ID to query.
        api_key: DashScope API key.

    Returns:
        The 'output' dict from the response, or None on error.
    """
    if api_key is None:
        api_key = get_or_prompt_api_key()

    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    endpoint = f"{DASHSCOPE_TASK_ENDPOINT}/{task_id}"

    try:
        response = _SESSION.get(endpoint, headers=headers, timeout=30)

        try:
            result = response.json()
        except ValueError:
            logger.error(f"Invalid JSON response (HTTP {response.status_code}): {response.text}")
            return None

        if response.status_code != 200:
            logger.error(f"Error querying task: {result.get('message', 'Unknown error')}")
            return None

        return result.get("output", {})

    except requests.exceptions.RequestException as e:
        logger.error(f"Error querying task status: {e}")
        return None


def wait_and_download(
    task_id: str,
    api_key: Optional[str] = None,
    poll_interval: int = 15,
    timeout: int = 1800,
    output_dir: Optional[Path] = None,
) -> List[dict]:
    """
    Wait for task completion and download generated video.

    Args:
        task_id: Task ID to wait for.
        api_key: DashScope API key.
        poll_interval: Seconds between status checks (default 15, per DashScope recommendation).
        timeout: Maximum seconds to wait (default 30 minutes).
        output_dir: Output directory path (default: ./ali_output).

    Returns:
        List of dicts with 'file' (local path) and 'url' (remote URL) for each downloaded video.
    """
    if api_key is None:
        api_key = get_or_prompt_api_key()
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR
    output_dir = Path(output_dir).expanduser().resolve()

    ensure_output_dir(output_dir)
    downloaded_files = []
    start_time = time.time()

    logger.info("Waiting for video generation to complete...")
    logger.info("   (This may take 1-5 minutes - please be patient)")

    last_heartbeat = 0
    last_status = None
    last_status_log = -999999

    while time.time() - start_time < timeout:
        task_output = query_task_status(task_id, api_key)

        if not task_output:
            time.sleep(poll_interval)
            continue

        status = task_output.get("task_status", "UNKNOWN")
        elapsed = int(time.time() - start_time)

        should_log_status = (status != last_status) or (elapsed - last_status_log >= 60)
        if should_log_status:
            logger.info(f"Status: {status} (elapsed: {elapsed}s)")
            last_status = status
            last_status_log = elapsed

        # Heartbeat every 60 seconds while running
        if status == TASK_STATUS_RUNNING and elapsed - last_heartbeat >= 60:
            logger.info(f"Video rendering in progress, elapsed {elapsed}s, please wait...")
            last_heartbeat = elapsed

        if status == TASK_STATUS_SUCCEEDED:
            logger.info("Task completed!")
            video_url = task_output.get("video_url")

            if not video_url:
                logger.warning("No video URL returned")
                return downloaded_files

            # Determine filename
            from urllib.parse import urlparse
            url_path = urlparse(video_url).path
            ext = Path(url_path).suffix
            if not ext or len(ext) > 5:
                ext = ".mp4"
            filename = f"{task_id}{ext}"
            output_path = output_dir / filename

            logger.info("Preparing download...")
            if download_video(video_url, output_path):
                downloaded_files.append({"file": str(output_path), "url": video_url})
                save_url_mapping(output_dir, filename, video_url)

            return downloaded_files

        elif status == TASK_STATUS_FAILED:
            error_code = task_output.get("code", "Unknown")
            error_msg = task_output.get("message", "Unknown error")
            raise AliVideoAPIError(f"Task failed: {error_msg} (Code: {error_code})")

        elif status == TASK_STATUS_UNKNOWN:
            raise AliVideoAPIError("Task expired or not found (task_id may be older than 24 hours)")

        time.sleep(poll_interval)

    raise AliVideoAPIError(f"Timeout waiting for task completion (waited {timeout}s)")


def main():
    parser = argparse.ArgumentParser(
        description="Generate videos using Aliyun Bailian HappyHorse models (DashScope API)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text-to-video (T2V, default)
  python ali_video.py "a spaceship flying through space"

  # Specify duration and aspect ratio
  python ali_video.py "sunset over ocean waves" --duration 10 --ratio 16:9

  # Image-to-video (I2V) with first-frame image URL
  python ali_video.py "a cat running on grass" --model i2v --image-url https://example.com/cat.jpg

  # Reference-to-video (R2V) with multiple reference images
  python ali_video.py "[Image 1] girl in red dress holding [Image 2] fan" --model r2v --reference-image https://example.com/girl.jpg --reference-image https://example.com/fan.jpg

  # High quality 1080P
  python ali_video.py "epic mountain timelapse" --resolution 1080P --duration 10
        """
    )

    parser.add_argument("prompt", help="Text prompt for video generation")
    parser.add_argument("--model", "-m",
                        choices=["t2v", "i2v", "r2v"],
                        default="t2v",
                        help="Model mode: t2v (text-to-video, default), i2v (image-to-video), r2v (reference-to-video)")
    parser.add_argument("--ratio", "-r", default="16:9",
                        help="Video aspect ratio (default: 16:9; not supported by i2v)")
    parser.add_argument("--duration", "-d", type=int, default=5,
                        help="Video duration in seconds (3-15, default: 5)")
    parser.add_argument("--resolution", choices=["720P", "1080P"],
                        default="720P", help="Video resolution (default: 720P)")
    parser.add_argument("--image-url",
                        help="Source image URL for I2V mode (first-frame image)")
    parser.add_argument("--reference-image", action="append", dest="reference_images",
                        help="Reference image URL for R2V mode (can specify 1-9 times)")
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    parser.add_argument("--no-watermark", action="store_true",
                        help="Disable watermark (default: watermark enabled)")
    parser.add_argument("--api-key", help="DashScope API key (uses DASHSCOPE_API_KEY env var if not set)")
    parser.add_argument("--poll-interval", type=int, default=15,
                        help="Status check interval in seconds (default: 15)")
    parser.add_argument("--timeout", type=int, default=1800,
                        help="Maximum wait time in seconds (default: 1800 = 30 minutes)")
    parser.add_argument("--output-dir", "-o", type=str, default=None,
                        help="Output directory path (default: ./ali_output)")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level, format="%(asctime)s - %(levelname)s - %(message)s")

    # Map short model name to full model ID
    model_map = {
        "t2v": MODEL_T2V,
        "i2v": MODEL_I2V,
        "r2v": MODEL_R2V,
    }
    model_id = model_map[args.model]

    # Setup output directory
    output_dir = Path(DEFAULT_OUTPUT_DIR).expanduser().resolve()
    if args.output_dir:
        output_dir = Path(args.output_dir).expanduser().resolve()

    # Validate duration
    if args.duration < 3 or args.duration > 15:
        logger.error("Error: duration must be between 3 and 15 seconds")
        sys.exit(1)

    # Validate model-specific requirements
    if model_id == MODEL_I2V and not args.image_url:
        logger.error("Error: I2V mode requires --image-url parameter")
        sys.exit(1)

    if model_id == MODEL_R2V and (not args.reference_images or len(args.reference_images) == 0):
        logger.error("Error: R2V mode requires at least one --reference-image URL")
        sys.exit(1)

    if args.reference_images and len(args.reference_images) > 9:
        logger.error("Error: maximum 9 reference images allowed for R2V")
        sys.exit(1)

    try:
        # Generate video
        task_id = generate_video(
            prompt=args.prompt,
            model=model_id,
            ratio=args.ratio,
            duration=args.duration,
            resolution=args.resolution,
            image_url=args.image_url,
            reference_images=args.reference_images,
            seed=args.seed,
            watermark=not args.no_watermark,
            api_key=args.api_key,
        )

        # Wait and download
        downloaded = wait_and_download(
            task_id=task_id,
            api_key=args.api_key,
            poll_interval=args.poll_interval,
            timeout=args.timeout,
            output_dir=output_dir,
        )

        logger.info(f"\nVideo generation complete! Saved to {output_dir}/")

        # Emit structured result to stdout
        print(
            json.dumps(
                {
                    "ok": True,
                    "task_id": task_id,
                    "output_dir": str(output_dir),
                    "downloads": downloaded,
                },
                ensure_ascii=False,
            )
        )

        # Persist API key to ~/.ali_video/.env for future sessions
        persisted_key = args.api_key or os.environ.get("DASHSCOPE_API_KEY")
        if persisted_key:
            save_api_key_to_env(persisted_key)

    except AliVideoAPIError as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Commit**

```bash
git add skills/ali-video/scripts/ali_video.py
git commit -m "feat(ali-video): add main video generation script with T2V/I2V/R2V support"
```

---

### Task 4: Create `references/api_reference.md` - API documentation

**Files:**
- Create: `skills/ali-video/references/api_reference.md`

- [ ] **Step 1: Write API reference document**

```markdown
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
| `watermark` | bool | true/false | true | Yes | Yes | Yes |
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
- Min resolution: 300x300
- Aspect ratio: 1:2.5 to 2.5:1
- Max file size: 20MB
- Supports URL or base64 data URL

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
- 15s video: ~3-5 minutes

Recommended polling interval: 15 seconds.
```

- [ ] **Step 2: Commit**

```bash
git add skills/ali-video/references/api_reference.md
git commit -m "docs(ali-video): add DashScope HappyHorse API reference"
```

---

### Task 5: Create `SKILL.md` - Skill definition

**Files:**
- Create: `skills/ali-video/SKILL.md`

This mirrors tl-video's SKILL.md structure but adapts for Aliyun Bailian / HappyHorse models. The key sections: overview, script path, authorization, models, workflows, progress tracking, CLI usage, error handling, output conventions.

- [ ] **Step 1: Write `SKILL.md`**

```markdown
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

When executing, construct the command using the resolved absolute path:
```bash
python "<absolute_path_to_skill_dir>/scripts/ali_video.py" <args>
```

## Authorization

**BEFORE any video generation, you must ensure you have a DashScope API key.**

### API Key Setup

The script checks for `DASHSCOPE_API_KEY` in this order:
1. `DASHSCOPE_API_KEY` environment variable
2. `~/.ali_video/.env` file
3. Exit with instructions if neither found

*(Note: When you need to verify the environment variable, ONLY check if it exists. NEVER display or print the actual API key value.)*

**To get your API key:**
1. Go to https://bailian.console.aliyun.com/
2. Create or find your API key
3. Set it via:
```bash
export DASHSCOPE_API_KEY=your_api_key_here
```

After a successful generation, the API key is **automatically saved** to `~/.ali_video/.env`. Future sessions will pick it up without needing to export again.

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
- `--image-url`: URL of the first-frame image (required for I2V)
- Prompt: Optional text describing desired motion/animation

**Note:** I2V does not support `--ratio`. Output aspect ratio matches the input image.

**Image constraints:**
- Formats: JPEG, PNG, WEBP
- Min resolution: 300x300
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
- `--reference-image`: Use multiple times for multiple images (1-9)
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

Video generation takes **1-5 minutes**. Keep users informed:

```
Waiting for video generation to complete...
   (This may take 1-5 minutes - please be patient)
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

# Reference-to-video (R2V) with multiple images
python "<absolute_path_to_skill_dir>/scripts/ali_video.py" "[Image 1] girl in dress holding [Image 2] fan" --model r2v --reference-image https://example.com/girl.jpg --reference-image https://example.com/fan.jpg

# High quality 1080P
python "<absolute_path_to_skill_dir>/scripts/ali_video.py" "epic mountain timelapse" --resolution 1080P --duration 10

# Without watermark
python "<absolute_path_to_skill_dir>/scripts/ali_video.py" "abstract flowing colors" --no-watermark

# Custom output directory
python "<absolute_path_to_skill_dir>/scripts/ali_video.py" "a sunset timelapse" --output-dir ./my_videos
```

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
| No API key | "Please set DASHSCOPE_API_KEY or get one from https://bailian.console.aliyun.com/" |
| Task failed | Show the specific error code and message from API |
| Timeout | "Generation timed out after N seconds" |
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
- **scripts/ali_auth.py**: API key management module
- **references/api_reference.md**: Detailed DashScope HappyHorse API documentation
- **DashScope Console**: https://bailian.console.aliyun.com/
```

- [ ] **Step 2: Commit**

```bash
git add skills/ali-video/SKILL.md
git commit -m "feat(ali-video): add SKILL.md skill definition"
```

---

### Task 6: Register ali-video in marketplace.json

**Files:**
- Modify: `.claude-plugin/marketplace.json`

Add a new plugin entry for `ali-video` alongside the existing `tl-image` and `tl-video` entries.

- [ ] **Step 1: Update marketplace.json**

Add the following entry to the `plugins` array:

```json
{
  "name": "ali-video",
  "source": "./skills/ali-video",
  "skills": "./",
  "description": "Aliyun Bailian Video Generation Skill. Generate videos using HappyHorse models via DashScope API. Supports Text-to-Video (T2V), Image-to-Video (I2V), and Reference-to-Video (R2V) modes with automatic prompt enhancement and local file delivery."
}
```

- [ ] **Step 2: Commit**

```bash
git add .claude-plugin/marketplace.json
git commit -m "feat: register ali-video skill in marketplace"
```

---

### Task 7: Update plugin.json keywords

**Files:**
- Modify: `.claude-plugin/plugin.json`

Add relevant keywords for the new ali-video skill.

- [ ] **Step 1: Add keywords**

Add these keywords to the existing `keywords` array: `"aliyun"`, `"dashscope"`, `"happyhorse"`.

- [ ] **Step 2: Commit**

```bash
git add .claude-plugin/plugin.json
git commit -m "feat: add ali-video related keywords to plugin metadata"
```

---

## Self-Review

### 1. Spec Coverage

| Requirement | Task |
|------------|------|
| Reference tl-video front-end logic | Tasks 2, 3 (mirrored structure: auth, video gen, polling, download, heartbeat, output) |
| Request to Aliyun Bailian (DashScope) | Task 3 (ali_video.py uses DASHSCOPE endpoints) |
| HappyHorse-1.0-T2V model | Task 3 (MODEL_T2V, T2V workflow in SKILL.md Task 5) |
| HappyHorse-1.0-I2V model | Task 3 (MODEL_I2V, I2V workflow in SKILL.md Task 5) |
| HappyHorse-1.0-R2V model | Task 3 (MODEL_R2V, R2V workflow in SKILL.md Task 5) |
| Skill registration | Task 6 (marketplace.json) |

### 2. Placeholder Scan

No TBD/TODO/placeholders found. All code is complete.

### 3. Type Consistency

- `generate_video()` returns `str` (task_id) - matches `wait_and_download()` parameter `task_id: str`
- `query_task_status()` returns `Optional[dict]` - checked for `None` in `wait_and_download()`
- Model constants `MODEL_T2V`, `MODEL_I2V`, `MODEL_R2V` used consistently across `ali_video.py`
- CLI `--model` choices use short names `t2v/i2v/r2v`, mapped to full model IDs via `model_map` dict
