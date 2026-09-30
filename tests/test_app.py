"""Flask upload and download tests."""

import csv
import io
from pathlib import Path

import pytest

import app as webapp

FIXTURE = Path(__file__).resolve().parents[1] / "examples" / "sample_messages.json"
EXPECTED_URLS = [
    "https://example.com/notes",
    "https://docs.example.com/guide",
    "https://example.com/plain",
]


@pytest.fixture
def client(tmp_path):
    webapp.app.config.update(TESTING=True, SECRET_KEY="test-secret", WORKDIR=str(tmp_path))
    with webapp.app.test_client() as test_client:
        yield test_client


def _upload(client, payload: bytes, filename: str = "export.json"):
    return client.post(
        "/upload",
        data={"file": (io.BytesIO(payload), filename)},
        content_type="multipart/form-data",
    )


def test_upload_fixture_download_urls_and_messages(client):
    response = _upload(client, FIXTURE.read_bytes(), "sample_messages.json")
    assert response.status_code == 200
    page = response.get_data(as_text=True)
    assert "Download URLs CSV" in page
    assert "Download messages CSV" in page
    for url in EXPECTED_URLS:
        assert url in page

    urls_response = client.get("/download_urls")
    assert urls_response.status_code == 200
    urls_text = urls_response.get_data(as_text=True)
    rows = list(csv.DictReader(io.StringIO(urls_text)))
    assert [row["urls"] for row in rows] == EXPECTED_URLS

    messages_response = client.get("/download_result")
    assert messages_response.status_code == 200
    messages = list(csv.DictReader(io.StringIO(messages_response.get_data(as_text=True))))
    assert len(messages) == 4
    assert "https://example.com/notes" in messages[0]["text"]


def test_upload_rejects_invalid_json(client):
    response = _upload(client, b"not-json")
    assert response.status_code == 400
    assert "not valid JSON" in response.get_data(as_text=True)


def test_upload_rejects_missing_messages(client):
    response = _upload(client, b'{"name": "chat"}')
    assert response.status_code == 400
    assert "messages" in response.get_data(as_text=True)
    assert "missing" in response.get_data(as_text=True)


def test_upload_requires_a_file(client):
    response = client.post("/upload", data={}, content_type="multipart/form-data")
    assert response.status_code == 400
    assert "Choose a JSON file" in response.get_data(as_text=True)


def test_download_before_upload(client):
    response = client.get("/download_urls")
    assert response.status_code == 404
    assert "Upload a JSON file first" in response.get_data(as_text=True)
