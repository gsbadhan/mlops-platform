from starlette import status

from app.exception.app_exception import AppException


class DuplicateModelException(AppException):

    def __init__(self, model_name: str):
        super().__init__(
            message=f"Model '{model_name}' already exists.",
            status_code=status.HTTP_409_CONFLICT,
        )
