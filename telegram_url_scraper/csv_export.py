"""Write extraction results to CSV files."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from telegram_url_scraper.extractor import ExtractionResult

MESSAGE_COLUMNS = ["id", "type", "date", "from", "text"]


def write_csvs(result: ExtractionResult, messages_path: str | Path, urls_path: str | Path) -> None:
    """Write ``result.csv``-style message rows and a one-column URL list."""
    messages = pd.DataFrame(result.messages, columns=MESSAGE_COLUMNS)
    messages.to_csv(messages_path, index=False)
    urls = pd.DataFrame({"urls": result.urls})
    urls.to_csv(urls_path, index=False)
