import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv("NEON_DATABASE_URL") or os.getenv("DATABASE_URL") or "postgresql://username:password@localhost/todo_app"
if not DATABASE_URL.startswith("postgresql"):
    print(f"Warning: DATABASE_URL does not start with postgresql, got: {DATABASE_URL}")

# Neon PostgreSQL defaults (these can be overridden by environment variables)
NEON_DB_HOST = os.getenv("NEON_DB_HOST", "ep-aged-snowflake-123456.us-east-1.aws.neon.tech")
NEON_DB_NAME = os.getenv("NEON_DB_NAME", "todo_app")
NEON_DB_USER = os.getenv("NEON_DB_USER", "neondb_owner")
NEON_DB_PASSWORD = os.getenv("NEON_DB_PASSWORD", "")
NEON_DB_SSL_MODE = os.getenv("NEON_DB_SSL_MODE", "require")

# Neon-specific connection parameters
NEON_POOL_SIZE = int(os.getenv("NEON_POOL_SIZE", "5"))
NEON_MAX_OVERFLOW = int(os.getenv("NEON_MAX_OVERFLOW", "10"))
NEON_POOL_TIMEOUT = int(os.getenv("NEON_POOL_TIMEOUT", "30"))
NEON_POOL_RECYCLE = int(os.getenv("NEON_POOL_RECYCLE", "3600"))
NEON_STATEMENT_TIMEOUT = int(os.getenv("NEON_STATEMENT_TIMEOUT", "30000"))  # in milliseconds

# Construct the full database URL if not provided
if not os.getenv("DATABASE_URL") and not os.getenv("NEON_DATABASE_URL"):
    DATABASE_URL = f"postgresql://{NEON_DB_USER}:{NEON_DB_PASSWORD}@{NEON_DB_HOST}/{NEON_DB_NAME}?sslmode={NEON_DB_SSL_MODE}"

# Application Configuration
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-123456-change-this-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# MCP Server Configuration
MCP_SERVER_HOST = os.getenv("MCP_SERVER_HOST", "127.0.0.1")
MCP_SERVER_PORT = int(os.getenv("MCP_SERVER_PORT", "3000"))

# API Configuration
API_V1_STR = os.getenv("API_PREFIX", "/api/v1")  # Changed to use API_PREFIX from .env
APP_NAME = os.getenv("APP_NAME", "Todo AI Agent")
VERSION = os.getenv("VERSION", "0.1.0")

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-fake-key-for-local-testing")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://api.openai.com/v1")  # Default to OpenAI


class Settings:
    """
    Application settings class that consolidates all configuration values.
    """

    def __init__(self):
        # Database settings
        self.database_url: str = DATABASE_URL
        self.database_echo: bool = DEBUG

        # Neon PostgreSQL specific settings
        self.neon_pool_size: int = NEON_POOL_SIZE
        self.neon_max_overflow: int = NEON_MAX_OVERFLOW
        self.neon_pool_timeout: int = NEON_POOL_TIMEOUT
        self.neon_pool_recycle: int = NEON_POOL_RECYCLE
        self.neon_statement_timeout: int = NEON_STATEMENT_TIMEOUT

        # Application settings
        self.debug: bool = DEBUG
        self.log_level: str = LOG_LEVEL
        self.secret_key: str = SECRET_KEY
        self.algorithm: str = ALGORITHM
        self.access_token_expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES

        # MCP Server settings
        self.mcp_server_host: str = MCP_SERVER_HOST
        self.mcp_server_port: int = MCP_SERVER_PORT

        # API settings
        self.api_v1_str: str = API_V1_STR
        self.app_name: str = APP_NAME
        self.version: str = VERSION
        self.allowed_origins: list = os.getenv("ALLOWED_ORIGINS", "http://localhost:5174,http://localhost:5175,http://localhost:5173,http://localhost:3000,http://localhost:8000").split(",")  # Allow common dev origins

        # Environment
        self.environment: str = ENVIRONMENT

        # OpenAI settings
        self.openai_api_key: str = OPENAI_API_KEY
        self.openai_model: str = OPENAI_MODEL
        self.openrouter_base_url: str = OPENROUTER_BASE_URL

    def __str__(self):
        return f"Settings(environment={self.environment}, debug={self.debug}, db_url={self.database_url})"

    def __repr__(self):
        return self.__str__()


# Create a global settings instance
settings = Settings()


def validate_settings():
    """
    Validate that all required settings are properly configured.

    Raises:
        ValueError: If any required setting is missing or invalid
    """
    errors = []

    if not settings.secret_key or settings.secret_key == "super-secret-123456-change-this-in-production":
        errors.append("SECRET_KEY is not set or is using default value")

    if settings.database_url == "postgresql://username:password@localhost/todo_app":
        print("Warning: Using default DATABASE_URL, this should be changed for production")

    if settings.environment == "production" and settings.debug:
        errors.append("DEBUG should be False in production environment")

    if errors:
        raise ValueError(f"Invalid configuration: {'; '.join(errors)}")


# Validate settings on import
try:
    validate_settings()
except ValueError as e:
    print(f"Configuration error: {e}")
    if os.getenv("ENVIRONMENT") == "production":
        raise