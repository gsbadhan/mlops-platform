from starlette import status

from app.exception.app_exception import AppException


class InvalidTransitionException(AppException):

    def __init__(self, current: str, target: str):
        super().__init__(
            message=f"Invalid lifecycle transition from '{current}' to '{target}'.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
