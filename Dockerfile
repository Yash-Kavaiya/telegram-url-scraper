FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080
EXPOSE 8080

# One worker: extracted CSVs live on local disk for the browser session.
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT} --workers 1 app:app"]
