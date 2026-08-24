import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not configured. Please add it to your .env file."
    )


def get_llm():
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model=MODEL_NAME,
        temperature=0,
    )