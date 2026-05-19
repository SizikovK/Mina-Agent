from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def create_llm():
    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("BASE_URL")
    model = os.getenv("MODEL")
    temperature = float(os.getenv("TEMPERATURE", 0))

    if not api_key:
        raise ValueError("LLM_API_KEY is not set")
    if not model:
        raise ValueError("MODEL is not set")

    return ChatOpenAI(
        api_key=api_key,
        base_url=base_url,
        model=model,
        temperature=temperature,
        timeout=65
    )