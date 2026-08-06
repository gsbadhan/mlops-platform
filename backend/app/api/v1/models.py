from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.core.database import get_db
from app.service.dependencies import get_ml_model_service
from app.service.ml_model_service import MLModelService
from app.schema.ml_model import CreateModelRequest
from app.schema.ml_model import ModelResponse
from app.model.ml_model import MLModel

router = APIRouter(prefix="/models", tags=["Models"])


@router.post("", response_model=ModelResponse, status_code=201)
def create_model(
    request: CreateModelRequest,
    db: Session = Depends(get_db),
    service: MLModelService = Depends(get_ml_model_service),
):
    model = MLModel(
        name=request.name,
        description=request.description,
        framework=request.framework,
        algorithm=request.algorithm,
    )

    return service.create_model(db=db, model=model)


@router.get("", response_model=list[ModelResponse])
def get_models(
    db: Session = Depends(get_db),
    service: MLModelService = Depends(get_ml_model_service),
):
    return service.list_models(db)


@router.get("/{model_id}", response_model=ModelResponse)
def get_model(
    model_id: UUID,
    db: Session = Depends(get_db),
    service: MLModelService = Depends(get_ml_model_service),
):
    return service.get_model(db, str(model_id))
