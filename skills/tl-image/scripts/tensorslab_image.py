#!/usr/bin/env python3
"""
TensorsLab Image Generation API Client

Supports text-to-image and image-to-image generation using TensorsLab's models.
"""

import os
import sys
import time
import json
import argparse
import logging
import mimetypes
from pathlib import Path
from urllib.parse import urlparse
from typing import Optional, List

try:
    import requests
except ImportError:
    logger = logging.getLogger(__name__)
    logger.error("Error: requests module is required. Install with: pip install requests")
    sys.exit(1)

# 禁用代理仅限当前 session，不影响进程级环境变量
_SESSION = requests.Session()
_SESSION.proxies = {"http": "", "https": ""}


class TensorsLabAPIError(Exception):
    """TensorsLab API error with context."""
    pass


logger = logging.getLogger(__name__)

# API Configuration
BASE_URL = "https://api.tensorslab.com"
DEFAULT_OUTPUT_DIR = Path(".") / "tensorslab_output"

# Image status codes
IMAGE_STATUS = {
    1: "Queued",
    2: "Processing",
    3: "Completed",
    4: "Failed"
}

# Response codes
RESPONSE_CODES = {
    1000: "Success",
    9000: "Insufficient Credits",
    9999: "Error"
}


def get_api_key() -> str:
    """Get API key from environment variable."""
    api_key = os.environ.get("TENSORSLAB_API_KEY")
    if not api_key:
        raise TensorsLabAPIError(
            "TENSORSLAB_API_KEY environment variable is not set.\n"
            "To get your API key:\n"
            "1. Visit https://tensorslab.tensorslab.com/ and subscribe\n"
            "2. Get your API Key from the console\n"
            "3. Set the environment variable:\n"
            "   - Windows (PowerShell): $env:TENSORSLAB_API_KEY=\"your-key-here\"\n"
            "   - Mac/Linux: export TENSORSLAB_API_KEY=\"your-key-here\""
        )
    return api_key


def ensure_output_dir(output_dir: Path):
    """Create output directory if it doesn't exist."""
    output_dir.mkdir(parents=True, exist_ok=True)


def download_image(url: str, output_path: Path) -> Path:
    """Download an image from URL to local path."""
    try:
        response = _SESSION.get(url, timeout=30)
        response.raise_for_status()

        content_type = response.headers.get('content-type', '').split(';')[0].strip()
        ext = mimetypes.guess_extension(content_type)
        if ext == '.jpe':
            ext = '.jpg'

        if not ext:
            ext = Path(urlparse(url).path).suffix

        if not ext or len(ext) > 6:
            ext = '.png'

        final_path = output_path.with_suffix(ext)
        with open(final_path, 'wb') as f:
            f.write(response.content)
        return final_path
    except Exception as e:
        logger.warning(f"Warning: Failed to download image from {url}: {e}")
        return None


