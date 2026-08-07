from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.service.dependencies import get_deployment_service
from app.service.deployment_service import DeploymentService
from app.schema.deployment import (
    CreateDeploymentRequest,
    DeploymentResponse,
    ChangeStateRequest,
)
from uuid import UUID

router = APIRouter(prefix="/deployments", tags=["Deployments"])


@router.post("", response_model=DeploymentResponse)
def create_deployment(
    request: CreateDeploymentRequest,
    db: Session = Depends(get_db),
    service: DeploymentService = Depends(get_deployment_service),
):
    deployment, history = service.create_deployment(db, request)
    return DeploymentResponse(
        deployment_id=deployment.id,
        model_id=deployment.model_version.ml_model.id,
        version=deployment.model_version.version,
        environment=deployment.environment,
        status=deployment.status,
        event=history.event,
        timestamp=deployment.created_at,
    )


@router.get("", response_model=list[DeploymentResponse])
def get_deployments(
    db: Session = Depends(get_db),
    service: DeploymentService = Depends(get_deployment_service),
):
    return service.get_all_deployments(db)


@router.get("/{deployment_id}", response_model=DeploymentResponse)
def get_deployment(
    deployment_id: UUID,
    db: Session = Depends(get_db),
    service: DeploymentService = Depends(get_deployment_service),
):
    deployment, history = service.get_deployment(db, str(deployment_id))
    return DeploymentResponse(
        deployment_id=deployment.id,
        model_id=deployment.model_version.ml_model.id,
        version=deployment.model_version.version,
        environment=deployment.environment,
        status=deployment.status,
        event=history.event,
        timestamp=deployment.created_at,
    )


@router.post("/{deployment_id}/retry", response_model=DeploymentResponse)
def retry_deployment(
    deployment_id: UUID,
    db: Session = Depends(get_db),
    service: DeploymentService = Depends(get_deployment_service),
):
    deployment, history = service.retry(db, str(deployment_id))
    return DeploymentResponse(
        deployment_id=deployment.id,
        model_id=deployment.model_version.ml_model.id,
        version=deployment.model_version.version,
        environment=deployment.environment,
        status=deployment.status,
        event=history.event,
        timestamp=deployment.created_at,
    )


@router.post("/{deployment_id}/rollback", response_model=DeploymentResponse)
def rollback_deployment(
    deployment_id: UUID,
    db: Session = Depends(get_db),
    service: DeploymentService = Depends(get_deployment_service),
):
    deployment, history = service.roolback(db, str(deployment_id))
    return DeploymentResponse(
        deployment_id=deployment.id,
        model_id=deployment.model_version.ml_model.id,
        version=deployment.model_version.version,
        environment=deployment.environment,
        status=deployment.status,
        event=history.event,
        timestamp=deployment.created_at,
    )


@router.post("/{deployment_id}/state", response_model=DeploymentResponse)
def change_deployment_state(
    deployment_id: UUID,
    request: ChangeStateRequest,
    db: Session = Depends(get_db),
    service: DeploymentService = Depends(get_deployment_service),
):
    deployment, history = service.change_state(db, str(deployment_id), request)
    return DeploymentResponse(
        deployment_id=deployment.id,
        model_id=deployment.model_version.ml_model.id,
        version=deployment.model_version.version,
        environment=deployment.environment,
        status=deployment.status,
        event=history.event,
        timestamp=deployment.created_at,
    )
