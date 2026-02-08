#!/usr/bin/env python3
"""
Application entry point that starts both the MCP server and the web API.
"""

import asyncio
import threading
import signal
import sys
import os
from typing import Callable
import uvicorn
from concurrent.futures import ThreadPoolExecutor
import time

# Fix Windows console encoding issues
if sys.platform == 'win32':
    # Set UTF-8 encoding for stdout/stderr
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8')
    # Set environment variable for subprocesses
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from src.services.mcp_server import mcp_server_instance
from src.api.chat_endpoint import create_app
from src.config import settings

# Create the app instance
app = create_app()


class ApplicationManager:
    """Manages the lifecycle of both the MCP server and web API."""

    def __init__(self):
        self.mcp_server_running = False
        self.web_server_running = False
        self.shutdown_event = threading.Event()

    def signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print(f"\nReceived signal {signum}. Shutting down gracefully...")
        self.shutdown()

    def shutdown(self):
        """Shut down all services."""
        print("Shutting down services...")
        self.shutdown_event.set()

    def start_mcp_server_sync(self):
        """Synchronous wrapper to start MCP server in separate thread."""
        print(f"Starting MCP server on {settings.mcp_server_host}:{settings.mcp_server_port}")
        try:
            self.mcp_server_running = True
            # Call the synchronous run method directly - it manages its own event loop
            mcp_server_instance.run_sync(settings.mcp_server_host, settings.mcp_server_port)
        except Exception as e:
            print(f"Error starting MCP server: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.mcp_server_running = False

    def start_web_server(self):
        """Start the web API server."""
        print(f"Starting web API server on 0.0.0.0:8001")
        try:
            self.web_server_running = True
            uvicorn.run(
                app,
                host="0.0.0.0",
                port=8001,
                reload=False,  # Set to True only for development
                workers=1
            )
        except Exception as e:
            print(f"Error starting web server: {e}")
        finally:
            self.web_server_running = False

    def run(self):
        """Run both servers concurrently."""
        print(f"Starting {settings.app_name} v{settings.version}")
        print(f"MCP Server will run on: {settings.mcp_server_host}:{settings.mcp_server_port}")
        print(f"Web API will run on: http://localhost:8001")
        print("Press Ctrl+C to stop")

        # SOLUTION 1: Run MCP in main thread, FastAPI in background thread
        # This fixes the signal handling issue since MCP needs to be in main thread
        with ThreadPoolExecutor(max_workers=1) as executor:
            # Start web server in background thread
            print("Starting web API server in background thread...")
            web_future = executor.submit(self.start_web_server)

            # Give the web server a moment to start
            time.sleep(2)

            # Start MCP server in MAIN THREAD (blocking)
            # This allows MCP to properly set up signal handlers
            print("Starting MCP server in main thread...")
            try:
                self.start_mcp_server_sync()
            except KeyboardInterrupt:
                print("\nKeyboard interrupt received")
            except Exception as e:
                print(f"MCP server error: {e}")
                import traceback
                traceback.print_exc()
            finally:
                self.shutdown()


def main():
    """Main entry point."""
    manager = ApplicationManager()
    manager.run()


if __name__ == "__main__":
    main()