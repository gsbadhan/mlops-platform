from starlette import status

from app.exception.app_exception import AppException


class ModelNotFoundException(AppException):

    def __init__(self, model_id: str):
        super().__init__(
            message=f"Model '{model_id}' not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )