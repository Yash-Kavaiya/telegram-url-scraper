"""Pure helpers for Telegram Desktop chat exports.

Telegram stores ``message["text"]`` as a string, a list of strings and entity
objects, or (less often) a single entity object. ``text_link`` entities keep
the real URL in ``href`` while the visible label lives in ``text``.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

# Trailing characters Telegram/JSON often glues onto an otherwise valid URL.
_TRAILING_JUNK = "}{\"',"
_URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)


class ExportError(ValueError):
    """The input is not a usable Telegram Desktop JSON export."""


@dataclass(frozen=True)
class ExtractionResult:
    """Rows for the messages CSV and a de-duplicated URL list."""

    messages: list[dict[str, object]]
    urls: list[str]


def parse_export_json(raw: str | bytes) -> dict:
    """Parse export JSON and require a top-level object."""
    if isinstance(raw, bytes):
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise ExportError("Input must be UTF-8 JSON.") from exc
    else:
        text = raw
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ExportError("Input is not valid JSON.") from exc
    if not isinstance(data, dict):
        raise ExportError("Telegram export must be a JSON object.")
    return data


def load_export(path: str | Path) -> dict:
    """Read a Telegram Desktop export from disk."""
    try:
        raw = Path(path).read_bytes()
    except OSError as exc:
        raise ExportError(f"Could not read input: {exc}") from exc
    return parse_export_json(raw)


def clean_url(url: str) -> str:
    """Strip whitespace and trailing junk characters from a URL."""
    cleaned = url.strip().rstrip(_TRAILING_JUNK).strip()
    if cleaned.lower().startswith(("http://", "https://")):
        return cleaned
    return ""


def dedupe_preserve_order(items: list[str]) -> list[str]:
    """Drop empty and repeated values without reordering first occurrences."""
    seen: set[str] = set()
    unique: list[str] = []
    for item in items:
        if not item or item in seen:
            continue
        seen.add(item)
        unique.append(item)
    return unique


def _collect_urls(node: object, found: list[str]) -> None:
    if isinstance(node, str):
        for match in _URL_RE.findall(node):
            cleaned = clean_url(match)
            if cleaned:
                found.append(cleaned)
        return
    if isinstance(node, Mapping):
        # href is the target of a text_link; other string fields can hold URLs too.
        for value in node.values():
            _collect_urls(value, found)
        return
    if isinstance(node, list):
        for item in node:
            _collect_urls(item, found)


def extract_urls_from_text(text: object) -> list[str]:
    """Return de-duplicated URLs from a Telegram ``text`` value."""
    found: list[str] = []
    _collect_urls(text, found)
    return dedupe_preserve_order(found)


def flatten_text(text: object) -> str:
    """Join the visible text of a string, list, or entity object."""
    parts: list[str] = []

    def walk(node: object) -> None:
        if isinstance(node, str):
            parts.append(node)
            return
        if isinstance(node, Mapping):
            if "text" in node:
                walk(node.get("text"))
            return
        if isinstance(node, list):
            for item in node:
                walk(item)

    walk(text)
    return "".join(parts)


def extract_from_export(data: object) -> ExtractionResult:
    """Build message rows and a URL list from a parsed Telegram export."""
    if not isinstance(data, dict):
        raise ExportError("Telegram export must be a JSON object.")
    if "messages" not in data:
        raise ExportError("JSON export is missing a 'messages' array.")
    messages = data["messages"]
    if not isinstance(messages, list):
        raise ExportError("'messages' must be an array.")

    rows: list[dict[str, object]] = []
    urls: list[str] = []
    for message in messages:
        if not isinstance(message, Mapping):
            continue
        text = message.get("text", "")
        sender = message.get("from") or message.get("actor") or ""
        rows.append(
            {
                "id": message.get("id", ""),
                "type": message.get("type", ""),
                "date": message.get("date", ""),
                "from": sender,
                "text": flatten_text(text),
            }
        )
        urls.extend(extract_urls_from_text(text))
    return ExtractionResult(messages=rows, urls=dedupe_preserve_order(urls))
