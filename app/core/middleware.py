"""
Logging middleware for FastAPI.

Logs request method, path, and processing time.
"""

import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("middleware")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log request method and URL
        logger.info(f"Incoming request: {request.method} {request.url.path}")

        response = await call_next(request)

        # Log request duration
        duration = time.time() - start_time
        logger.info(f"Completed {request.method} {request.url.path} in {duration:.3f}s")

        return response
