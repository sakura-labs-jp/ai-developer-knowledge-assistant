from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.models.chat import ChatRequest, ChatResponse
from backend.services.rag import ask_with_knowledge


app = FastAPI(
    title="AI Developer Knowledge Assistant",
    description="RAG-based AI assistant for developer knowledge",
    version="1.0.0"
)


# CORS configuration for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
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

    try:
        result = ask_with_knowledge(
            request.message
        )

        return ChatResponse(
            answer=result["answer"],
            source=result["source"]
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate an answer."
        ) from e