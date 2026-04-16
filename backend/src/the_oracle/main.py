from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from the_oracle.chroma import get_client, search_by_proximity

chroma_client = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global chroma_client
    chroma_client = get_client()
    yield


app = FastAPI(lifespan=lifespan)

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
    try:
        collection = chroma_client.get_collection("documents")
    except Exception:
        return JSONResponse(
            status_code=503,
            content={"error": "Knowledge base not synced yet"},
        )

    question_text = request_payload.question
    response = search_by_proximity(collection, question_text)
    return {"question": question_text, "response": response}
