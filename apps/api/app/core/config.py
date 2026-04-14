from pathlib import Path

from pydantic_settings import BaseSettings


ROOT_DIR = Path(__file__).resolve().parents[4]
ENV_FILE = ROOT_DIR / ".env"
UPLOADS_DIR = ROOT_DIR / "uploads"


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://opsflow:opsflow_dev@localhost:5432/opsflow"
    REDIS_URL: str = "redis://localhost:6379/0"
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    UPLOAD_DIR: str = str(UPLOADS_DIR)
    LLM_MODEL: str = "gpt-4o"

    model_config = {
        "env_file": ENV_FILE,
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


settings = Settings()
