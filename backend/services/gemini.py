from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY is not set")

def ask_gemini(message: str):

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=message
    )

    return response.text