from starlette import status

from app.exception.app_exception import AppException


class DuplicateVersionException(AppException):

    def __init__(self, model_id: str, version: str):
        super().__init__(
            message=f"Version '{version}' already exists for model '{model_id}'.",
            status_code=status.HTTP_409_CONFLICT,
        )
