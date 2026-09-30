#!/usr/bin/env python3
"""Extract messages and URLs from a Telegram Desktop JSON export."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from telegram_url_scraper.csv_export import write_csvs
from telegram_url_scraper.extractor import ExportError, extract_from_export, load_export


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract messages and URLs from a Telegram Desktop JSON export."
    )
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Path to a Telegram Desktop JSON export",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default=".",
        help="Directory for result.csv and urls.csv (default: current directory)",
    )
    parser.add_argument(
        "--messages",
        help="Write the messages CSV to this path instead of <output-dir>/result.csv",
    )
    parser.add_argument(
        "--urls",
        help="Write the URLs CSV to this path instead of <output-dir>/urls.csv",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print each extracted URL",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = extract_from_export(load_export(args.input))
    except ExportError as exc:
        print(exc, file=sys.stderr)
        return 1

    output_dir = Path(args.output_dir)
    messages_path = Path(args.messages) if args.messages else output_dir / "result.csv"
    urls_path = Path(args.urls) if args.urls else output_dir / "urls.csv"
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        messages_path.parent.mkdir(parents=True, exist_ok=True)
        urls_path.parent.mkdir(parents=True, exist_ok=True)
        write_csvs(result, messages_path, urls_path)
    except OSError as exc:
        print(f"Could not write output: {exc}", file=sys.stderr)
        return 1

    if args.verbose:
        for url in result.urls:
            print(url)
    print(f"Wrote {len(result.messages)} messages to {messages_path}")
    print(f"Wrote {len(result.urls)} URLs to {urls_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
