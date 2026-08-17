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


GENERATIVE_MODEL = "gemini-3.6-flash"


def ask_gemini(message: str) -> str:
    """
    Send a prompt to Gemini and return the generated response.
    """

    response = client.models.generate_content(
        model=GENERATIVE_MODEL,
        contents=message
    )

    return response.text