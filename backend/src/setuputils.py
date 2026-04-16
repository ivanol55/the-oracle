import os
import chromadb
import json
import time
import socket

def wait_for_port(host, port, timeout):

    start_time = time.perf_counter()
    while True:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                break
        except OSError:
            time.sleep(1)
            if time.perf_counter() - start_time >= timeout:
                raise TimeoutError('ChromaDB connection failed from backend')

def populate_collection(chroma_client, knowledge_data_file):
    chroma_client.delete_collection(name="documents")
    print("[setup] Recycling collection: deleted existing 'documents' collection")

    documents_collection = chroma_client.create_collection(name="documents")
    with open(knowledge_data_file, "r") as f:
        knowledge_data = json.load(f)
    for entry in knowledge_data["entries"]:
        documents_collection.add(
            documents=[entry.get("content")],
            metadatas=[entry.get("metadata")],
            ids=[entry.get("id")]
        )
    print(f"[setup] Populated collection with {len(knowledge_data['entries'])} entries")
    return documents_collection

def instantiate_chroma():
    wait_for_port(os.environ["CHROMA_HOST"], os.environ["CHROMA_PORT"], 60)
    chroma_client = chromadb.HttpClient(host=os.environ["CHROMA_HOST"], port=os.environ["CHROMA_PORT"])
    force_repopulate = os.environ.get("FORCE_REPOPULATE", "False") == "True"
    knowledge_data_file = os.environ["KNOWLEDGE_DATA_FILE"]

    if force_repopulate:
        print("[setup] FORCE_REPOPULATE is set, repopulating collection...")
        documents_collection = populate_collection(chroma_client, knowledge_data_file)
    else:
        try:
            documents_collection = chroma_client.get_collection(name="documents")
            print(f"[setup] Found existing collection 'documents' with {documents_collection.count()} entries, using it as-is")
        except Exception:
            print("[setup] No existing collection found, creating and populating...")
            documents_collection = populate_collection(chroma_client, knowledge_data_file)

    return chroma_client, documents_collection
