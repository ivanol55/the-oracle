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


def get_client() -> chromadb.HttpClient:
    host = os.environ["CHROMA_HOST"]
    port = int(os.environ["CHROMA_PORT"])
    wait_for_port(host, port)
    return chromadb.HttpClient(host=host, port=port)


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
