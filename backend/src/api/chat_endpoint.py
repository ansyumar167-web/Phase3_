from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import status
from typing import Optional, Dict, Any, List
from sqlmodel import Session, select
from ..database.session import get_session
from ..services.ai_agent import AIAgent
from ..services.conversation_service import ConversationService
from ..models.conversation import ConversationCreate
from ..models.message import Message as DBMessage, MessageCreate as MessageCreateModel, MessageRole
from pydantic import BaseModel
from ..auth.middleware import auth_middleware
import time
from ..utils.logging_config import get_logger, log_api_request, log_error
from ..utils.rate_limiter import check_rate_limit
from datetime import datetime, timedelta, timezone
from ..config import settings
from .auth_endpoint import include_auth_router
from jose import jwt, JWTError
from ..database.models import User as DBUser
import time


router = APIRouter(prefix=settings.api_v1_str, tags=["chat"])  # Use the API prefix from settings


async def get_current_user_from_token(
    token_credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    """
    Get the current authenticated user from the JWT token using the standard auth config.

    Args:
        token_credentials: The JWT token from the Authorization header

    Returns:
        The authenticated user object
    """
    from ..auth.config import SECRET_KEY, ALGORITHM
    from jose import JWTError

    try:
        payload = jwt.decode(
            token_credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")

        # Convert to int for DB lookup
        user_id_int = int(user_id)
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    # Get database session and lookup user
    from ..database.session import get_session_context
    from contextlib import contextmanager

    # Use the session in a context manager
    with get_session_context() as session:
        user = session.get(DBUser, user_id_int)
        if user is None:
            # Create user if not found in database (based on JWT payload)
            # Extract user info from payload
            user_email = payload.get("email", f"user_{user_id_int}@example.com")
            username = payload.get("username", f"user_{user_id_int}")

            # Create new user
            from ..database.models import UserRole
            new_user = DBUser(
                email=user_email,
                username=username,
                hashed_password="",  # Empty for auto-generated users
                role=UserRole.USER,
                is_active=True
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)

            # Ensure all necessary attributes are loaded before returning
            # by accessing them within the session context
            _ = new_user.id  # Force loading of id
            _ = new_user.email  # Force loading of email
            _ = new_user.username  # Force loading of username

            return new_user

        # Ensure all necessary attributes are loaded before returning
        # by accessing them within the session context
        _ = user.id  # Force loading of id
        _ = user.email  # Force loading of email
        _ = user.username  # Force loading of username

        return user


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    conversation_id: Optional[int] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    conversation_id: int
    response: str
    tool_calls: list[str]




@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: Request,
    request_body: ChatRequest,
    current_user = Depends(get_current_user_from_token),
    session: Session = Depends(get_session)
) -> ChatResponse:
    """
    Process a user message and return an AI response.
    This endpoint requires authentication based on the JWT token.

    Args:
        request: The incoming request (for header access)
        request_body: Contains the message and optional conversation_id
        current_user: The authenticated user from the token
        session: Database session

    Returns:
        ChatResponse with conversation_id, AI response, and tool calls
    """
    start_time = time.time()
    logger = get_logger("api.chat_endpoint")

    # Use the user ID from the authenticated user
    user_id = str(current_user.id)

    # Check rate limiting
    if not check_rate_limit(user_id, "chat"):
        logger.warning(f"Rate limit exceeded for user: {user_id}")
        duration = time.time() - start_time
        log_api_request(f"{settings.api_v1_str}/chat", "POST", user_id=user_id, status_code=status.HTTP_429_TOO_MANY_REQUESTS, duration=duration)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )

    # Log the incoming request
    log_api_request(f"{settings.api_v1_str}/chat", "POST", user_id=user_id)
    logger.info(f"Processing chat request for user_id: {user_id}, conversation_id: {request_body.conversation_id}")

    try:
        logger.info(f"User authentication successful: {user_id}")

        # Get or create conversation
        if request_body.conversation_id is None:
            # Create a new conversation
            logger.info(f"Creating new conversation for user: {user_id}")
            from ..models.conversation import Conversation as ConversationModel
            new_conversation = ConversationModel(user_id=user_id)
            session.add(new_conversation)
            session.commit()
            session.refresh(new_conversation)
            conversation_id = new_conversation.id
            logger.info(f"New conversation created with ID: {conversation_id}")
        else:
            # Verify the conversation belongs to the user
            logger.info(f"Fetching existing conversation: {request_body.conversation_id} for user: {user_id}")
            from ..models.conversation import Conversation as ConversationModel
            statement = select(ConversationModel).where(
                ConversationModel.id == request_body.conversation_id,
                ConversationModel.user_id == user_id
            )
            conversation = session.exec(statement).first()
            if not conversation:
                logger.warning(f"Conversation {request_body.conversation_id} not found for user: {user_id}")
                raise HTTPException(status_code=404, detail="Conversation not found")
            conversation_id = conversation.id
            logger.info(f"Found existing conversation with ID: {conversation_id}")

        # Add user message to conversation
        logger.info(f"Adding user message to conversation {conversation_id}")
        user_message_data = MessageCreateModel(
            user_id=user_id,
            conversation_id=conversation_id,
            role=MessageRole.USER,
            content=request_body.message
        )
        # Use direct database operations instead of service methods that may not exist
        from ..models.message import Message as MessageModel
        db_message = MessageModel(
            user_id=user_id,
            conversation_id=conversation_id,
            role=MessageRole.USER,
            content=request_body.message
        )
        session.add(db_message)
        session.commit()
        session.refresh(db_message)

        # Get conversation history for context using direct database query
        logger.info(f"Retrieving conversation history for conversation {conversation_id}")
        from ..models.message import Message as MessageModel
        statement = select(MessageModel).where(
            MessageModel.conversation_id == conversation_id
        ).order_by(MessageModel.id.desc()).limit(10)
        conversation_history = session.exec(statement).all()

        # Prepare history for the AI agent (reverse to get chronological order)
        history_for_ai = []
        for msg in reversed(conversation_history):
            role = "user" if msg.role == MessageRole.USER else "assistant"
            history_for_ai.append({"role": role, "content": msg.content})

        # Process message with AI agent
        logger.info(f"Sending message to AI agent for user: {user_id}")
        ai_agent = AIAgent()
        ai_response = await ai_agent.process_message(
            user_id, request_body.message, history_for_ai
        )
        logger.info(f"AI agent responded successfully for user: {user_id}")

        # Add AI response to conversation
        logger.info(f"Adding AI response to conversation {conversation_id}")
        ai_message_data = MessageCreateModel(
            user_id=user_id,  # Technically this is the AI, but we'll attribute to user for simplicity
            conversation_id=conversation_id,
            role=MessageRole.ASSISTANT,
            content=ai_response.content
        )
        # Add AI response to database
        ai_db_message = MessageModel(
            user_id=user_id,
            conversation_id=conversation_id,
            role=MessageRole.ASSISTANT,
            content=ai_response.content
        )
        session.add(ai_db_message)
        session.commit()
        session.refresh(ai_db_message)

        duration = time.time() - start_time
        logger.info(f"Chat request completed successfully for user: {user_id}, duration: {duration:.3f}s")

        # Log successful API request
        log_api_request(f"{settings.api_v1_str}/chat", "POST", user_id=user_id, status_code=200, duration=duration)

        return ChatResponse(
            conversation_id=conversation_id,
            response=ai_response.content,
            tool_calls=getattr(ai_response, 'tool_calls', [])
        )
    except HTTPException as e:
        duration = time.time() - start_time
        logger.error(f"HTTP exception for user {user_id}: {e.detail}, status: {e.status_code}")
        log_api_request(f"{settings.api_v1_str}/chat", "POST", user_id=user_id, status_code=e.status_code, duration=duration)
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Unexpected error for user {user_id}: {str(e)}")
        log_error(e, f"chat endpoint for user {user_id}")
        log_api_request(f"{settings.api_v1_str}/chat", "POST", user_id=user_id, status_code=500, duration=duration)
        # Handle any other errors
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your request: {str(e)}"
        )



