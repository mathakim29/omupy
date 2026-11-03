"""Command-line interface for Kameron."""

import argparse
import os
import sys

from dotenv import load_dotenv


DEFAULT_API_HOST = "127.0.0.1"
DEFAULT_API_PORT = 8000
DEFAULT_API_RELOAD = False
DEFAULT_MODELS_DIR = "~/.local/rvc_app"


def _load_config() -> None:
    """Load CLI configuration before importing modules that initialize the engine."""
    load_dotenv()
    os.environ.setdefault("RVC_MODELS_DIR", DEFAULT_MODELS_DIR)


def _server_config() -> tuple[str, int, bool]:
    host = os.getenv("API_HOST", DEFAULT_API_HOST)
    port = int(os.getenv("API_PORT", str(DEFAULT_API_PORT)))
    reload = os.getenv("API_RELOAD", str(DEFAULT_API_RELOAD)).lower() in {
        "1", "true", "yes"
    }
    return host, port, reload


def main() -> None:
    _load_config()
    parser = argparse.ArgumentParser(prog="kameron", description="RVC voice conversion tools")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("server", help="Start the HTTP API server")
    live_parser = subparsers.add_parser("live", help="Start live microphone conversion")
    live_parser.add_argument("live_args", nargs=argparse.REMAINDER)

    args = parser.parse_args()

    if args.command == "server":
        from .api import main as server_main

        server_main(*_server_config())
    elif args.command == "live":
        from .live import main as live_main

        sys.argv = [f"{parser.prog} live", *args.live_args]
        live_main()
