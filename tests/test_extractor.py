"""Unit tests for Telegram export parsing and URL extraction."""

import json
from pathlib import Path

import pytest

from telegram_url_scraper.extractor import (
    ExportError,
    clean_url,
    dedupe_preserve_order,
    extract_from_export,
    extract_urls_from_text,
)

FIXTURE = Path(__file__).resolve().parents[1] / "examples" / "sample_messages.json"

EXPECTED_URLS = [
    "https://example.com/notes",
    "https://docs.example.com/guide",
    "https://example.com/plain",
]


def test_plain_string_urls():
    urls = extract_urls_from_text("See https://example.com/a and http://example.com/b")
    assert urls == ["https://example.com/a", "http://example.com/b"]


def test_nested_list_and_text_link_href():
    text = [
        "label ",
        {"type": "text_link", "text": "the docs", "href": "https://docs.example.com/guide"},
        {"type": "bold", "text": {"type": "text_link", "text": "inner", "href": "https://nested.example/a"}},
    ]
    assert extract_urls_from_text(text) == [
        "https://docs.example.com/guide",
        "https://nested.example/a",
    ]


def test_dict_text_uses_href():
    text = {"type": "text_link", "text": "click", "href": "https://dict.example/item}"}
    assert extract_urls_from_text(text) == ["https://dict.example/item"]


def test_clean_url_strips_trailing_junk_only():
    assert clean_url('https://example.com/a}",\'') == "https://example.com/a"
    assert clean_url("https://example.com/a}b") == "https://example.com/a}b"
    assert extract_urls_from_text('go to https://example.com/a}",\' now') == ["https://example.com/a"]


def test_dedupe_preserves_order():
    assert dedupe_preserve_order(["b", "a", "b", "", "c", "a"]) == ["b", "a", "c"]
    data = {
        "messages": [
            {"id": 1, "text": "https://example.com/b https://example.com/a"},
            {"id": 2, "text": "https://example.com/b"},
            {"id": 3, "text": [{"type": "link", "text": "https://example.com/c"}]},
        ]
    }
    assert extract_from_export(data).urls == [
        "https://example.com/b",
        "https://example.com/a",
        "https://example.com/c",
    ]


def test_missing_messages_key():
    with pytest.raises(ExportError, match="missing a 'messages' array"):
        extract_from_export({"name": "chat"})


def test_messages_must_be_an_array():
    with pytest.raises(ExportError, match="'messages' must be an array"):
        extract_from_export({"messages": {"text": "https://example.com"}})


def test_sample_fixture_urls_and_flattened_text():
    result = extract_from_export(json.loads(FIXTURE.read_text(encoding="utf-8")))
    assert result.urls == EXPECTED_URLS
    assert result.messages[1]["text"] == 'Read the guide or open https://example.com/plain},"'
    assert result.messages[3]["from"] == "Ada"
    assert result.messages[3]["text"] == ""
