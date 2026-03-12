from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_NAME: str = "Financial Document Intelligence API"

    class Config:
        env_file = ".env"

settings = Settings()       