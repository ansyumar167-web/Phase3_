from better_auth import auth, BaseUser
from better_auth.oauth2 import google, github
from better_auth.api import create_app
from pydantic import Field
from typing import Optional
import os

# Define the authentication configuration
class CustomUser(BaseUser):
    email: str = Field(..., description="User's email address")
    username: Optional[str] = Field(None, description="User's username")


# Configure Better Auth
auth_instance = auth(
    secret=os.getenv("AUTH_SECRET", "your-secret-key-change-this"),
    database_url=os.getenv("DATABASE_URL", "sqlite:///./test.db"),
    user_model=CustomUser,
    providers=[
        google(
            client_id=os.getenv("GOOGLE_CLIENT_ID", ""),
            client_secret=os.getenv("GOOGLE_CLIENT_SECRET", ""),
        ),
        github(
            client_id=os.getenv("GITHUB_CLIENT_ID", ""),
            client_secret=os.getenv("GITHUB_CLIENT_SECRET", ""),
        ),
    ],
    debug=True,  # Set to False in production
)

# Create the FastAPI app with Better Auth
app = create_app(auth_instance)

# Optionally add custom routes or middleware here