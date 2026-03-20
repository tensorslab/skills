#!/usr/bin/env python3
"""
TensorsLab Authorization Module

Provides browser-based OAuth-like authorization flow for TensorsLab API.
Shared by both image and video generation skills.
"""

import os
import http.server
import urllib.parse
import webbrowser
from threading import Thread
import logging
import logging
import time
import requests
from pathlib import Path

logger = logging.getLogger(__name__)

# --- Common Session Setup ---
# 禁用代理仅限当前 session，不影响进程级环境变量
SESSION = requests.Session()
SESSION.proxies = {"http": "", "https": ""}

# Shared user configurations
API_BASE_URL = "https://api.tensorslab.com"
AUTH_BASE_URL = "https://tensorai.tensorslab.com/auth"
USER_CONFIG_DIR = os.path.expanduser("~/.tensorslab")
ENV_FILE_PATH = os.path.join(USER_CONFIG_DIR, ".env")
DEFAULT_OUTPUT_DIR = Path(".") / "tensorslab_output"


def ensure_output_dir(output_dir: Path):
    """Create output directory if it doesn't exist."""
    output_dir.mkdir(parents=True, exist_ok=True)


def get_api_key() -> str:
    """Get API key from environment variable or trigger authorization flow."""
    return get_or_authorize_api_key()


class AuthHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler for OAuth callback."""
    api_key = None

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        query_components = urllib.parse.parse_qs(post_data)

        if "token" in query_components:
            AuthHandler.api_key = query_components["token"][0]

            try:
                # Ensure config directory exists
                os.makedirs(os.path.dirname(ENV_FILE_PATH), exist_ok=True)

                # Get or update .env file's TENSORSLAB_API_KEY
                lines = []
                if os.path.exists(ENV_FILE_PATH):
                    with open(ENV_FILE_PATH, "r", encoding="utf-8") as f:
                        lines = f.readlines()

                new_lines = []
                key_updated = False
                for line in lines:
                    if line.startswith("TENSORSLAB_API_KEY="):
                        new_lines.append(f"TENSORSLAB_API_KEY={AuthHandler.api_key}\n")
                        key_updated = True
                    else:
                        new_lines.append(line)

                if not key_updated:
                    new_lines.append(f"TENSORSLAB_API_KEY={AuthHandler.api_key}\n")

                with open(ENV_FILE_PATH, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)

                logger.info(f"[Success] API Key saved to: {ENV_FILE_PATH}")
            except Exception as e:
                logger.error(f"[Error] Failed to save .env file: {e}")

            # Send response to browser
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            html_content = """
            <html><head><meta charset="utf-8"><title>Authorization Successful</title></head>
            <body style="font-family: Arial; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f0f2f5;">
            <div style="background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center;">
                <h1 style="color: #52c41a;">Authorization Successful!</h1>
                <p style="color: #666; font-size: 16px;">TensorsLab API Key has been synchronized to your local environment.</p>
                <p style="color: #999; font-size: 14px; margin-top: 20px;">You can safely close this window and return to the console.</p>
            </div></body></html>
            """
            self.wfile.write(html_content.encode("utf-8"))
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Bad Request: Missing token parameter")

    def log_message(self, format, *args):
        pass  # Suppress HTTP server logs


def start_auth_flow(key_name: str = "TENSORSLAB_API_KEY") -> str:
    """
    Start browser-based authorization flow.

    Returns:
        The API key received from the authorization callback.

    This function:
    1. Starts a local HTTP server on a dynamic port
    2. Opens the browser to the authorization page
    3. Waits for the callback with the API key
    4. Saves the key to ~/.tensorslab/.env
    5. Returns the API key
    """
    # Start HTTP server on dynamic port
    server = http.server.HTTPServer(('127.0.0.1', 0), AuthHandler)
    assigned_port = server.server_port

    server_thread = Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    callback_uri = f"http://127.0.0.1:{assigned_port}/callback"
    auth_url = f"{AUTH_BASE_URL}?redirect_uri={urllib.parse.quote(callback_uri)}&key_name={key_name}"

    logger.info("=" * 60)
    logger.info(f"[*] Starting browser authorization...")
    logger.info(f"[*] If the browser does not open automatically,")
    logger.info(f"[*] please copy and open the link below manually:")
    logger.info(f"[*] {auth_url}")
    logger.info("=" * 60)
    logger.info(f"[*] Listening on port: {assigned_port}...")

    try:
        webbrowser.open(auth_url)
    except Exception as e:
        logger.warning(f"[*] Failed to open browser automatically: {e}")

    while AuthHandler.api_key is None:
        time.sleep(0.5)

    logger.info(f"[*] Authorization complete, shutting down local server.")
    server.shutdown()
    return AuthHandler.api_key


def load_api_key_from_env() -> str | None:
    """
    Load API key from ~/.tensorslab/.env file.

    Returns:
        The API key if found and valid (non-empty), None otherwise.
    """
    if not os.path.exists(ENV_FILE_PATH):
        return None

    try:
        with open(ENV_FILE_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("TENSORSLAB_API_KEY="):
                    api_key = line.strip().split("=", 1)[1].strip()
                    # Return None if key is empty after stripping
                    if api_key:
                        return api_key
                    return None
    except Exception as e:
        logger.warning(f"Failed to read .env file: {e}")

    return None


def get_or_authorize_api_key(key_name: str = "TENSORSLAB_API_KEY") -> str:
    """
    Get API key from environment or trigger authorization flow.

    This function first checks if TENSORSLAB_API_KEY is set in the environment.
    If not, it checks ~/.tensorslab/.env file. If still not found, it triggers
    the browser-based authorization flow.

    Returns:
        The API key.
    """
    # First check environment variable
    api_key = os.environ.get("TENSORSLAB_API_KEY")
    if api_key:
        return api_key

    # Then check shared .env file
    api_key = load_api_key_from_env()
    if api_key:
        # Set it in environment for current session
        os.environ["TENSORSLAB_API_KEY"] = api_key
        return api_key

    # Trigger authorization flow
    logger.info("TENSORSLAB_API_KEY not found. Starting authorization flow...")
    api_key = start_auth_flow(key_name=key_name)
    os.environ["TENSORSLAB_API_KEY"] = api_key
    return api_key


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    api_key = get_or_authorize_api_key()
    if api_key:
        logger.info(f"[Success] API Key: {api_key[:4]}****{api_key[-4:]}")
