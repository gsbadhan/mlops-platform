from starlette import status

from app.exception.app_exception import AppException


class VersionNotFoundException(AppException):

    def __init__(self, version_id: str):
        super().__init__(
            message=f"Version '{version_id}' not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
