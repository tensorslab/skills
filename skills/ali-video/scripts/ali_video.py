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
import base64
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

from ali_auth import (  # noqa: E402
    get_or_prompt_api_key,
    save_api_key_to_env,
    AliAPIKeyError,
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

# Supported image formats and their MIME types
_IMAGE_MIME_MAP = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}


def resolve_image_input(image_input: str) -> str:
    """
    Resolve image input to a URL or base64 data URL.

    Accepts:
      - HTTP/HTTPS URL (returned as-is)
      - Base64 data URL (data:image/...;base64,...) (returned as-is)
      - Local file path (converted to base64 data URL)

    Returns:
        A URL or data URL string suitable for the API.
    """
    # Already a URL
    if image_input.startswith("http://") or image_input.startswith("https://"):
        return image_input

    # Already a base64 data URL
    if image_input.startswith("data:"):
        return image_input

    # Treat as local file path
    file_path = Path(image_input).expanduser().resolve()

    if not file_path.exists():
        raise AliVideoAPIError(f"Image file not found: {image_input}")

    ext = file_path.suffix.lower()
    mime_type = _IMAGE_MIME_MAP.get(ext)
    if not mime_type:
        raise AliVideoAPIError(
            f"Unsupported image format: {ext}. Supported: {', '.join(_IMAGE_MIME_MAP.keys())}"
        )

    file_size = file_path.stat().st_size
    if file_size > 20 * 1024 * 1024:
        raise AliVideoAPIError(f"Image file too large: {file_size / (1024*1024):.1f}MB (max 20MB)")

    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    logger.info(f"Converted local image to base64: {file_path.name} ({file_size / 1024:.0f}KB)")
    return f"data:{mime_type};base64,{encoded}"


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
    watermark: bool = False,
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
        watermark: Whether to add watermark (default False).
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
        "X-DashScope-DataInspection": '{"input":"disable","output":"disable"}',
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
    body["parameters"]["watermark"] = watermark

    # Build input based on model
    if model == MODEL_T2V:
        body["input"]["prompt"] = prompt

    elif model == MODEL_I2V:
        if not image_url:
            raise AliVideoAPIError("I2V model requires --image-url parameter")
        resolved_url = resolve_image_input(image_url)
        body["input"]["prompt"] = prompt
        body["input"]["media"] = [
            {"type": "first_frame", "url": resolved_url}
        ]

    elif model == MODEL_R2V:
        if not reference_images or len(reference_images) == 0:
            raise AliVideoAPIError("R2V model requires at least one --reference-image URL")
        body["input"]["prompt"] = prompt
        body["input"]["media"] = [
            {"type": "reference_image", "url": resolve_image_input(url)}
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
            # Detect auth failures
            if response.status_code in (401, 403) or error_code in ("InvalidApiKey", "Forbidden"):
                raise AliAPIKeyError(
                    f"API key invalid or expired: {error_msg} (Code: {error_code}). "
                    "Get a new key from https://bailian.console.aliyun.com/ "
                    "and set via: --api-key YOUR_KEY"
                )
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
    logger.info("   (This may take 1-5 minutes, longer for 15s videos - please be patient)")

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

    elapsed = int(time.time() - start_time)
    msg = (
        f"Timeout waiting for task completion (waited {timeout}s).\n"
        f"Task ID: {task_id}\n"
        f"Use the query script to check status later:\n"
        f"  python ali_query_task.py {task_id}"
    )
    logger.error(msg)
    print(json.dumps({"ok": False, "error": "timeout", "task_id": task_id, "elapsed": elapsed}, ensure_ascii=False))
    raise AliVideoAPIError(msg)


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
                        help="Image for I2V first frame: URL, base64 data URL, or local file path")
    parser.add_argument("--reference-image", action="append", dest="reference_images",
                        help="Reference image for R2V: URL, base64 data URL, or local file path (can specify 1-9 times)")
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    parser.add_argument("--watermark", type=str, choices=["true", "false"], default="false",
                        help="Enable watermark: true/false (default: false)")
    parser.add_argument("--api-key", help="DashScope API key (saved to .env file for future use)")
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
            watermark=args.watermark == "true",
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

        # Persist API key to .env for future sessions
        if args.api_key:
            save_api_key_to_env(args.api_key)

    except AliAPIKeyError as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    except AliVideoAPIError as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
