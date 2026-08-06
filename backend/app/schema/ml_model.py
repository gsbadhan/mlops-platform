from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.enums.stages import Algorithm
from app.enums.stages import Framework


class CreateModelRequest(BaseModel):
    """
    Request payload for creating a new ML model.
    """

    name: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=10, max_length=400)
    framework: Framework
    algorithm: Algorithm


class UpdateModelRequest(BaseModel):
    """
    Request payload for updating an existing ML model.
    """

    description: str | None = None
    framework: Framework | None = None
    algorithm: Algorithm | None = None


class ModelResponse(BaseModel):
    """
    Response returned by Model Registry APIs.
    """

    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    description: str | None
    framework: Framework
    algorithm: Algorithm
    created_at: datetime
    updated_at: datetime
