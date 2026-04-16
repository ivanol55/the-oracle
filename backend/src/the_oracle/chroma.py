import json
import os
import socket
import time

import chromadb


def wait_for_port(host: str, port: int, timeout: int = 60) -> None:
    start_time = time.perf_counter()
    while True:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                break
        except OSError:
            time.sleep(1)
            if time.perf_counter() - start_time >= timeout:
                raise TimeoutError("ChromaDB connection failed from backend")


def search_by_proximity(documents_collection, question_text: str) -> dict:
    response = documents_collection.query(
        query_texts=[question_text],
        n_results=1,
    )
    return {
        "id": response["ids"][0][0],
        "content": response["documents"][0][0],
        "metadata": response["metadatas"][0][0],
    }


def initialize_collection(chroma_client, knowledge_data_file: str):
    collection = chroma_client.create_collection(name="documents")
    with open(knowledge_data_file) as f:
        knowledge_data = json.load(f)
    for entry in knowledge_data["entries"]:
        collection.add(
            documents=[entry["content"]],
            metadatas=[entry["metadata"]],
            ids=[entry["id"]],
        )
    return collection


def connect() -> tuple:
    host = os.environ["CHROMA_HOST"]
    port = int(os.environ["CHROMA_PORT"])
    wait_for_port(host, port)
    client = chromadb.HttpClient(host=host, port=port)

    if os.environ.get("POPULATE_CHROMA", "False") == "True":
        collection = initialize_collection(
            client, os.environ["KNOWLEDGE_DATA_FILE"]
        )
    else:
        collection = client.get_collection(name="documents")

    return client, collection
