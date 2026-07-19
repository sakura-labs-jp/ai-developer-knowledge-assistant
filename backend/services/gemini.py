from google import genai
import os
from dotenv import load_dotenv


load_dotenv()


MODEL_NAME = "gemini-2.5-flash"


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set"
    )


client = genai.Client(
    api_key=api_key
)


def ask_gemini(message: str) -> str:
    """
    Send prompt to Gemini and return response.
    """

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=message
        )

        return response.text

    except Exception as e:
        return f"Gemini API Error: {str(e)}"