from starlette import status

from app.exception.app_exception import AppException


class InvalidStateException(AppException):

    def __init__(self, state: str):
        super().__init__(
            message=f"Invalid state '{state}'.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
