from starlette import status

from app.exception.app_exception import AppException


class DeploymentNotFoundException(AppException):

    def __init__(self, deployment_id: str):
        super().__init__(
            message=f"Deployment '{deployment_id}' not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