def generate_image(
    prompt: str,
    model: str = "seedreamv4",
    resolution: str = "2K",
    source_images: Optional[List[str]] = None,
    image_url: Optional[str] = None,
    api_key: Optional[str] = None
) -> str:
    """
    Generate an image using TensorsLab API.

    Args:
        prompt: Text prompt for image generation
        model: Model to use (seedreamv4, seedreamv45, zimage)
        resolution: Image resolution (aspect ratio like "16:9", "1:1", or level like "2K", "4K", or WxH like "2048x2048")
        source_images: List of local image paths for image-to-image
        image_url: URL of source image for image-to-image
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
    # Format: [("fieldname", (None, "value"))] for text fields
    files = [
        ("prompt", (None, prompt)),
        ("resolution", (None, resolution)),
    ]

    # Add model-specific parameters
    if model in ["seedreamv4", "seedreamv45"]:
        files.append(("category", (None, model)))
    elif model == "zimage":
        # Enable prompt extension
        files.append(("prompt_extend", (None, "1")))

    # Handle image-to-image source images
    opened_files = []
    if source_images:
        for img_path in source_images:
            f = open(img_path, "rb")
            opened_files.append(f)
            files.append(("sourceImage", (os.path.basename(img_path), f)))
    elif image_url:
        files.append(("imageUrl", (None, image_url)))

    # Determine endpoint
    if model == "zimage":
        endpoint = f"{BASE_URL}/v1/images/zimage"
    elif model == "seedreamv4":
        endpoint = f"{BASE_URL}/v1/images/seedreamv4"
    else:  # seedreamv45 (default)
        endpoint = f"{BASE_URL}/v1/images/seedreamv45"

    try:
        logger.info(f"🎨 Generating image using {model}...")
        logger.info(f"📝 Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")

        response = _SESSION.post(endpoint, headers=headers, files=files, timeout=60)

        for f in opened_files:
            f.close()
        logger.debug(f"API Response ({response.status_code}): {response.text}")

        try:
            result = response.json()
        except ValueError:
            raise TensorsLabAPIError(f"Invalid JSON response (HTTP {response.status_code}): {response.text}")

        if result.get("code") == 1000:
            task_id = result.get("data", {}).get("taskid")
            logger.info(f"✅ Task created successfully! Task ID: {task_id}")
            return task_id
        else:
            error_msg = result.get("msg", "Unknown error")
            error_code = result.get("code")
            if error_code == 9000:
                raise TensorsLabAPIError("Insufficient credits. Please top up at https://tensorslab.tensorslab.com/")
            raise TensorsLabAPIError(f"{error_msg} (Code: {error_code})")

    except TensorsLabAPIError:
        raise
    except requests.exceptions.RequestException as e:
        raise TensorsLabAPIError(f"Network error: {e}") from e


def query_task_status(task_id: str, api_key: Optional[str] = None) -> dict:
    """
    Query the status of an image generation task.

    Args:
        task_id: Task ID to query
        api_key: TensorsLab API key (uses env var if not provided)

    Returns:
        Task status information
    """
    if api_key is None:
        api_key = get_api_key()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    endpoint = f"{BASE_URL}/v1/images/infobytaskid"

    try:
        response = _SESSION.post(endpoint, headers=headers, json={"taskid": task_id}, timeout=30)

        try:
            result = response.json()
        except ValueError:
            logger.error(f"❌ API Error: Invalid JSON response (HTTP {response.status_code}): {response.text}")
            return None

        if result.get("code") == 1000:
            return result.get("data", {})

        logger.error(f"❌ Error querying task: {result.get('msg', 'Unknown error')}")
        return None

    except Exception as e:
        logger.error(f"❌ Error querying task status: {e}")
        return None


def wait_and_download(
    task_id: str,
    api_key: Optional[str] = None,
    poll_interval: int = 5,
    timeout: int = 300,
    output_dir: Optional[Path] = None
) -> List[str]:
    """
    Wait for task completion and download generated images.

    Args:
        task_id: Task ID to wait for
        api_key: TensorsLab API key (uses env var if not provided)
        poll_interval: Seconds between status checks
        timeout: Maximum seconds to wait
        output_dir: Output directory path (default: ./tensorslab_output)

    Returns:
        List of downloaded file paths
    """
    if api_key is None:
        api_key = get_api_key()
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR

    ensure_output_dir(output_dir)
    downloaded_files = []
    start_time = time.time()

    logger.info(f"⏳ Waiting for image generation to complete...")

    while time.time() - start_time < timeout:
        task_data = query_task_status(task_id, api_key)

        if not task_data:
            time.sleep(poll_interval)
            continue

        status = task_data.get("image_status")
        status_text = IMAGE_STATUS.get(status, "Unknown")

        elapsed = int(time.time() - start_time)
        logger.info(f"🔄 Status: {status_text} (elapsed: {elapsed}s)")

        if status == 3:  # Completed
            logger.info(f"\n✅ Task completed!")
            urls = task_data.get("url", [])

            if not urls:
                logger.warning("⚠️ No images returned")
                return downloaded_files

            for i, url in enumerate(urls):
                filename = f"{task_id}_{i}"
                output_path = output_dir / filename

                logger.info(f"📥 Downloading image {i+1}/{len(urls)}")
                final_path = download_image(url, output_path)
                if final_path:
                    downloaded_files.append(str(final_path))

            return downloaded_files

        elif status == 4:  # Failed
            error_msg = task_data.get("error_message", "Unknown error")
            raise TensorsLabAPIError(f"Task failed: {error_msg}")

        time.sleep(poll_interval)

    raise TensorsLabAPIError(f"Timeout waiting for task completion (waited {timeout}s)")


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using TensorsLab API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text-to-image
  python tensorslab_image.py "a cat on the moon"

  # Image-to-image with local file
  python tensorslab_image.py "make this look like a watercolor painting" --source cat.png

  # Specify model and resolution
  python tensorslab_image.py "a sunset over mountains" --model seedreamv45 --resolution 16:9
        """
    )

    parser.add_argument("prompt", help="Text prompt for image generation")
    parser.add_argument("--model", "-m", choices=["seedreamv4", "seedreamv45", "zimage"],
                       default="seedreamv4", help="Model to use (default: seedreamv4)")
    parser.add_argument("--resolution", "-r", default="2K",
                       help="Resolution: aspect ratio (9:16, 16:9, 1:1, etc.), level (2K, 4K), or WxH")
    parser.add_argument("--source", "-s", action="append", dest="sources",
                       help="Source image path for image-to-image (can be used multiple times)")
    parser.add_argument("--image-url", help="Source image URL for image-to-image")
    parser.add_argument("--api-key", help="TensorsLab API key (uses TENSORSLAB_API_KEY env var if not set)")
    parser.add_argument("--poll-interval", type=int, default=5,
                       help="Status check interval in seconds (default: 5)")
    parser.add_argument("--timeout", type=int, default=300,
                       help="Maximum wait time in seconds (default: 300)")
    parser.add_argument("--output-dir", "-o", type=str, default=None,
                       help="Output directory path (default: ./tensorslab_output)")

    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level, format="%(asctime)s - %(levelname)s - %(message)s")

    # Setup output directory
    output_dir = DEFAULT_OUTPUT_DIR
    if args.output_dir:
        output_dir = Path(args.output_dir)

    try:
        # Generate image
        task_id = generate_image(
            prompt=args.prompt,
            model=args.model,
            resolution=args.resolution,
            source_images=args.sources,
            image_url=args.image_url,
            api_key=args.api_key
        )

        # Wait and download
        downloaded = wait_and_download(
            task_id=task_id,
            api_key=args.api_key,
            poll_interval=args.poll_interval,
            timeout=args.timeout,
            output_dir=output_dir
        )

        logger.info(f"\n🎉 All done! Downloaded {len(downloaded)} image(s) to {output_dir}/")
        for f in downloaded:
            logger.info(f"   - {f}")
    except TensorsLabAPIError as e:
        logger.error(f"❌ {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
