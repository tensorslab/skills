#!/usr/bin/env python3
"""
TensorsLab Video Generation API Client

Supports text-to-video and image-to-video generation using TensorsLab's models.
"""

import os
import sys
import time
import json
import argparse
import logging
from pathlib import Path
from urllib.parse import urlparse
from typing import Optional, List

try:
    import requests
except ImportError:
    logger.error("Error: requests module is required. Install with: pip install requests")
    sys.exit(1)


logger = logging.getLogger(__name__)

# API Configuration
BASE_URL = "https://test.tensorai.tensorslab.com"
OUTPUT_DIR = Path("./tensorslab_output")

# Task status codes
TASK_STATUS = {
    1: "Pending",
    2: "Processing",
    3: "Completed",
    4: "Failed",
    5: "Uploading"
}

# Response codes
RESPONSE_CODES = {
    1000: "Success",
    9000: "Insufficient Credits",
    9999: "Error"
}


def get_api_key() -> str:
    """Get API key from environment variable."""
    api_key = os.environ.get("TENSORAI_API_KEY")
    if not api_key:
        logger.error("Error: TENSORAI_API_KEY environment variable is not set.")
        logger.info("\nTo get your API key:")
        logger.info("1. Visit https://tensorai.tensorslab.com/ and subscribe")
        logger.info("2. Get your API Key from the console")
        logger.info("3. Set the environment variable:")
        logger.info("   - Windows (PowerShell): $env:TENSORAI_API_KEY=\"your-key-here\"")
        logger.info("   - Mac/Linux: export TENSORAI_API_KEY=\"your-key-here\"")
        sys.exit(1)
    return api_key


def ensure_output_dir():
    """Create output directory if it doesn't exist."""
    OUTPUT_DIR.mkdir(exist_ok=True)


def download_video(url: str, output_path: Path) -> bool:
    """Download a video from URL to local path."""
    try:
        response = requests.get(url, timeout=300, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))

        with open(output_path, 'wb') as f:
            if total_size > 0:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        percent = (downloaded / total_size) * 100
                        logger.info(f"\r📥 Downloading: {percent:.1f}%")
            else:
                f.write(response.content)

        logger.info(f"\r✅ Download complete: {output_path}")
        return True
    except Exception as e:
        logger.warning(f"\r⚠️ Failed to download video from {url}: {e}")
        return False


