#!/usr/bin/env python3
"""
TensorsLab Image Generation API Client

Supports text-to-image and image-to-image generation using TensorsLab's models.
"""

import os
import sys

# Disable proxy for TensorsLab API to avoid SSL renegotiation issues
# Must be done before importing requests
for proxy_var in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY']:
    os.environ.pop(proxy_var, None)

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
    logger = logging.getLogger(__name__)
    logger.error("Error: requests module is required. Install with: pip install requests")
    sys.exit(1)


logger = logging.getLogger(__name__)

# API Configuration
BASE_URL = "https://test.tensorai.tensorslab.com"
OUTPUT_DIR = Path.home() / "tensorslab_output"

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
        logger.error("Error: TENSORSLAB_API_KEY environment variable is not set.")
        logger.info("\nTo get your API key:")
        logger.info("1. Visit https://tensorslab.tensorslab.com/ and subscribe")
        logger.info("2. Get your API Key from the console")
        logger.info("3. Set the environment variable:")
        logger.info("   - Windows (PowerShell): $env:TENSORSLAB_API_KEY=\"your-key-here\"")
        logger.info("   - Mac/Linux: export TENSORSLAB_API_KEY=\"your-key-here\"")
        sys.exit(1)
    return api_key


def ensure_output_dir():
    """Create output directory if it doesn't exist."""
    OUTPUT_DIR.mkdir(exist_ok=True)


def download_image(url: str, output_path: Path) -> Path:
    """Download an image from URL to local path."""
    import mimetypes
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # 获取真实的Content-Type扩展名
        content_type = response.headers.get('content-type', '').split(';')[0].strip()
        ext = mimetypes.guess_extension(content_type)
        if ext == '.jpe':
            ext = '.jpg'
            
        if not ext:
            url_path = urlparse(url).path
            ext = Path(url_path).suffix
            
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

        response = requests.post(
            endpoint,
            headers=headers,
            files=files,
            timeout=60
        )

        # Close any opened files
        for f in opened_files:
            f.close()
        logger.debug(f"API Response ({response.status_code}): {response.text}")
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
        response = requests.post(
            endpoint,
            headers=headers,
            json={"taskid": task_id},
            timeout=30
        )

        result = response.json()

        if result.get("code") == 1000:
            return result.get("data", {})
        else:
            logger.error(f"❌ Error querying task: {result.get('msg', 'Unknown error')}")
            return None

    except Exception as e:
        logger.error(f"❌ Error querying task status: {e}")
        return None


def wait_and_download(
    task_id: str,
    api_key: Optional[str] = None,
    poll_interval: int = 5,
    timeout: int = 300
) -> List[str]:
    """
    Wait for task completion and download generated images.

    Args:
        task_id: Task ID to wait for
        api_key: TensorsLab API key (uses env var if not provided)
        poll_interval: Seconds between status checks
        timeout: Maximum seconds to wait

    Returns:
        List of downloaded file paths
    """
    if api_key is None:
        api_key = get_api_key()

    ensure_output_dir()
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
                output_path = OUTPUT_DIR / filename

                logger.info(f"📥 Downloading image {i+1}/{len(urls)}")
                final_path = download_image(url, output_path)
                if final_path:
                    downloaded_files.append(str(final_path))

            return downloaded_files

        elif status == 4:  # Failed
            error_msg = task_data.get("error_message", "Unknown error")
            logger.error(f"\n❌ Task failed: {error_msg}")
            sys.exit(1)

        time.sleep(poll_interval)

    logger.error(f"\n⏱️ Timeout waiting for task completion")
    sys.exit(1)


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

    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level, format="%(asctime)s - %(levelname)s - %(message)s")

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
        timeout=args.timeout
    )

    logger.info(f"\n🎉 All done! Downloaded {len(downloaded)} image(s) to {OUTPUT_DIR}/")
    for f in downloaded:
        logger.info(f"   - {f}")


if __name__ == "__main__":
    main()
