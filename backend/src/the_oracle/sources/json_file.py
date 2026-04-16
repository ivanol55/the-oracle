import json

KNOWLEDGE_FILE = "/data/knowledge/data.json"


def load_entries() -> list[dict]:
    with open(KNOWLEDGE_FILE) as f:
        return json.load(f)
