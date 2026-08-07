from fastapi import FastAPI

from app.api.router import api_v1_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.middleware.logging import LoggingMiddleware
from app.exception.handlers import register_exception_handlers
from fastapi.middleware.cors import CORSMiddleware

configure_logging()

app = FastAPI(title=settings.app_name, version=settings.app_version)
app.include_router(api_v1_router)

app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
