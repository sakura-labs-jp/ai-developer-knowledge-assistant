from fastapi import FastAPI

from models.chat import ChatRequest, ChatResponse
from services.knowledge import ask_with_knowledge


app = FastAPI(
    title="AI Developer Knowledge Assistant",
    description="RAG based AI assistant for developer knowledge",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "AI Developer Knowledge Assistant"
    }


@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    answer = ask_with_knowledge(
        request.message
    )

    return ChatResponse(
        answer=answer
    )