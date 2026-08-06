from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from app.exception.app_exception import AppException


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": exc.status_code, "message": exc.detail},
        )

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        print("caugt up in app_exception_handler ....")
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": exc.status_code, "message": exc.message},
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500, content={"status": 500, "message": "Internal Server Error"}
        )
