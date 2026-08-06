from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.enums.stages import Algorithm, Framework, ModelRegistryStages


class CreateModelRequest(BaseModel):
    """
    Request payload for creating a new ML model.
    """

    name: str = Field(..., min_length=2, max_length=100)
    owner: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=10, max_length=400)
    framework: Framework
    algorithm: Algorithm


class ModelResponse(BaseModel):
    """
    Response returned by Model Registry APIs.
    """

    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    owner: str
    description: str | None
    framework: Framework
    algorithm: Algorithm
    created_at: datetime
    updated_at: datetime


class ModelVersionSummaryResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    version: str
    stage: ModelRegistryStages
    approved: bool
    artifact_uri: str


class ModelSummaryResponse(BaseModel):
    """
    Response for Model summary.
    """

    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    owner: str
    description: str | None
    framework: Framework
    versions: list[ModelVersionSummaryResponse]
