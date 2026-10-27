"""Command line interface for SheetSync."""
from __future__ import annotations

import argparse
import logging
import sys

from .sync import sync_to_google_sheet

logger = logging.getLogger("sheetsync")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sheetsync",
        description="Upload local CSV data directly to a Google Sheet.",
    )
    parser.add_argument(
        "csv_path", 
        help="Path to the local CSV file you want to upload"
    )
    parser.add_argument(
        "-s", "--sheet-id", 
        required=True, 
        help="The ID of the Google Sheet (found in the URL)"
    )
    parser.add_argument(
        "-c", "--credentials", 
        default="credentials.json", 
        help="Path to your Google service account JSON file (default: credentials.json)"
    )
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="Enable debug logging"
    )
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(message)s",
        datefmt="%H:%M:%S",
    )

    try:
        sync_to_google_sheet(
            csv_path=args.csv_path,
            sheet_id=args.sheet_id,
            credentials_path=args.credentials
        )
    except Exception as exc:
        logger.error("Error: %s", exc)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())