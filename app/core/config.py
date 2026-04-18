from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    APP_NAME: str = "FastAPI Boilerplate"
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"

settings = Settings()