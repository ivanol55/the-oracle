# The Oracle

A semantic Q&A tool. Feed it a knowledge base of question-answer pairs, then ask questions in natural language — the Oracle finds the closest match using vector embeddings and returns the answer with a confidence score.

## Architecture

The project runs as four Docker services:

| Service | Role |
|---|---|
| `embedding_database` | ChromaDB instance for vector storage (cosine similarity) |
| `data_sync` | Background worker that syncs `data.json` into ChromaDB every 5 minutes |
| `api_backend` | FastAPI server exposing `/ask` and `/bulk` endpoints |
| `app_frontend` | Astro frontend served on port 3000 |

Questions from `data.json` are split into individual embeddings (one per question variant) using ChromaDB's default `all-MiniLM-L6-v2` model. When a user asks something, the query is embedded and compared against all stored questions using cosine distance. The closest match is returned along with its answer and a confidence percentage.

## Getting started

1. Install [Docker](https://docs.docker.com/get-docker/) with the `compose` plugin
2. Clone this repository
3. Start the stack:
   ```bash
   docker compose up -d --build
   ```
4. Open `http://localhost:3000`
5. Start asking questions (the first request may be slow while the embedding model downloads)

To stop:
```bash
docker compose down
```

## Adding knowledge

Edit `data/knowledge/data.json`. Each entry follows this format:

```json
{
  "id": "1",
  "questions": "Question variant A | Question variant B | Question variant C",
  "answer": "The answer text.",
  "owner": "Product"
}
```

- **id** — unique identifier for the entry
- **questions** — pipe-separated (`|`) question variations that should all map to the same answer. More variants improve matching.
- **answer** — the response returned when a question matches
- **owner** — category tag (e.g. `Product`, `Implementation`, `Sales`)

The `data_sync` service picks up changes automatically every 5 minutes (configurable via `SYNC_INTERVAL_SECONDS`). To force an immediate re-sync, restart the sync service:

```bash
docker compose restart data_sync
```

**Important:** If you change the distance metric or embedding strategy, delete the existing ChromaDB data so it rebuilds from scratch:

```bash
rm -rf data/chroma/
docker compose restart data_sync
```

## API

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/ask` | Ask a single question. Body: `{"question": "..."}` |
| `POST` | `/bulk` | Upload a CSV of questions. Returns a CSV with answers. |
| `GET` | `/template` | Download the CSV template for bulk uploads |

## Configuration

Environment variables in `docker-compose.yaml`:

| Variable | Service | Default | Description |
|---|---|---|---|
| `CONFIDENCE_THRESHOLD` | `api_backend` | `30` | Minimum confidence % to return a result |
| `SYNC_SOURCE` | `data_sync` | `json` | Data source (`json` or `google_sheets`) |
| `SYNC_INTERVAL_SECONDS` | `data_sync` | `300` | Seconds between knowledge base syncs |
