from fastapi import FastAPI

from backend.models.chat import ChatRequest, ChatResponse
from backend.services.rag import ask_with_knowledge


app = FastAPI(
    title="AI Developer Knowledge Assistant",
    description="RAG based AI assistant for developer knowledge",
    version="1.0.0"
)


@app.get("/")
def root():
    """
    Health check endpoint.
    """
    return {
        "message": "AI Developer Knowledge Assistant"
    }


@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):
    """
    Receive a user question and return an AI-generated answer.
    """

    answer = ask_with_knowledge(
        request.message
    )

    return ChatResponse(
        answer=answer
    )