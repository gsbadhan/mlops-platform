from starlette import status

from app.exception.app_exception import AppException


class ModelNotApprovedException(AppException):

    def __init__(self, model_id: str):
        super().__init__(
            message=f"Model '{model_id}' not approved.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
