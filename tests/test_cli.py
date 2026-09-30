"""CLI tests for main.py."""

import csv
from pathlib import Path

import pytest

from main import main

FIXTURE = Path(__file__).resolve().parents[1] / "examples" / "sample_messages.json"
EXPECTED_URLS = [
    "https://example.com/notes",
    "https://docs.example.com/guide",
    "https://example.com/plain",
]


def test_cli_writes_urls_csv(tmp_path, capsys):
    code = main(["-i", str(FIXTURE), "-o", str(tmp_path)])
    assert code == 0
    captured = capsys.readouterr()
    assert "https://example.com/notes" not in captured.out.splitlines()
    with (tmp_path / "urls.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert [row["urls"] for row in rows] == EXPECTED_URLS
    with (tmp_path / "result.csv").open(newline="", encoding="utf-8") as handle:
        messages = list(csv.DictReader(handle))
    assert len(messages) == 4
    assert "the guide" in messages[1]["text"]


def test_cli_verbose_prints_urls(tmp_path, capsys):
    assert main(["-i", str(FIXTURE), "-o", str(tmp_path), "--verbose"]) == 0
    captured = capsys.readouterr()
    assert captured.out.splitlines()[:3] == EXPECTED_URLS


def test_cli_custom_output_paths(tmp_path):
    urls_path = tmp_path / "nested" / "links.csv"
    messages_path = tmp_path / "messages.csv"
    code = main(
        [
            "-i",
            str(FIXTURE),
            "--urls",
            str(urls_path),
            "--messages",
            str(messages_path),
        ]
    )
    assert code == 0
    assert urls_path.is_file()
    assert messages_path.is_file()


def test_cli_missing_file(capsys):
    assert main(["-i", "does-not-exist.json"]) == 1
    assert "Could not read input" in capsys.readouterr().err


def test_cli_rejects_invalid_json_and_missing_messages(tmp_path, capsys):
    bad = tmp_path / "bad.json"
    bad.write_text("{", encoding="utf-8")
    assert main(["-i", str(bad), "-o", str(tmp_path)]) == 1
    assert "not valid JSON" in capsys.readouterr().err

    missing = tmp_path / "missing.json"
    missing.write_text('{"name": "chat"}', encoding="utf-8")
    assert main(["-i", str(missing), "-o", str(tmp_path)]) == 1
    assert "missing a 'messages' array" in capsys.readouterr().err


def test_cli_requires_input():
    with pytest.raises(SystemExit) as exc:
        main([])
    assert exc.value.code == 2
