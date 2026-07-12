from fastapi import FastAPI

from models.chat import ChatRequest
from services.gemini import ask_gemini

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "AI Developer Knowledge Assistant"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    answer = ask_gemini(request.message)

    return {
        "answer": answer
    }