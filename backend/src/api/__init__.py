"""API package for the Todo AI Agent."""

from .chat_endpoint import create_app, router

# Create the app instance
app = create_app()

__all__ = ["app", "router"]