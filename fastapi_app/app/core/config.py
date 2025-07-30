from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_KEY: str
    DOLPHIN_API_TOKEN: str
    DOLPHIN_API_URL: str
    DOLPHIN_API_LOCAL: str
    GEMINI_API_KEY: str
    PROXY_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()