@router.get("/conversations", response_model=List[Dict[str, Any]])
async def get_user_conversations(
    request: Request,
    current_user = Depends(get_current_user_from_token),
    session: Session = Depends(get_session)
) -> List[Dict[str, Any]]:
    """
    Get all conversations for a specific user.

    Args:
        request: The incoming request (for header access)
        current_user: The authenticated user from the token
        session: Database session

    Returns:
        List of conversation objects with their metadata
    """
    logger = get_logger("api.chat_endpoint")

    # Use the user ID from the authenticated user
    authenticated_user_id = str(current_user.id)
    logger.info(f"Getting conversations for user: {authenticated_user_id}")

    try:
        conversations = ConversationService.get_conversations_by_user(session, authenticated_user_id)
        conversations_data = []

        for conv in conversations:
            # Get message count for each conversation
            query = select(DBMessage).where(DBMessage.conversation_id == conv.id)
            messages = session.exec(query).all()
            message_count = len(messages)

            conversations_data.append({
                "id": conv.id,
                "user_id": conv.user_id,
                "created_at": conv.created_at,
                "updated_at": conv.updated_at,
                "message_count": message_count
            })

        logger.info(f"Retrieved {len(conversations_data)} conversations for user: {authenticated_user_id}")
        return conversations_data

    except Exception as e:
        logger.error(f"Error retrieving conversations for user {authenticated_user_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving conversations: {str(e)}"
        )


