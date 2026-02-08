from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from src.database.connection import create_db_and_tables
from src.api.routers.chat import router as chat_router
from src.api.auth_endpoint import include_auth_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for FastAPI application.
    Runs startup and shutdown events.
    """
    logger.info("Starting up the application...")
    # Create database tables on startup
    await create_db_and_tables()
    yield
    logger.info("Shutting down the application...")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(
        title="AI Todo Chatbot API",
        description="An AI-powered chatbot for managing todos through natural language",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5178", "http://localhost:5175", "http://localhost:5174", "http://localhost:5173", "http://localhost:3000", "http://localhost:8000"],  # Specific development origins
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],  # Comprehensive HTTP methods
        allow_headers=["Content-Type", "Authorization", "Accept", "X-Requested-With"],  # Common headers
    )

    # Include API routers
    app.include_router(chat_router, prefix="/api", tags=["chat"])
    include_auth_router(app)

    @app.get("/")
    def read_root():
        return {"message": "AI Todo Chatbot API is running!"}

    @app.get("/health")
    def health_check():
        return {"status": "healthy", "service": "AI Todo Chatbot API"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
