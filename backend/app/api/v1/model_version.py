from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.model.model_version import ModelVersion
from app.schema.model_version import (
    CreateModelVersionRequest,
    ModelVersionResponse,
    ChangeStageRequest,
)

from app.service.dependencies import get_model_version_service
from app.service.model_version_service import ModelVersionService

router = APIRouter(prefix="/models/{model_id}/versions", tags=["Model Versions"])


@router.post(
    "", response_model=ModelVersionResponse, status_code=status.HTTP_201_CREATED
)
def create_model_version(
    model_id: UUID,
    request: CreateModelVersionRequest,
    db: Session = Depends(get_db),
    service: ModelVersionService = Depends(get_model_version_service),
):
    version = ModelVersion(
        model_id=str(model_id),
        version=request.version,
        artifact_uri=request.artifact_uri,
        training_data_uri=request.training_data_uri,
        tags=request.tags,
    )
    return service.register_version(db=db, version=version)


@router.get("", response_model=list[ModelVersionResponse])
def get_model_versions(
    model_id: UUID,
    db: Session = Depends(get_db),
    service: ModelVersionService = Depends(get_model_version_service),
):
    return service.list_versions(db=db, model_id=str(model_id))


@router.post("/{version_id}/stage", response_model=ModelVersionResponse)
def change_stage(
    model_id: UUID,
    version_id: UUID,
    request: ChangeStageRequest,
    db: Session = Depends(get_db),
    service: ModelVersionService = Depends(get_model_version_service),
):
    return service.change_stage(
        db=db,
        model_id=str(model_id),
        version_id=str(version_id),
        new_stage=request.stage,
    )
