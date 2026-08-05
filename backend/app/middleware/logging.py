import time

from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import logger


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start = time.perf_counter()

        response = await call_next(request)

        duration = (time.perf_counter() - start) * 1000

        logger.info(
            "request",
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration_ms=round(duration, 2),
        )

        return response