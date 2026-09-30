# Telegram URL Scraper

Extract URLs from a [Telegram Desktop](https://desktop.telegram.org/) JSON chat export and save them as CSV. The same extractor backs a small Flask web app and a command-line tool.

**Try it online:** [telegram-url-extracter-wuv6jff7zq-de.a.run.app](https://telegram-url-extracter-wuv6jff7zq-de.a.run.app/)

License: [MPL-2.0](LICENSE).

## What it does

Telegram Desktop stores each message `text` field as a plain string or as a list of strings and entity objects. Link labels and real targets are not always the same string: a `text_link` entity keeps the URL in `href`.

This project:

- reads a Telegram Desktop export (`messages` array)
- flattens nested `text` values, including `text_link` `href`s
- strips trailing junk characters (`}{",'`) that stick to URLs
- de-duplicates URLs without changing first-seen order
- writes `result.csv` (one row per message) and `urls.csv` (one URL per row)

`result.csv` columns: `id`, `type`, `date`, `from`, `text`.

`urls.csv` column: `urls`.

## Requirements

- Python 3.9 or newer
- A Telegram Desktop JSON export (see below)

## Install

```bash
git clone https://github.com/Yash-Kavaiya/telegram-url-scraper.git
cd telegram-url-scraper
pip install -r requirements.txt
```

Development install (adds pytest):

```bash
pip install -r requirements-dev.txt
```

Production installs, including Cloud Run, should use `requirements.txt` only.

## Web app

```bash
python app.py
```

Open http://127.0.0.1:5000 , upload a `.json` export, then download either CSV from the results page.

`PORT` overrides the default port (`python app.py` with `PORT=8080` listens on 8080). Debug mode is off.

The WSGI object is `app:app`. For a production process, run one gunicorn worker so the browser session can find the CSVs written for that upload:

```bash
gunicorn --bind 0.0.0.0:8080 --workers 1 app:app
```

Uploads are parsed in memory. CSV files are stored under the system temp directory for the current browser session, not in the repository.

Invalid JSON and exports without a `messages` array are rejected with an error on the upload page.

## Command line

```bash
python main.py -i examples/sample_messages.json
```

That writes `result.csv` and `urls.csv` in the current directory. Both filenames are gitignored.

```bash
python main.py -i examples/sample_messages.json -o output
python main.py -i export.json --messages result.csv --urls urls.csv
python main.py -i export.json --verbose
python main.py --help
```

| Flag | Meaning |
| --- | --- |
| `-i`, `--input` | Telegram Desktop JSON export (required) |
| `-o`, `--output-dir` | Directory for `result.csv` and `urls.csv` (default: `.`) |
| `--messages` | Explicit messages CSV path |
| `--urls` | Explicit URLs CSV path |
| `--verbose` | Print each URL. Without this, the command prints two summary lines. |

The process exits with a non-zero status when the file is missing, the JSON is invalid, or `messages` is absent.

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

## Project layout

```
app.py                         Flask app (WSGI: app:app)
main.py                        CLI
telegram_url_scraper/          Shared extractor and CSV writer
examples/sample_messages.json  Small synthetic export
templates/                     Upload and download pages
tests/                         pytest
requirements.txt               Runtime dependencies
requirements-dev.txt           Runtime dependencies plus pytest
Dockerfile                     gunicorn on $PORT (default 8080)
```

Generated `result.json`, `result.csv`, and `urls.csv` files are not part of the source tree.

## Export a chat from Telegram Desktop

1. Install [Telegram Desktop](https://desktop.telegram.org/) and sign in.
2. Open the chat or group you want to export.
3. Open the chat profile (click the name or photo at the top).
4. Open the three-dot menu and choose **Export chat history**.
5. Choose **JSON** format and save the file.
6. Upload that file in the web app, or pass it to `python main.py -i`.

The tool only reads the export you give it. It does not log in to Telegram.

## Docker

```bash
docker build -t telegram-url-scraper .
docker run --rm -p 8080:8080 telegram-url-scraper
```

The container listens on `PORT` (default `8080`) and serves `app:app` with gunicorn.

## Google Cloud Run

`gcloud run deploy --source .` builds the Dockerfile in this repository. The public site already deployed from this project is:

https://telegram-url-extracter-wuv6jff7zq-de.a.run.app/

```bash
gcloud run deploy telegram-url-scraper \
    --source . \
    --platform managed \
    --region us-central1
```

Set `SECRET_KEY` in the service environment if you want session cookies signed with your own key. The web process must keep a single worker (the Dockerfile already does). Extracted CSVs stay on that instance's local disk for the browser session.

## License

[Mozilla Public License 2.0](LICENSE).
