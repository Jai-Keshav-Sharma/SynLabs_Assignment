import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()


class Config:
    """Configuration for the application."""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Model configurations
    OPENAI_MODEL = "gpt-4o-mini"
    GROQ_MODEL = "llama-3.3-70b-versatile"
    
    # LLM Provider (change here to switch)
    PRIMARY_PROVIDER = "openai"  # or "groq"
    
    # Output settings
    OUTPUT_DIR = "Outputs"
    
    @classmethod
    def get_llm(cls, temperature: float = 0.7):
        """Get the configured LLM instance."""
        if cls.PRIMARY_PROVIDER == "openai":
            return ChatOpenAI(
                model=cls.OPENAI_MODEL,
                temperature=temperature,
                api_key=cls.OPENAI_API_KEY
            )
        elif cls.PRIMARY_PROVIDER == "groq":
            return ChatGroq(
                model=cls.GROQ_MODEL,
                temperature=temperature,
                api_key=cls.GROQ_API_KEY
            )
        else:
            raise ValueError(f"Unknown provider: {cls.PRIMARY_PROVIDER}")