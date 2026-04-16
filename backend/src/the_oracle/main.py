import csv
import io
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

from the_oracle.chroma import get_client, search_by_proximity

chroma_client = None
confidence_threshold = 40


@asynccontextmanager
async def lifespan(app: FastAPI):
    global chroma_client, confidence_threshold
    chroma_client = get_client()
    confidence_threshold = int(os.environ.get("CONFIDENCE_THRESHOLD", "40"))
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
    response = search_by_proximity(collection, question_text, confidence_threshold)

    if response is None:
        return {"question": question_text, "response": None}

    return {"question": question_text, "response": response}


TEMPLATE_HEADERS = ["question", "answer", "confidence", "owner"]


@app.get("/template")
async def template():
    buf = io.StringIO()
    csv.writer(buf).writerow(TEMPLATE_HEADERS)
    return StreamingResponse(
        iter([buf.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=oracle_template.csv"},
    )


@app.post("/bulk")
async def bulk(file: UploadFile):
    try:
        collection = chroma_client.get_collection("documents")
    except Exception:
        return JSONResponse(
            status_code=503,
            content={"error": "Knowledge base not synced yet"},
        )

    content = (await file.read()).decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))

    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=TEMPLATE_HEADERS)
    writer.writeheader()

    for row in reader:
        question = row.get("question", "").strip()
        if not question:
            continue

        result = search_by_proximity(collection, question, confidence_threshold)
        if result:
            writer.writerow({
                "question": question,
                "answer": result["metadata"]["answer"],
                "confidence": result["confidence"],
                "owner": result["metadata"]["owner"],
            })
        else:
            writer.writerow({
                "question": question,
                "answer": "",
                "confidence": 0,
                "owner": "",
            })

    return StreamingResponse(
        iter([buf.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=oracle_answers.csv"},
    )
