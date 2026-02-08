from fastapi import HTTPException, status, Request, Depends
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from typing import Optional, Dict, Any
import time
from functools import wraps
from ..config import settings
from .config import SECRET_KEY, ALGORITHM, get_current_user


class AuthMiddleware:
    """
    Authentication middleware class containing utility functions and decorators
    for handling authentication in the application.
    """

    def __init__(self):
        self.security = HTTPBearer(auto_error=False)

    async def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify a JWT token and return the payload if valid.

        Args:
            token: The JWT token to verify

        Returns:
            The decoded token payload if valid, None otherwise
        """
        try:
            # Decode with automatic expiration validation
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": True, "verify_exp": True})
            return payload
        except JWTError:
            return None

    def require_auth(self, roles: Optional[list] = None):
        """
        Decorator to require authentication for a route.

        Args:
            roles: Optional list of allowed roles

        Returns:
            A decorator function
        """
        def auth_decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Extract token from request (assuming it's passed as a dependency)
                request = kwargs.get('request') or next((arg for arg in args if isinstance(arg, Request)), None)

                if not request:
                    # Look for token in dependencies
                    token = kwargs.get('token')
                    if not token:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="No authentication token provided"
                        )
                else:
                    authorization = request.headers.get("Authorization")
                    if not authorization:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="No authorization header provided"
                        )

                    # Extract token from Authorization header
                    try:
                        token_type, token = authorization.split(" ")
                        if token_type.lower() != "bearer":
                            raise HTTPException(
                                status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid token type"
                            )
                    except ValueError:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authorization header format"
                        )

                # Verify token
                payload = await self.verify_token(token)
                if not payload:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid or expired token"
                    )

                # Check roles if specified
                if roles:
                    user_role = payload.get("role", "user")
                    if user_role not in roles:
                        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail="Insufficient permissions"
                        )

                # Add user info to kwargs
                kwargs['current_user'] = payload.get("sub")
                kwargs['current_user_id'] = payload.get("user_id")
                kwargs['current_user_role'] = payload.get("role", "user")

                return await func(*args, **kwargs)
            return wrapper
        return auth_decorator


# Global auth middleware instance
auth_middleware = AuthMiddleware()


def get_current_active_user(current_user: str = Depends(get_current_user)):
    """Dependency to get the current active user, ensuring they exist and are active."""
    if current_user is None:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def require_role(required_role: str):
    """
    Decorator to require a specific role for a route.

    Args:
        required_role: The role required to access the route

    Returns:
        A decorator function
    """
    def role_checker(payload: dict = Depends(get_current_user)):
        user_role = payload.get("role", "user")
        if user_role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role {required_role} required to access this resource"
            )
        return payload
    return role_checker


# Utility function to create auth dependency
def create_auth_dependency(roles: Optional[list] = None):
    """
    Create an authentication dependency with optional role checking.

    Args:
        roles: Optional list of allowed roles

    Returns:
        A dependency function
    """
    async def auth_dep(
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ):
        payload = await auth_middleware.verify_token(credentials.credentials)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )

        # Check roles if specified
        if roles:
            user_role = payload.get("role", "user")
            if user_role not in roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )

        return payload

    return auth_dep