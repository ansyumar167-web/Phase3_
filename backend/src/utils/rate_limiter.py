import time
from collections import defaultdict, deque
from typing import Dict
from ..utils.logging_config import get_logger


logger = get_logger("rate_limiter")


class RateLimiter:
    """
    Simple in-memory rate limiter to limit API requests.
    NOTE: This is a basic implementation suitable for single-instance deployments.
    For production with multiple instances, consider using Redis-based rate limiting.
    """

    def __init__(self):
        # Dictionary to store request times for each user/endpoint
        self.requests: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))  # Store max 100 requests per user
        self.limits = {
            "requests_per_minute": 60,  # Default: 60 requests per minute
            "requests_per_hour": 1000,  # Default: 1000 requests per hour
        }

    def is_allowed(self, user_id: str, endpoint: str = "default") -> bool:
        """
        Check if a request is allowed based on rate limits.

        Args:
            user_id: The ID of the user making the request
            endpoint: The API endpoint being accessed

        Returns:
            True if request is allowed, False otherwise
        """
        current_time = time.time()
        identifier = f"{user_id}:{endpoint}"

        # Clean up old requests (older than 1 hour)
        self._cleanup_old_requests(identifier, current_time)

        # Count requests in the last minute
        requests_last_minute = sum(1 for req_time in self.requests[identifier]
                                  if current_time - req_time <= 60)

        # Count requests in the last hour
        requests_last_hour = len(self.requests[identifier])

        # Check rate limits
        if requests_last_minute >= self.limits["requests_per_minute"]:
            logger.warning(f"Rate limit exceeded for user {user_id} on endpoint {endpoint}: too many requests per minute")
            return False

        if requests_last_hour >= self.limits["requests_per_hour"]:
            logger.warning(f"Rate limit exceeded for user {user_id} on endpoint {endpoint}: too many requests per hour")
            return False

        # Add current request to the record
        self.requests[identifier].append(current_time)
        return True

    def _cleanup_old_requests(self, identifier: str, current_time: float):
        """
        Remove requests older than 1 hour from the record.

        Args:
            identifier: The user:endpoint identifier
            current_time: Current timestamp
        """
        # Remove requests older than 1 hour
        cutoff_time = current_time - 3600  # 1 hour in seconds

        # Create a new deque with only recent requests
        recent_requests = deque(maxlen=100)
        for req_time in self.requests[identifier]:
            if req_time >= cutoff_time:
                recent_requests.append(req_time)

        self.requests[identifier] = recent_requests


# Global rate limiter instance
rate_limiter = RateLimiter()


def check_rate_limit(user_id: str, endpoint: str = "default") -> bool:
    """
    Check if the user is within rate limits for the specified endpoint.

    Args:
        user_id: The ID of the user making the request
        endpoint: The API endpoint being accessed

    Returns:
        True if within limits, False otherwise
    """
    return rate_limiter.is_allowed(user_id, endpoint)


def set_rate_limits(requests_per_minute: int = 60, requests_per_hour: int = 1000):
    """
    Set the rate limits.

    Args:
        requests_per_minute: Maximum requests allowed per minute
        requests_per_hour: Maximum requests allowed per hour
    """
    rate_limiter.limits["requests_per_minute"] = requests_per_minute
    rate_limiter.limits["requests_per_hour"] = requests_per_hour
    logger.info(f"Rate limits updated: {requests_per_minute}/minute, {requests_per_hour}/hour")


def get_rate_limit_status(user_id: str, endpoint: str = "default") -> dict:
    """
    Get the current rate limit status for a user on an endpoint.

    Args:
        user_id: The ID of the user
        endpoint: The API endpoint

    Returns:
        Dictionary with rate limit information
    """
    current_time = time.time()
    identifier = f"{user_id}:{endpoint}"

    # Clean up old requests
    rate_limiter._cleanup_old_requests(identifier, current_time)

    # Count requests in the last minute
    requests_last_minute = sum(1 for req_time in rate_limiter.requests[identifier]
                              if current_time - req_time <= 60)

    # Count requests in the last hour
    requests_last_hour = len(rate_limiter.requests[identifier])

    return {
        "user_id": user_id,
        "endpoint": endpoint,
        "requests_last_minute": requests_last_minute,
        "requests_last_hour": requests_last_hour,
        "limit_per_minute": rate_limiter.limits["requests_per_minute"],
        "limit_per_hour": rate_limiter.limits["requests_per_hour"],
        "within_limits": (requests_last_minute < rate_limiter.limits["requests_per_minute"] and
                         requests_last_hour < rate_limiter.limits["requests_per_hour"])
    }