import time
from collections import defaultdict
from typing import Dict, List, Tuple
from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse, Response
from app.core.config import settings


class SlidingWindowRateLimiter:
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests_map: Dict[str, List[float]] = defaultdict(list)

    def is_allowed(self, client_ip: str) -> Tuple[bool, int, int]:
        now = time.time()
        window_start = now - self.window_seconds

        # Filter out timestamps older than the window
        timestamps = self.requests_map[client_ip]
        valid_timestamps = [t for t in timestamps if t > window_start]
        self.requests_map[client_ip] = valid_timestamps

        current_count = len(valid_timestamps)
        if current_count >= self.max_requests:
            oldest = valid_timestamps[0]
            retry_after = max(1, int(oldest + self.window_seconds - now))
            return False, 0, retry_after

        # Record this request
        valid_timestamps.append(now)
        remaining = self.max_requests - len(valid_timestamps)
        return True, remaining, self.window_seconds

    def reset_for_ip(self, client_ip: str) -> None:
        if client_ip in self.requests_map:
            del self.requests_map[client_ip]


rate_limiter = SlidingWindowRateLimiter(
    max_requests=settings.RATE_LIMIT_REQUESTS_PER_MINUTE,
    window_seconds=60,
)


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Exempt health probes, API documentation, and static files
        path = request.url.path
        if path.startswith(("/health", "/docs", "/redoc", "/openapi.json")):
            return await call_next(request)

        # Extract client IP, taking into account X-Forwarded-For if behind reverse proxy
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        else:
            client_ip = request.client.host if request.client else "127.0.0.1"

        allowed, remaining, reset_time = rate_limiter.is_allowed(client_ip)

        if not allowed:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": "Rate limit exceeded. Maximum 60 requests per minute allowed.",
                    "client_ip": client_ip,
                },
                headers={
                    "Retry-After": str(reset_time),
                    "X-RateLimit-Limit": str(rate_limiter.max_requests),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(reset_time),
                },
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(rate_limiter.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(reset_time)
        return response
