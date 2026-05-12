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

# Resolve paths relative to the skill directory
# ali_auth.py is at skills/ali-video/scripts/ali_auth.py
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILL_DIR = os.path.dirname(_SCRIPT_DIR)      # skills/ali-video/
_SKILLS_DIR = os.path.dirname(_SKILL_DIR)       # skills/

ENV_FILE_PATH = os.path.join(_SKILLS_DIR, ".env")
DEFAULT_OUTPUT_DIR = Path(".") / "ali_output"

# DashScope API constants
DASHSCOPE_API_BASE = "https://dashscope.aliyuncs.com"
DASHSCOPE_VIDEO_ENDPOINT = f"{DASHSCOPE_API_BASE}/api/v1/services/aigc/video-generation/video-synthesis"
DASHSCOPE_TASK_ENDPOINT = f"{DASHSCOPE_API_BASE}/api/v1/tasks"


def load_api_key_from_env() -> str | None:
    """
    Load API key from .env file at skills directory.

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
    """Save API key to .env file at skills directory for future sessions."""
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
    Get API key from environment variable or .env file at skills directory.

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
