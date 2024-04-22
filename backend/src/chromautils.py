# Declare the endpoint that will grab a provided question and answer it with Chroma proximity
def searchWithChromaProximity(documents_collection, question_text):
    proximity_search_response = documents_collection.query(
        query_texts=[question_text],
        n_results=1
    )

    print(proximity_search_response)
    return {
        "id": proximity_search_response.get("ids")[0][0],
        "content": proximity_search_response.get("documents")[0][0],
        "metadata": proximity_search_response.get("metadatas")[0][0]
    }