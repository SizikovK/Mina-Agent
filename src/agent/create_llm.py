import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

load_dotenv()

def create_llm():
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()
    model = os.getenv("LLM_MODEL", "llama3.1")
    temperature = float(os.getenv("LLM_TEMPERATURE", "0"))
    api_key = os.getenv("LLM_API_KEY", "")
    base_url = os.getenv("BASE_URL", "http://localhost:11434")

    if provider == "openai":
        return ChatOpenAI(
            api_key=api_key,
            base_url=base_url,
            model=model,
            temperature=temperature,
            default_headers={
                "HTTP-Referer": "https://localhost", 
                "X-Title": "LangChain App"
            }
        )

    if provider == "ollama":
        return ChatOllama(
            model=model,
            temperature=temperature,
            base_url=base_url
        )

    raise ValueError(f"Неизвестный провайдер: {provider}")