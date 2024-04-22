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

def instantiate_chroma():
    # Declare chroma client, which we'll need later when making requests
    wait_for_port(os.environ["CHROMA_HOST"], os.environ["CHROMA_PORT"], 60)
    chroma_client = chromadb.HttpClient(host=os.environ["CHROMA_HOST"], port=os.environ["CHROMA_PORT"])
    populate_chroma = os.environ["POPULATE_CHROMA"]
    if populate_chroma == "True":
        documents_collection = chroma_client.create_collection(name="documents")
        knowledge_data_file = os.environ["KNOWLEDGE_DATA_FILE"]
        knowledge_file_contents = open(knowledge_data_file, "r")
        knowledge_data = json.load(knowledge_file_contents)
        for entry in knowledge_data["entries"]:
            documents_collection.add(
                documents=[entry.get("content")],
                metadatas=[entry.get("metadata")],
                ids=[entry.get("id")]
            )
    else:
        documents_collection = chroma_client.get_collection(name="documents")
    return chroma_client, documents_collection
