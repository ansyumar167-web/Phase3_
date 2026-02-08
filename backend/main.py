"""
Main entry point for the Todo AI Agent application.
This file provides a simple way to start just the web API server without the MCP server.
For full functionality including the MCP server, use application.py
"""

import os
import uvicorn
from src.api.chat_endpoint import create_app
from src.config import settings

app = create_app()


def main():
    """Run the web API only."""
    # Get port from environment variable or default to 8000
    port = int(os.environ.get("PORT", 8000))

    print(f"Starting {settings.app_name} v{settings.version} - Web API only")
    print(f"API available at: http://0.0.0.0:{port}")
    print("Note: MCP server is not running. For full functionality, use 'python application.py'")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=False,  # Set to False in production
    )


if __name__ == "__main__":
    main()