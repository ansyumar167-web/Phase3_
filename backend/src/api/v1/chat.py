from fastapi import APIRouter, HTTPException, Depends, Request
from sqlmodel import Session
from typing import Optional, Dict, Any
from pydantic import BaseModel
from ...database.session import get_session
from ...auth.middleware import auth_middleware
from ...services.conversation_service import ConversationService
from ...services.message_service import MessageService
from ...models.conversation import ConversationCreate
from ...models.message import MessageCreate, MessageRole
import logging

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["chat"])


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    conversation_id: Optional[int] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    conversation_id: int
    response: str
    tool_calls: list[str]


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    req: Request,
    session: Session = Depends(get_session)
) -> ChatResponse:
    """
    Process a user message and return an AI response.

    Args:
        user_id: The ID of the user (extracted from URL)
        request: Contains the message and optional conversation_id
        req: Request object for extracting authentication
        session: Database session

    Returns:
        ChatResponse with conversation_id, AI response, and tool calls
    """
    # Extract and validate authentication
    authorization = req.headers.get("Authorization")
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="No authorization header provided"
        )

    # Extract token from Authorization header
    try:
        token_type, token = authorization.split(" ", 1)
        if token_type.lower() != "bearer":
            raise HTTPException(
                status_code=401,
                detail="Invalid token type"
            )
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header format"
        )

    # Verify token
    payload = await auth_middleware.verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    # Extract authenticated user ID from token
    authenticated_user_id = payload.get("user_id") or payload.get("sub")
    if not authenticated_user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token: no user ID found"
        )

    # Validate that the user_id in the URL matches the authenticated user
    if authenticated_user_id != user_id:
        logger.warning(f"User ID mismatch: URL={user_id}, Authenticated={authenticated_user_id}")
        raise HTTPException(
            status_code=403,
            detail="Access forbidden: user_id does not match authenticated user"
        )

    try:
        # Get or create conversation
        if request.conversation_id is None:
            # Create a new conversation
            conv_data = ConversationCreate(user_id=user_id)
            conversation = ConversationService.create_conversation(session, conv_data)
            conversation_id = conversation.id
        else:
            # Verify the conversation belongs to the user
            conversation = ConversationService.get_conversation_by_id(
                session, request.conversation_id, user_id
            )
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
            conversation_id = conversation.id

        # Add user message to conversation
        user_message = MessageCreate(
            user_id=user_id,
            conversation_id=conversation_id,
            role=MessageRole.USER,
            content=request.message
        )
        MessageService.add_message_to_conversation(session, user_message)

        # Get conversation history for context
        conversation_history = MessageService.get_latest_messages_for_conversation(
            session, conversation_id, user_id, limit=10
        )

        # Prepare history for the AI agent (mock for now)
        history_for_ai = []
        for msg in conversation_history:
            if msg.role == MessageRole.USER:
                history_for_ai.append({"role": "user", "content": msg.content})
            else:
                history_for_ai.append({"role": "assistant", "content": msg.content})

        # Mock AI response (to be replaced with actual AI agent later)
        # For now, return a simple response based on the message
        if "hello" in request.message.lower() or "hi" in request.message.lower():
            ai_response_content = f"Hello! I received your message: '{request.message}'. How can I help you?"
        elif "bye" in request.message.lower() or "goodbye" in request.message.lower():
            ai_response_content = f"Goodbye! Thanks for chatting: '{request.message}'. Have a great day!"
        else:
            ai_response_content = f"I understand you said: '{request.message}'. This is a mock AI response."

        # Add AI response to conversation
        ai_message = MessageCreate(
            user_id=user_id,
            conversation_id=conversation_id,
            role=MessageRole.ASSISTANT,
            content=ai_response_content
        )
        MessageService.add_message_to_conversation(session, ai_message)

        return ChatResponse(
            conversation_id=conversation_id,
            response=ai_response_content,
            tool_calls=[]  # Empty for now, will be populated when AI agent is implemented
        )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log the error for debugging
        logger.error(f"Error processing chat request: {str(e)}", exc_info=True)
        # Handle any other errors
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your request: {str(e)}"
        )