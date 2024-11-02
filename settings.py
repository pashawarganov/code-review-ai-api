import os

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Code Review AI API"

    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")

    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN")

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
