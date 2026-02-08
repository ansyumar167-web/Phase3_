# Quickstart Guide: Backend API with Authentication

## Prerequisites

- Python 3.9+
- Poetry or pip for dependency management
- Neon Serverless PostgreSQL account
- Better Auth configured

## Setup Instructions

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd <project-directory>

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn sqlmodel python-multipart asyncpg
pip install better-fastapi  # Better Auth integration
```

### 2. Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+asyncpg://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname
AUTH_SECRET_KEY=your-super-secret-key-here
AUTH_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Database Configuration

Initialize the database models and create tables:

```python
# database/init.py
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from typing import AsyncGenerator

DATABASE_URL = "postgresql+asyncpg://..."

# Create async engine
engine = create_async_engine(DATABASE_URL)

async def create_tables():
    """Create all tables in the database"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Call this function during app startup
```

### 4. Better Auth Configuration

```python
# auth/auth_config.py
from better_fastapi.auth import Auth
from better_fastapi.utils.db import SQLAlchemyAsyncDB
from sqlmodel.ext.asyncio.session import AsyncSession

# Initialize Better Auth with Neon database
auth = Auth(
    db=SQLAlchemyAsyncDB("postgresql+asyncpg://..."),
    secret="your-secret-key",
    algorithm="HS256",
    access_token_expire_minutes=30
)
```

### 5. Run the Application

```bash
# Start the development server
uvicorn main:app --reload

# The API will be available at http://localhost:8000
```

## API Usage Examples

### Authenticating Requests

All protected endpoints require a Bearer token in the Authorization header:

```bash
curl -X POST "http://localhost:8000/api/ziakhan/chat" \
  -H "Authorization: Bearer YOUR_BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "What can you help me with?"}'
```

### Testing the Chat Endpoint

1. Obtain an authentication token through the login endpoint
2. Use the token to make requests to the chat endpoint
3. Verify that conversation history is properly reconstructed
4. Check that messages are persisted in the database

## Development Workflow

1. **Start database**: Ensure Neon PostgreSQL is accessible
2. **Run migrations**: Apply any pending database schema changes
3. **Start server**: Launch the FastAPI application with `uvicorn`
4. **Test endpoints**: Verify authentication and chat functionality
5. **Debug**: Check logs and database state as needed

## Troubleshooting

### Common Issues

- **Database Connection**: Verify Neon PostgreSQL credentials and connection string
- **Authentication**: Ensure tokens are properly formatted and not expired
- **User ID Mismatch**: Confirm that the authenticated user matches the user_id in the URL
- **CORS**: If developing with a frontend, configure CORS middleware appropriately