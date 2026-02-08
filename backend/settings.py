import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Database
DATABASE_URL = os.getenv("DATABASE_URL")

# App & debug
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
APP_NAME = os.getenv("APP_NAME", "Todo AI Agent")
VERSION = os.getenv("VERSION", "0.1.0")

# JWT
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkeychangethisinproduction")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# API
API_PREFIX = os.getenv("API_PREFIX", "/api/v1")
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5175,http://localhost:5174,http://localhost:5173,http://localhost:3000,http://localhost:8000"
).split(",")

# OpenAI / OpenRouter
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")


class Settings:
    def __init__(self):
        self.database_url = DATABASE_URL
        self.debug = DEBUG
        self.app_name = APP_NAME
        self.version = VERSION
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        self.access_token_expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES
        self.api_prefix = API_PREFIX
        self.allowed_origins = ALLOWED_ORIGINS
        self.openai_api_key = OPENAI_API_KEY
        self.openai_model = OPENAI_MODEL
        self.openrouter_base_url = OPENROUTER_BASE_URL

    def __repr__(self):
        return f"<Settings app_name={self.app_name} env_debug={self.debug} db_url={self.database_url[:30]}...>"


settings = Settings()