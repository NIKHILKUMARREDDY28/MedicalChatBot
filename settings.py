from pydantic_settings import BaseSettings
class Settings(BaseSettings):

    OPENAI_API_KEY : str

    class Config:
        env_file = None  # Disable default env_file setting
        extra = "allow"

settings = Settings(_env_file=".env")