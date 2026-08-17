from google import genai
import os
from dotenv import load_dotenv


load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set"
    )


client = genai.Client(
    api_key=api_key
)


EMBEDDING_MODEL = "gemini-embedding-2"


def create_embedding(text: str):
    """
    Generate an embedding vector from the given text.
    """

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text
    )

    return response.embeddings[0].values