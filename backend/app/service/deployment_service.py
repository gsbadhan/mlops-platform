from sqlalchemy.orm import Session

from app.enums.stages import DeploymentState, ModelRegistryStages, DeploymentEvent
from app.exception.model_not_approved_exception import ModelNotApprovedException
from app.exception.version_not_found_exception import VersionNotFoundException
from app.exception.InvalidStateException import InvalidStateException
from app.exception.deployment_not_found_exception import DeploymentNotFoundException
from app.exception.InvalidTransitionException import InvalidTransitionException
from app.enums.stages import (
    DEPLOYMENT_STATE_TRANSITIONS,
    DEPLOYMENT_STATES_TO_EVENT,
)
from app.model.deployment import Deployment
from app.model.deployment_history import DeploymentHistory
from app.repository.deployment_repository import DeploymentRepository
from app.repository.deployment_history_repository import DeploymentHistoryRepository
from app.repository.model_version_repository import ModelVersionRepository
from app.schema.deployment import (
    CreateDeploymentRequest,
    DeploymentResponse,
    ChangeStateRequest,
)


class DeploymentService:

    def __init__(
        self,
        deployment_repository: DeploymentRepository,
        model_version_repository: ModelVersionRepository,
        deployment_history_repository: DeploymentHistoryRepository,
    ):
        self.deployment_repository = deployment_repository
        self.model_version_repository = model_version_repository
        self.deployment_history_repository = deployment_history_repository

    def create_deployment(
        self, db: Session, request: CreateDeploymentRequest
    ) -> tuple[Deployment, DeploymentHistory]:
        deployment = self.deployment_repository.find_by_idempotency_key(
            db, request.idempotency_key
        )

        if deployment:
            return (
                deployment,
                self.deployment_history_repository.find_latest_by_deployment(
                    db, deployment.id
                ),
            )

        model_version = self.model_version_repository.find_by_version_id(
            db, request.model_version_id
        )
        if model_version is None:
            raise VersionNotFoundException(version_id=request.model_version_id)

        if model_version.stage not in (ModelRegistryStages.APPROVED):
            raise ModelNotApprovedException(model_id=model_version.model_id)

        deployment = Deployment(
            model_version_id=model_version.id,
            environment=request.environment,
            status=DeploymentState.REQUESTED,
            retry_count=0,
            idempotency_key=request.idempotency_key,
        )

        deployment = self.deployment_repository.create(db, deployment)
        history = self._save_history(
            db=db,
            deployment=deployment,
            old_status=DeploymentState.NONE,
            event=DEPLOYMENT_STATES_TO_EVENT[(DeploymentState.NONE, deployment.status)],
        )
        return (deployment, history)

    def _save_history(
        self,
        db: Session,
        deployment: Deployment,
        old_status: DeploymentState,
        event: DeploymentEvent,
    ):
        history = DeploymentHistory(
            deployment_id=deployment.id,
            event=event,
            old_status=old_status,
            new_status=deployment.status,
        )
        return self.deployment_history_repository.create(db, history)

    def get_deployment(
        self, db: Session, deployment_id: str
    ) -> tuple[Deployment, DeploymentHistory]:
        deployment = self.deployment_repository.find_by_id(db, deployment_id)

        if deployment is None:
            raise DeploymentNotFoundException(deployment_id)

        return (
            deployment,
            self.deployment_history_repository.find_latest_by_deployment(
                db, deployment.id
            ),
        )

    def get_all_deployments(self, db: Session) -> list[Deployment, DeploymentHistory]:
        rows = self.deployment_repository.find_all_with_latest_history(db)
        return [
            DeploymentResponse(
                deployment_id=deployment.id,
                model_id=deployment.model_version.ml_model.id,
                version=deployment.model_version.version,
                environment=deployment.environment,
                status=deployment.status,
                event=history.event,
                timestamp=history.created_at,
            )
            for deployment, history in rows
        ]

    def retry(self, db: Session, deployment_id: str) -> DeploymentResponse:
        """
        Expected current state: FAILED
        State changes: FAILED -> REQUESTED
        Expected workflow: FAILED -> REQUESTED -> VALIDATING
        """
        deployment = self.deployment_repository.find_by_id(db, deployment_id)
        if deployment is None:
            raise DeploymentNotFoundException(deployment_id)

        if deployment.status != DeploymentState.FAILED:
            raise InvalidStateException(deployment.status.name)

        old_status = deployment.status
        deployment.status = DeploymentState.REQUESTED
        deployment.retry_count += 1

        return self._change_state(
            db,
            deployment,
            old_status,
            DEPLOYMENT_STATES_TO_EVENT[(old_status, deployment.status)],
        )

    def roolback(self, db: Session, deployment_id: str) -> DeploymentResponse:
        """
        Expected current state: SUCCEEDED
        State changes: SUCCEEDED -> ROLLED_BACK
        Expected workflow: SUCCEEDED -> ROLLED_BACK -> NONE
        """
        deployment = self.deployment_repository.find_by_id(db, deployment_id)
        if deployment is None:
            raise DeploymentNotFoundException(deployment_id)

        if deployment.status != DeploymentState.SUCCEEDED:
            raise InvalidStateException(deployment.status.name)

        old_status = deployment.status
        deployment.status = DeploymentState.ROLLED_BACK
        return self._change_state(
            db,
            deployment,
            old_status,
            DEPLOYMENT_STATES_TO_EVENT[(old_status, deployment.status)],
        )

    def change_state(
        self, db: Session, deployment_id: str, request: ChangeStateRequest
    ) -> DeploymentResponse:
        """
        Allowed state changes:
        REQUESTED -> VALIDATING, VALIDATING -> DEPLOYING,
        DEPLOYING -> SUCCEEDED, DEPLOYING -> FAILED
        """
        state_workflow_conditions = {
            DeploymentState.VALIDATING: DeploymentState.REQUESTED,
            DeploymentState.DEPLOYING: DeploymentState.VALIDATING,
            DeploymentState.SUCCEEDED: DeploymentState.DEPLOYING,
            DeploymentState.FAILED: DeploymentState.SUCCEEDED,
        }
        print(request.state)
        from_state = state_workflow_conditions[request.state]
        print(from_state)
        if from_state is None:
            raise InvalidStateException(request.state.name)

        deployment = self.deployment_repository.find_by_id(db, deployment_id)

        if deployment is None:
            raise DeploymentNotFoundException(deployment_id)

        if deployment.status != from_state:
            raise InvalidStateException(request.state.name)

        old_status = deployment.status
        deployment.status = request.state
        return self._change_state(
            db,
            deployment,
            old_status,
            DEPLOYMENT_STATES_TO_EVENT[(old_status, deployment.status)],
        )

    def _change_state(
        self,
        db: Session,
        deployment: Deployment,
        old_status: DeploymentState,
        event: DeploymentEvent,
    ) -> DeploymentResponse:
        self.validate_transition(old_status, deployment.status)
        self.deployment_repository.update(db, deployment)
        history = self._save_history(
            db=db, deployment=deployment, old_status=old_status, event=event
        )
        return (deployment, history)

    @staticmethod
    def validate_transition(current: DeploymentState, target: DeploymentState) -> None:
        if target not in DEPLOYMENT_STATE_TRANSITIONS[current]:
            raise InvalidTransitionException(current=current.name, target=target.name)
