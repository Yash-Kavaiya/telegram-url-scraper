"""Flask UI for extracting URLs from a Telegram Desktop JSON export."""

from __future__ import annotations

import os
import tempfile
import uuid

from flask import Flask, render_template, request, send_file, session

from telegram_url_scraper.csv_export import write_csvs
from telegram_url_scraper.extractor import ExportError, extract_from_export, parse_export_json

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "telegram-url-scraper")
app.config.setdefault(
    "WORKDIR",
    os.path.join(tempfile.gettempdir(), "telegram-url-scraper"),
)


def _workdir() -> str:
    path = app.config["WORKDIR"]
    os.makedirs(path, exist_ok=True)
    return path


def _csv_path(name: str) -> str | None:
    token = session.get("export_token")
    if not isinstance(token, str) or not token.isalnum():
        return None
    path = os.path.join(_workdir(), token, name)
    if not os.path.isfile(path):
        return None
    return path


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    upload_file = request.files.get("file")
    if upload_file is None or upload_file.filename == "":
        return render_template("index.html", error="Choose a JSON file to upload."), 400
    try:
        data = parse_export_json(upload_file.read())
        result = extract_from_export(data)
    except ExportError as exc:
        return render_template("index.html", error=str(exc)), 400

    token = uuid.uuid4().hex
    dest = os.path.join(_workdir(), token)
    os.makedirs(dest, exist_ok=True)
    write_csvs(result, os.path.join(dest, "result.csv"), os.path.join(dest, "urls.csv"))
    session["export_token"] = token
    return render_template(
        "download.html",
        urls=result.urls,
        message_count=len(result.messages),
        url_count=len(result.urls),
    )


def _missing_export():
    return (
        render_template(
            "index.html",
            error="No export is ready to download. Upload a JSON file first.",
        ),
        404,
    )


@app.route("/download_result")
def download_result():
    path = _csv_path("result.csv")
    if path is None:
        return _missing_export()
    return send_file(path, as_attachment=True, download_name="result.csv", mimetype="text/csv")


@app.route("/download_urls")
def download_urls():
    path = _csv_path("urls.csv")
    if path is None:
        return _missing_export()
    return send_file(path, as_attachment=True, download_name="urls.csv", mimetype="text/csv")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=False)
