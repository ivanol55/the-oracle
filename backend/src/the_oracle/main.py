from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from the_oracle.chroma import connect, search_by_proximity

chroma_client, documents_collection = connect()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
async def root():
    return {"message": "Hello! this is the Oracle API."}


@app.post("/ask")
async def ask(request_payload: QuestionRequest):
    question_text = request_payload.question
    response = search_by_proximity(documents_collection, question_text)
    return {"question": question_text, "response": response}
