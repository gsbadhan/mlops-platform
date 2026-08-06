from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

from app.enums.stages import ModelRegistryStages


class CreateModelVersionRequest(BaseModel):
    """
    Request payload for registering a model version.
    """

    version: str = Field(..., min_length=1, max_length=30, examples=["1.0.0"])
    artifact_uri: str = Field(..., examples=["s3://models/fraud/1.0.0"])
    training_data_uri: str = Field(..., examples=["s3://datasets/fraud/train.csv"])
    tags: list[str] = Field(default_factory=list)


class ModelVersionResponse(BaseModel):
    """
    Response returned by Model Version APIs.
    """

    model_config = ConfigDict(from_attributes=True, frozen=True)
    id: UUID
    model_id: UUID
    version: str
    approved: bool
    stage: ModelRegistryStages
    artifact_uri: str
    training_data_uri: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime


class ChangeStageRequest(BaseModel):
    stage: ModelRegistryStages