def generate_video(
    prompt: str,
    model: str = "seedancev1profast",
    ratio: str = "9:16",
    duration: int = 5,
    resolution: str = "1080p",
    fps: str = "24",
    source_images: Optional[List[str]] = None,
    image_url: Optional[str] = None,
    camerafixed: bool = False,
    generate_audio: bool = False,
    return_last_frame: bool = False,
    seed: Optional[int] = None,
    api_key: Optional[str] = None
) -> str:
    """
    Generate a video using TensorsLab API.

    Args:
        prompt: Text prompt for video generation
        model: Model to use (seedancev1, seedancev15pro, seedancev1profast, seedancev2)
        ratio: Video aspect ratio (9:16, 16:9, etc.)
        duration: Video duration in seconds (5-15)
        resolution: Video resolution (480p, 720p, 1080p, 1440p)
        fps: Frame rate
        source_images: List of local image paths for image-to-video (1-2 images)
        image_url: URL of source image for image-to-video
        camerafixed: Keep camera fixed (for stable scenes)
        generate_audio: Generate audio with video (seedancev2 only)
        return_last_frame: Return the last frame image
        seed: Random seed for reproducibility
        api_key: TensorsLab API key (uses env var if not provided)

    Returns:
        Task ID for tracking generation status
    """
    if api_key is None:
        api_key = get_api_key()

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    # Prepare multipart form data (like curl -F)
    # Format: {'fieldname': (None, 'value')} for text fields
    files = {
        "prompt": (None, prompt),
        "ratio": (None, ratio),
        "duration": (None, str(duration)),
        "resolution": (None, resolution),
        "fps": (None, fps),
    }

    # Add optional parameters
    if seed is not None:
        files["seed"] = (None, str(seed))
    if camerafixed:
        files["camerafixed"] = (None, "1")
    if generate_audio and model == "seedancev2":
        files["generate_audio"] = (None, "1")
    if return_last_frame and model == "seedancev2":
        files["return_last_frame"] = (None, "1")

    # Prepare files for image-to-video
    opened_files = []
    if source_images:
        for i, img_path in enumerate(source_images[:2]):  # Max 2 images
            f = open(img_path, "rb")
            opened_files.append(f)
            files["sourceImage"] = (os.path.basename(img_path), f)
    elif image_url:
        files["imageUrl"] = (None, image_url)

    # Determine endpoint
    endpoint_map = {
        "seedancev1": f"{BASE_URL}/v1/video/seedancev1",
        "seedancev15pro": f"{BASE_URL}/v1/video/seedancev15pro",
        "seedancev1profast": f"{BASE_URL}/v1/video/seedancev1profast",
        "seedancev2": f"{BASE_URL}/v1/video/seedancev2",
    }

    endpoint = endpoint_map.get(model, f"{BASE_URL}/v1/video/seedancev2")

    try:
        logger.info(f"🎬 Generating video using {model}...")
        logger.info(f"📝 Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
        logger.info(f"⚙️ Settings: {ratio} @ {resolution}, {duration}s, {fps}fps")

        response = requests.post(
            endpoint,
            headers=headers,
            files=files,
            timeout=60
        )

        # Close any opened files
        for f in opened_files:
            f.close()

        result = response.json()

        if result.get("code") == 1000:
            task_id = result.get("data", {}).get("taskid")
            logger.info(f"✅ Task created successfully! Task ID: {task_id}")
            return task_id
        else:
            error_msg = result.get("msg", "Unknown error")
            error_code = result.get("code")
            if error_code == 9000:
                logger.error("❌ Error: Insufficient credits. Please top up at https://tensorslab.tensorslab.com/")
            else:
                logger.error(f"❌ Error: {error_msg} (Code: {error_code})")
            sys.exit(1)

    except requests.exceptions.RequestException as e:
        logger.exception(f"❌ Network error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"❌ Unexpected error: {e}")
        sys.exit(1)


def query_task_status(task_id: str, api_key: Optional[str] = None, more_info: bool = False) -> dict:
    """
    Query the status of a video generation task.

    Args:
        task_id: Task ID to query
        api_key: TensorsLab API key (uses env var if not provided)
        more_info: Whether to request more detailed task information

    Returns:
        Task status information
    """
    if api_key is None:
        api_key = get_api_key()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    endpoint = f"{BASE_URL}/v1/video/infobytaskid"

    try:
        response = requests.post(
            endpoint,
            headers=headers,
            json={"taskid": task_id, "moreTaskInfo": more_info},
            timeout=30
        )

        result = response.json()

        if result.get("code") == 1000:
            return result.get("data", {})
        else:
            logger.error(f"❌ Error querying task: {result.get('msg', 'Unknown error')}")
            return None

    except Exception as e:
        logger.exception(f"❌ Error querying task status: {e}")
        return None


def wait_and_download(
    task_id: str,
    api_key: Optional[str] = None,
    poll_interval: int = 10,
    timeout: int = 1800
) -> List[str]:
    """
    Wait for task completion and download generated videos.

    Args:
        task_id: Task ID to wait for
        api_key: TensorsLab API key (uses env var if not provided)
        poll_interval: Seconds between status checks
        timeout: Maximum seconds to wait (default 30 minutes)

    Returns:
        List of downloaded file paths
    """
    if api_key is None:
        api_key = get_api_key()

    ensure_output_dir()
    downloaded_files = []
    start_time = time.time()

    logger.info(f"⏳ Waiting for video generation to complete...")
    logger.info(f"   (This may take several minutes - please be patient)")

    last_heartbeat = 0

    while time.time() - start_time < timeout:
        task_data = query_task_status(task_id, api_key)

        if not task_data:
            time.sleep(poll_interval)
            continue

        status = task_data.get("task_status")
        status_text = TASK_STATUS.get(status, "Unknown")
        elapsed = int(time.time() - start_time)

        # Heartbeat every 60 seconds to show progress
        if elapsed - last_heartbeat >= 60 or status == 3:
            if status == 2:
                logger.info(f"🚀 正在渲染电影级大片，已耗时 {elapsed} 秒，请稍安勿躁...")
                last_heartbeat = elapsed

        logger.info(f"🔄 Status: {status_text} (elapsed: {elapsed}s)")

        if status == 3:  # Completed
            logger.info(f"\n✅ Task completed!")
            urls = task_data.get("url", [])

            if not urls:
                logger.warning("⚠️ No videos returned")
                return downloaded_files

            for i, url in enumerate(urls):
                url_path = urlparse(url).path
                ext = Path(url_path).suffix
                if not ext or len(ext) > 5:
                    ext = ".mp4"
                filename = f"{task_id}_{i}{ext}"
                output_path = OUTPUT_DIR / filename

                logger.info(f"📥 Downloading video {i+1}/{len(urls)}: {output_path}")
                if download_video(url, output_path):
                    downloaded_files.append(str(output_path))

            return downloaded_files

        elif status == 4:  # Failed
            error_msg = task_data.get("message", "Unknown error")
            logger.error(f"\n❌ Task failed: {error_msg}")
            sys.exit(1)

        time.sleep(poll_interval)

    logger.error(f"\n⏱️ Timeout waiting for task completion")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Generate videos using TensorsLab API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text-to-video (default settings)
  python tensorslab_video.py "a spaceship flying through space"

  # Specify duration and aspect ratio
  python tensorslab_video.py "sunset over ocean waves" --duration 10 --ratio 16:9

  # Image-to-video with local file
  python tensorslab_video.py "make this photo come alive" --source photo.jpg

  # Use faster model
  python tensorslab_video.py "abstract flowing colors" --model seedancev1profast

  # High quality video
  python tensorslab_video.py "epic mountain timelapse" --resolution 1440p --duration 10

  # Fixed camera for stable scene
  python tensorslab_video.py "portrait talking to camera" --source face.jpg --camera-fixed
        """
    )

    parser.add_argument("prompt", help="Text prompt for video generation")
    parser.add_argument("--model", "-m",
                       choices=["seedancev1", "seedancev15pro", "seedancev1profast", "seedancev2"],
                       default="seedancev1profast",
                       help="Model to use (default: seedancev1profast - fast and good quality)")
    parser.add_argument("--ratio", "-r", default="9:16",
                       help="Video aspect ratio (default: 9:16 vertical)")
    parser.add_argument("--duration", "-d", type=int, default=5,
                       help="Video duration in seconds (5-15, default: 5)")
    parser.add_argument("--resolution", choices=["480p", "720p", "1080p", "1440p"],
                       default="1080p", help="Video resolution (default: 1080p)")
    parser.add_argument("--fps", "-f", default="24",
                       help="Frame rate (default: 24)")
    parser.add_argument("--source", "-s", action="append", dest="sources",
                       help="Source image path for image-to-video (can use 1-2 images)")
    parser.add_argument("--image-url", help="Source image URL for image-to-video")
    parser.add_argument("--camera-fixed", action="store_true",
                       help="Keep camera fixed for stable scenes")
    parser.add_argument("--audio", action="store_true",
                       help="Generate audio with video (seedancev2 only)")
    parser.add_argument("--last-frame", action="store_true",
                       help="Return the last frame as image (seedancev2 only)")
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    parser.add_argument("--api-key", help="TensorsLab API key (uses TENSORAI_API_KEY env var if not set)")
    parser.add_argument("--poll-interval", type=int, default=10,
                       help="Status check interval in seconds (default: 10)")
    parser.add_argument("--timeout", type=int, default=1800,
                       help="Maximum wait time in seconds (default: 1800 = 30 minutes)")

    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level, format="%(asctime)s - %(levelname)s - %(message)s")

    # Validate duration based on model
    max_duration = 15 if args.model == "seedancev2" else 10
    if args.duration < 5 or args.duration > max_duration:
        logger.error(f"❌ Error: duration must be between 5 and {max_duration} seconds for {args.model}")
        sys.exit(1)

    # Validate source images count
    if args.sources and len(args.sources) > 2:
        logger.error("❌ Error: maximum 2 source images allowed")
        sys.exit(1)

    # Generate video
    task_id = generate_video(
        prompt=args.prompt,
        model=args.model,
        ratio=args.ratio,
        duration=args.duration,
        resolution=args.resolution,
        fps=args.fps,
        source_images=args.sources,
        image_url=args.image_url,
        camerafixed=args.camera_fixed,
        generate_audio=args.audio,
        return_last_frame=args.last_frame,
        seed=args.seed,
        api_key=args.api_key
    )

    # Wait and download
    downloaded = wait_and_download(
        task_id=task_id,
        api_key=args.api_key,
        poll_interval=args.poll_interval,
        timeout=args.timeout
    )

    logger.info(f"\n🎉 您的视频处理完毕！已存放于 {OUTPUT_DIR}/")
    for f in downloaded:
        logger.info(f"   - {f}")


if __name__ == "__main__":
    main()
