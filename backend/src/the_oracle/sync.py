import logging
import os
import time

from the_oracle.chroma import get_client
from the_oracle.sources import google_sheets, json_file

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

SOURCES = {
    "json": json_file.load_entries,
    "google_sheets": google_sheets.load_entries,
}


def sync_knowledge(client, entries: list[dict]) -> int:
    collection = client.get_or_create_collection(name="documents")

    collection.upsert(
        ids=[e["id"] for e in entries],
        documents=[e["questions"] for e in entries],
        metadatas=[
            {"question": e["questions"], "answer": e["answer"], "owner": e["owner"]}
            for e in entries
        ],
    )

    return len(entries)


def main():
    source_name = os.environ.get("SYNC_SOURCE", "json")
    interval = int(os.environ.get("SYNC_INTERVAL_SECONDS", "300"))

    load_entries = SOURCES[source_name]
    client = get_client()
    log.info("Connected to ChromaDB, source=%s", source_name)

    while True:
        entries = load_entries()
        count = sync_knowledge(client, entries)
        log.info("Synced %d entries", count)
        time.sleep(interval)


if __name__ == "__main__":
    main()
