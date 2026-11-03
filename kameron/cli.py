"""Command-line interface for Kameron."""

import argparse
import sys


def main() -> None:
    parser = argparse.ArgumentParser(prog="kameron", description="RVC voice conversion tools")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("server", help="Start the HTTP API server")
    live_parser = subparsers.add_parser("live", help="Start live microphone conversion")
    live_parser.add_argument("live_args", nargs=argparse.REMAINDER)

    args = parser.parse_args()

    if args.command == "server":
        from .api import main as server_main

        server_main()
    elif args.command == "live":
        from .live import main as live_main

        sys.argv = [f"{parser.prog} live", *args.live_args]
        live_main()
