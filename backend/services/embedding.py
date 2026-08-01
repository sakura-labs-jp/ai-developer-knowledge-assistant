from google import genai
import os
from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(
    BASE_DIR / ".env"
)


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


MODEL = "gemini-embedding-001"


def create_embedding(text: str):

    response = client.models.embed_content(
        model=MODEL,
        contents=text
    )

    return response.embeddings[0].values