from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://opsflow:opsflow_dev@localhost:5432/opsflow"
    REDIS_URL: str = "redis://localhost:6379/0"
    OPENAI_API_KEY: str = ""
    UPLOAD_DIR: str = "./uploads"
    LLM_MODEL: str = "gpt-4o"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
