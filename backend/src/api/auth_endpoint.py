from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional
from jose import jwt
from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select
from ..config import settings
from ..database.session import get_session
from ..database.models import User as DBUser
from ..auth.config import get_password_hash, verify_password

# Create the auth router with no prefix for root-level endpoints
root_router = APIRouter(tags=["auth"])

# Create the auth router with /api prefix for API-consistent endpoints
api_router = APIRouter(prefix="/api", tags=["auth"])

# User models
class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    email: str
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: Optional[str] = None

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

def get_user_by_email(session: Session, email: str) -> Optional[DBUser]:
    """Get user by email from the database."""
    statement = select(DBUser).where(DBUser.email == email)
    user = session.exec(statement).first()
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def register_user(user_data: UserRegister, session: Session) -> UserResponse:
    """Register a new user in the database."""
    # Check if user already exists
    existing_user = get_user_by_email(session, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password
    from ..auth.config import get_password_hash
    hashed_password = get_password_hash(user_data.password)

    # Create new user
    db_user = DBUser(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return UserResponse(
        id=db_user.id,
        email=db_user.email,
        username=db_user.username
    )

def login_handler(user_credentials: UserLogin, session: Session):
    """
    Common login handler that contains the actual login logic.
    """
    # Check if user exists in database
    user = get_user_by_email(session, user_credentials.email)
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create JWT token
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    token_data = {
        "sub": str(user.id),
        "user_id": str(user.id),
        "email": user.email,
        "username": user.username,
        "exp": expire.timestamp()
    }

    encoded_jwt = create_access_token(token_data)

    return LoginResponse(
        access_token=encoded_jwt,
        token_type="bearer",
        user=UserResponse(
            id=user.id,
            email=user.email,
            username=user.username
        )
    )


@root_router.post("/register", response_model=UserResponse)
async def root_register(user_data: UserRegister, session: Session = Depends(get_session)):
    """
    Register a new user account.
    """
    return register_user(user_data, session)


@api_router.post("/register", response_model=UserResponse)
async def api_register(user_data: UserRegister, session: Session = Depends(get_session)):
    """
    Register a new user account (API version).
    """
    return register_user(user_data, session)


@root_router.post("/login", response_model=LoginResponse)
async def root_login(user_credentials: UserLogin, session: Session = Depends(get_session)):
    """
    Login endpoint that authenticates user credentials and returns a JWT token (available at /login).
    """
    return login_handler(user_credentials, session)


@api_router.post("/login", response_model=LoginResponse)
async def api_login(user_credentials: UserLogin, session: Session = Depends(get_session)):
    """
    Login endpoint that authenticates user credentials and returns a JWT token (available at /api/login).
    """
    return login_handler(user_credentials, session)

# Include this router in the main app
def include_auth_router(app):
    app.include_router(root_router)  # Mount at root: /login
    app.include_router(api_router)   # Mount under API: /api/login