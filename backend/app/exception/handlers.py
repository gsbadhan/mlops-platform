from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from app.exception.app_exception import AppException
from fastapi.exceptions import RequestValidationError


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": exc.status_code, "message": exc.detail, "errors": []},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        print(exc)
        errors = []
        for error in exc.errors():
            field = ".".join(str(loc) for loc in error.get("loc", []))
            errors.append(
                {
                    "field": field,
                    "message": error.get("msg", "Validation error"),
                    "type": error.get("type", "unknown"),
                }
            )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "status": status.HTTP_422_UNPROCESSABLE_CONTENT,
                "message": "Validation error",
                "errors": errors,
            },
        )

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": exc.status_code, "message": exc.message, "errors": []},
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"status": 500, "message": "Internal Server Error", "errors": []},
        )
