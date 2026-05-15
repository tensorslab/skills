#!/usr/bin/env python3
"""
Query Aliyun Bailian video generation task status and download result.

Usage:
  # Single query, just check status
  python ali_query_task.py TASK_ID

  # Poll until done (wait up to 10 minutes), download on success
  python ali_query_task.py TASK_ID --wait 600 --download

  # Poll with custom interval
  python ali_query_task.py TASK_ID --wait 600 --poll-interval 15 --download
"""

import os
import sys
import time
import json
import argparse
import logging
from pathlib import Path
from urllib.parse import urlparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from ali_auth import AliAPIKeyError, DEFAULT_OUTPUT_DIR  # noqa: E402
from ali_video import (  # noqa: E402
    query_task_status,
    download_video,
    save_url_mapping,
    AliVideoAPIError,
    TASK_STATUS_RUNNING,
    TASK_STATUS_SUCCEEDED,
    TASK_STATUS_FAILED,
    TASK_STATUS_UNKNOWN,
)

logger = logging.getLogger(__name__)


def poll_and_download(task_id, api_key, poll_interval, timeout, output_dir):
    """Poll task status until terminal state or timeout. Download on success."""
    start_time = time.time()
    last_heartbeat = 0
    last_status = None
    last_status_log = -999999

    while time.time() - start_time < timeout:
        output = query_task_status(task_id, api_key)

        if not output:
            time.sleep(poll_interval)
            continue

        status = output.get("task_status", "UNKNOWN")
        elapsed = int(time.time() - start_time)

        should_log = (status != last_status) or (elapsed - last_status_log >= 60)
        if should_log:
            logger.info(f"Status: {status} (elapsed: {elapsed}s)")
            last_status = status
            last_status_log = elapsed

        if status == TASK_STATUS_RUNNING and elapsed - last_heartbeat >= 60:
            logger.info(f"Video rendering in progress, elapsed {elapsed}s, please wait...")
            last_heartbeat = elapsed

        if status == TASK_STATUS_SUCCEEDED:
            logger.info("Task completed!")
            video_url = output.get("video_url")
            if not video_url:
                logger.warning("No video URL returned")
                print(json.dumps({"ok": True, "task_id": task_id, "status": status}, ensure_ascii=False))
                return

            output_dir.mkdir(parents=True, exist_ok=True)
            url_path = urlparse(video_url).path
            ext = Path(url_path).suffix
            if not ext or len(ext) > 5:
                ext = ".mp4"
            filename = f"{task_id}{ext}"
            output_path = output_dir / filename

            if download_video(video_url, output_path):
                save_url_mapping(output_dir, filename, video_url)
                logger.info(f"Video saved to: {output_path}")
                print(json.dumps({
                    "ok": True,
                    "task_id": task_id,
                    "status": status,
                    "file": str(output_path),
                    "url": video_url,
                }, ensure_ascii=False))
            return

        elif status == TASK_STATUS_FAILED:
            error_code = output.get("code", "Unknown")
            error_msg = output.get("message", "Unknown error")
            logger.error(f"Task failed: {error_msg} (Code: {error_code})")
            print(json.dumps({
                "ok": False,
                "task_id": task_id,
                "status": status,
                "error": f"{error_msg} (Code: {error_code})",
            }, ensure_ascii=False))
            return

        elif status == TASK_STATUS_UNKNOWN:
            logger.error("Task expired or not found (task_id may be older than 24 hours)")
            print(json.dumps({
                "ok": False,
                "task_id": task_id,
                "status": status,
                "error": "Task expired or not found",
            }, ensure_ascii=False))
            return

        time.sleep(poll_interval)

    elapsed = int(time.time() - start_time)
    logger.error(f"Timeout after {timeout}s. Task ID: {task_id}")
    logger.error(f"Retry later: python ali_query_task.py {task_id} --wait {timeout} --download")
    print(json.dumps({
        "ok": False,
        "error": "timeout",
        "task_id": task_id,
        "elapsed": elapsed,
    }, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description="Query Aliyun Bailian video task status, with optional polling and download",
    )
    parser.add_argument("task_id", help="Task ID to query")
    parser.add_argument("--wait", type=int, default=120,
                        help="Poll timeout in seconds, minimum 120 (default: 120). Pass 0 for single query.")
    parser.add_argument("--poll-interval", type=int, default=15,
                        help="Seconds between polls when --wait > 0 (default: 15)")
    parser.add_argument("--download", action="store_true",
                        help="Download video if task succeeded (auto-enabled when --wait > 0)")
    parser.add_argument("--output-dir", "-o", type=str, default=None,
                        help="Output directory (default: ./ali_output)")
    parser.add_argument("--api-key", help="DashScope API key")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level, format="%(asctime)s - %(levelname)s - %(message)s")

    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else Path(DEFAULT_OUTPUT_DIR).expanduser().resolve()

    # When polling, auto-download on success
    do_download = args.download or args.wait > 0

    try:
        if args.wait > 0:
            poll_and_download(args.task_id, args.api_key, args.poll_interval, args.wait, output_dir)
        else:
            # Single query
            output = query_task_status(args.task_id, args.api_key)
            if not output:
                logger.error("Failed to query task status")
                sys.exit(1)

            status = output.get("task_status", "UNKNOWN")
            print(json.dumps({
                "ok": True,
                "task_id": args.task_id,
                "status": status,
                "output": output,
            }, ensure_ascii=False, indent=2))

            if status == TASK_STATUS_SUCCEEDED and do_download:
                video_url = output.get("video_url")
                if not video_url:
                    logger.error("Task succeeded but no video_url found")
                    sys.exit(1)

                output_dir.mkdir(parents=True, exist_ok=True)
                url_path = urlparse(video_url).path
                ext = Path(url_path).suffix
                if not ext or len(ext) > 5:
                    ext = ".mp4"
                filename = f"{args.task_id}{ext}"
                output_path = output_dir / filename

                if download_video(video_url, output_path):
                    save_url_mapping(output_dir, filename, video_url)
                    logger.info(f"Video saved to: {output_path}")
                    print(json.dumps({
                        "ok": True,
                        "task_id": args.task_id,
                        "status": status,
                        "file": str(output_path),
                        "url": video_url,
                    }, ensure_ascii=False))

    except AliAPIKeyError as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    except AliVideoAPIError as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

    if args.api_key:
        from ali_auth import save_api_key_to_env
        save_api_key_to_env(args.api_key)


if __name__ == "__main__":
    main()
