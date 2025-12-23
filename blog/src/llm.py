from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from src.config import LLM_PROVIDER, LLM_MODEL, OPENAI_API_KEY, GROQ_API_KEY


def get_llm():
    """Returns LLM based on provider config"""
    if LLM_PROVIDER == "groq":
        return ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=GROQ_API_KEY,
            temperature=0
        )
    else:
        return ChatOpenAI(
            model=LLM_MODEL,
            api_key=OPENAI_API_KEY,
            temperature=0,
            model_kwargs={"response_format": {"type": "json_object"}}
        )