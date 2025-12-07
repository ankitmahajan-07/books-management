from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:1234@localhost:5432/books")
    secret_key: str = os.getenv("SECRET_KEY", "changeme")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    ai_model_endpoint: str = os.getenv("AI_MODEL_ENDPOINT", "http://localhost:11434/generate")
    groq_api_key: str = os.getenv("GROQ_API_KEY", "your-groq-api-key")

    class Config:
        env_file = ".env"

settings = Settings()
