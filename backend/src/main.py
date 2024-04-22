# Make necessary application imports
import chromautils
import setuputils
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Initiate the Chroma collection depending if it's empty
chroma_client, documents_collection = setuputils.instantiate_chroma()

# Declare the FastAPI application for route management
app = FastAPI()

# Set up CORS access

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy root endpoint to test the API server is working
@app.get("/")
async def root():
    return {
        "message": "Hello! this is the Oracle API."
    }

# Declare the Question structure to track what data will be provided as POST for the API
class QuestionStruct(BaseModel):
    question: str

# Declare the endpoint that will grab a provided question and answer it with Chroma proximity
@app.options("/ask")
async def ask_options():
    return {
        "status_code": 200
    }


@app.post("/ask")
async def ask(request_payload: QuestionStruct):

    question_text = request_payload.question
    proximity_search_response = chromautils.searchWithChromaProximity(documents_collection, question_text)
    return {
        "question": question_text,
        "response": proximity_search_response
    }
