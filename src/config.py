from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_NAME: str = "Financial Document Intelligence API"
    sec_user_agent: str = "DefaultUser/1.0 default@email.com"
    news_api_key: str = "your_key_here"
    

    class Config:
        env_file = ".env"

settings = Settings()       