#!/usr/bin/env python3
"""
Aliyun DashScope API Key Management Module

Manages DASHSCOPE_API_KEY for Aliyun Bailian video generation.
Reads and writes key from/to ~/.ali/.env (user home directory).
"""

import os
import sys
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Store .env in user home directory at ~/.ali/.env (global, easy to find)
USER_CONFIG_DIR = os.path.expanduser("~/.ali")
ENV_FILE_PATH = os.path.join(USER_CONFIG_DIR, ".env")
DEFAULT_OUTPUT_DIR = Path(".") / "ali_output"

# DashScope API constants
DASHSCOPE_API_BASE = "https://dashscope.aliyuncs.com"
DASHSCOPE_VIDEO_ENDPOINT = f"{DASHSCOPE_API_BASE}/api/v1/services/aigc/video-generation/video-synthesis"
DASHSCOPE_TASK_ENDPOINT = f"{DASHSCOPE_API_BASE}/api/v1/tasks"


def load_api_key_from_env() -> str | None:
    """
    Load API key from ~/.ali/.env file.

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
    """Save API key to ~/.ali/.env file for future sessions."""
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


class AliAPIKeyError(Exception):
    """API key not found or invalid."""
    pass


def get_or_prompt_api_key() -> str:
    """
    Get API key from ~/.ali/.env file.

    Returns:
        The API key.

    Raises:
        AliAPIKeyError if no key is found.
    """
    api_key = load_api_key_from_env()
    if api_key:
        return api_key

    raise AliAPIKeyError(
        "DASHSCOPE_API_KEY not found. "
        "Get your key from https://bailian.console.aliyun.com/ "
        "and set via: --api-key YOUR_KEY"
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    api_key = get_or_prompt_api_key()
    if api_key:
        print(f"[Success] API Key: {api_key[:4]}****{api_key[-4:]}")