@router.get("/conversations/{conversation_id}/messages", response_model=List[Dict[str, Any]])
async def get_conversation_messages(
    request: Request,
    conversation_id: int,
    current_user = Depends(get_current_user_from_token),
    session: Session = Depends(get_session)
) -> List[Dict[str, Any]]:
    """
    Get all messages for a specific conversation.

    Args:
        request: The incoming request (for header access)
        conversation_id: The ID of the conversation
        current_user: The authenticated user from the token
        session: Database session

    Returns:
        List of message objects in the conversation
    """
    logger = get_logger("api.chat_endpoint")

    # Use the user ID from the authenticated user
    authenticated_user_id = str(current_user.id)
    logger.info(f"Getting messages for conversation {conversation_id} for user: {authenticated_user_id}")

    try:
        messages = ConversationService.get_messages_for_conversation(session, conversation_id, authenticated_user_id)

        messages_data = []
        for msg in messages:
            messages_data.append({
                "id": msg.id,
                "conversation_id": msg.conversation_id,
                "user_id": msg.user_id,
                "role": msg.role.value if hasattr(msg.role, 'value') else msg.role,
                "content": msg.content,
                "created_at": msg.created_at
            })

        logger.info(f"Retrieved {len(messages_data)} messages for conversation {conversation_id}")
        return messages_data

    except Exception as e:
        logger.error(f"Error retrieving messages for conversation {conversation_id}, user {authenticated_user_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving messages: {str(e)}"
        )


@router.get("/health")
def health_check() -> Dict[str, Any]:
    """
    Health check endpoint to verify API is running and database connectivity.

    Returns:
        Dict with status information
    """
    return {
        "status": "healthy",
        "service": "Todo AI Chat API",
        "timestamp": time.time()
    }


def create_app():
    """Create and configure the FastAPI application."""
    from fastapi import FastAPI  # Import here to avoid circular dependencies
    from fastapi.middleware.cors import CORSMiddleware
    from ..config import settings
    from .task_endpoint import router as task_router

    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        debug=settings.debug,
        docs_url="/docs",  # Enable API documentation
        redoc_url="/redoc"  # Enable alternative API documentation
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,  # Use settings for allowed origins
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE", "PATCH"],  # Added PATCH
        allow_headers=["Content-Type", "Authorization", "Accept", "X-Requested-With"],  # Proper headers
    )

    # Include the chat router
    app.include_router(router)

    # Include the auth router
    include_auth_router(app)

    # Include the task router
    app.include_router(task_router)

    return app