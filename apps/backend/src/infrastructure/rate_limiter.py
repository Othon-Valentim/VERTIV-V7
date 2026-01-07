"""
VERTIV v6.0 - Rate Limiting Module
Protects API from abuse and DDoS attacks.
"""

import time
from collections import defaultdict
from typing import Optional, Callable
from fastapi import HTTPException, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import asyncio


class RateLimiter:
    """
    In-memory rate limiter using sliding window algorithm.

    For production at scale, consider using Redis-based rate limiting.
    """

    def __init__(
        self,
        requests_per_minute: int = 60,
        requests_per_second: int = 10,
        burst_size: int = 20
    ):
        self.requests_per_minute = requests_per_minute
        self.requests_per_second = requests_per_second
        self.burst_size = burst_size

        # Storage: {client_key: [(timestamp, count), ...]}
        self._minute_windows: dict = defaultdict(list)
        self._second_windows: dict = defaultdict(list)

        # Lock for thread safety
        self._lock = asyncio.Lock()

    def _get_client_key(self, request: Request) -> str:
        """
        Get unique client identifier.
        Uses X-Forwarded-For for proxied requests, falls back to client host.
        """
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            # Take the first IP in the chain (original client)
            return forwarded.split(",")[0].strip()

        # For authenticated requests, use user ID if available
        if hasattr(request.state, "user") and request.state.user:
            return f"user:{request.state.user.id}"

        return request.client.host if request.client else "unknown"

    def _cleanup_old_entries(self, entries: list, window_seconds: int) -> list:
        """Remove entries older than the window."""
        cutoff = time.time() - window_seconds
        return [entry for entry in entries if entry[0] > cutoff]

    async def check_rate_limit(self, request: Request) -> tuple[bool, dict]:
        """
        Check if request is within rate limits.

        Returns:
            (is_allowed, info_dict)
        """
        async with self._lock:
            client_key = self._get_client_key(request)
            current_time = time.time()

            # Cleanup old entries
            self._minute_windows[client_key] = self._cleanup_old_entries(
                self._minute_windows[client_key], 60
            )
            self._second_windows[client_key] = self._cleanup_old_entries(
                self._second_windows[client_key], 1
            )

            # Count requests
            minute_count = len(self._minute_windows[client_key])
            second_count = len(self._second_windows[client_key])

            # Check limits
            if minute_count >= self.requests_per_minute:
                return False, {
                    "error": "rate_limit_exceeded",
                    "limit": "minute",
                    "retry_after": 60 - (current_time - self._minute_windows[client_key][0][0]),
                    "requests_made": minute_count,
                    "requests_allowed": self.requests_per_minute
                }

            if second_count >= self.requests_per_second:
                return False, {
                    "error": "rate_limit_exceeded",
                    "limit": "second",
                    "retry_after": 1 - (current_time - self._second_windows[client_key][0][0]),
                    "requests_made": second_count,
                    "requests_allowed": self.requests_per_second
                }

            # Record this request
            self._minute_windows[client_key].append((current_time, 1))
            self._second_windows[client_key].append((current_time, 1))

            return True, {
                "remaining_minute": self.requests_per_minute - minute_count - 1,
                "remaining_second": self.requests_per_second - second_count - 1
            }


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware for rate limiting.
    """

    def __init__(
        self,
        app,
        limiter: RateLimiter,
        exclude_paths: Optional[list[str]] = None
    ):
        super().__init__(app)
        self.limiter = limiter
        self.exclude_paths = exclude_paths or ["/health", "/docs", "/openapi.json"]

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip rate limiting for excluded paths
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            return await call_next(request)

        # Check rate limit
        is_allowed, info = await self.limiter.check_rate_limit(request)

        if not is_allowed:
            retry_after = int(info.get("retry_after", 1)) + 1

            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Too Many Requests",
                    "message": f"Rate limit exceeded. Please wait {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit_type": info.get("limit"),
                    "requests_made": info.get("requests_made"),
                    "requests_allowed": info.get("requests_allowed")
                },
                headers={"Retry-After": str(retry_after)}
            )

        # Add rate limit headers to response
        response = await call_next(request)

        response.headers["X-RateLimit-Remaining-Minute"] = str(info.get("remaining_minute", 0))
        response.headers["X-RateLimit-Remaining-Second"] = str(info.get("remaining_second", 0))
        response.headers["X-RateLimit-Limit-Minute"] = str(self.limiter.requests_per_minute)
        response.headers["X-RateLimit-Limit-Second"] = str(self.limiter.requests_per_second)

        return response


# Global rate limiter instance with sensible defaults
# 60 requests/minute, 10 requests/second, burst of 20
default_limiter = RateLimiter(
    requests_per_minute=60,
    requests_per_second=10,
    burst_size=20
)


# Endpoint-specific limiters
simulation_limiter = RateLimiter(
    requests_per_minute=30,  # Simulations are expensive
    requests_per_second=5,
    burst_size=10
)


async def check_simulation_rate_limit(request: Request):
    """
    Dependency for rate limiting simulation endpoints.

    Usage:
        @app.post("/calculate/quick")
        async def calculate(
            project: ProjectTIV,
            _: None = Depends(check_simulation_rate_limit)
        ):
            ...
    """
    is_allowed, info = await simulation_limiter.check_rate_limit(request)

    if not is_allowed:
        retry_after = int(info.get("retry_after", 1)) + 1
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Simulation Rate Limit Exceeded",
                "message": f"Too many simulation requests. Please wait {retry_after} seconds.",
                "retry_after": retry_after
            },
            headers={"Retry-After": str(retry_after)}
        )
