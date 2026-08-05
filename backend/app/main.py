from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.middleware.logging import LoggingMiddleware
from app.exception.handlers import register_exception_handlers

configure_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
)
app.include_router(api_router)

app.add_middleware(LoggingMiddleware)

register_exception_handlers(app)
